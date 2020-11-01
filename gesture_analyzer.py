import draw_service
import os,sys
import time
import cv2
import numpy as np

FINGER_BASE_COORDS = [17, 13, 9, 5, 2]
PALM_CENTER_INDEX = 0
POSITIVE_INF = float('inf')
DETECTED_COLOR = draw_service.BGR_BLUE
FACE_INDICES = [0, 15, 16, 17, 18]
RIGHT_ARM_INDICES = [5, 6, 7]
LEFT_ARM_INDICES = [2, 3, 4]
LEar_INDEX = 17
Nose_INDEX = 0
REar_INDEX = 16
FINGER_TIP_COORDS = [20, 16, 12, 8, 4]
dir_path = os.path.dirname(os.path.realpath(__file__))
OPENPOSE_DIR = '/home/david/openpose/'
MODEL_DIR = os.path.join(OPENPOSE_DIR,'models/')
try:
    sys.path.append(os.path.join(OPENPOSE_DIR,'build/python/'))
    from openpose import pyopenpose as op
except ImportError as ಠ_ಠ:
    print(
        'Error: OpenPose library could not be found in {}. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?'.format(os.path.join(OPENPOSE_DIR,'build/python/')))
    raise ಠ_ಠ

FACE_KEYPOINT_PART_NAMES = ["Nose", "LEye", "REye", "LEar", "REar"]
ARMS_KEYPOINT_PART_NAMES = ["RShoulder", "LShoulder","RElbow","LElbow","LWrist","RWrist"]
RIGHT_ARMS = [part for part in ARMS_KEYPOINT_PART_NAMES if part.startswith("L")]
LEFT_ARMS = [part for part in ARMS_KEYPOINT_PART_NAMES if part.startswith("R")]
LEFT_COLOR = draw_service.BGR_GRINK
RIGHT_COLOR = draw_service.BGR_GRORANGE
STATIC_COLOR = draw_service.BGR_GRAY

POSE_INDICES = {"Nose": 0,
                "Neck": 1,
                "RShoulder": 2,
                "RElbow": 3,
                "RWrist": 4,
                "LShoulder": 5,
                "LElbow": 6,
                "LWrist": 7,
                "MidHip": 8,
                "RHip": 9,
                "RKnee": 10,
                "RAnkle": 11,
                "LHip": 12,
                "LKnee": 13,
                "LAnkle": 14,
                "REye": 15,
                "LEye": 16,
                "REar": 17,
                "LEar": 18,
                "LBigToe": 19,
                "LSmallToe": 20,
                "LHeel": 21,
                "RBigToe": 22,
                "RSmallToe": 23,
                "RHeel": 24}

def get_pose_keypoint_coord_dict(pose_keypoints,requested_parts=None):
    """
    Will return whatever is in the correct index (expects keypoints array or coordinates array).
    """
    if requested_parts is None: # return all of the coords
        requested_parts = list(POSE_INDICES.keys())
    out_dict = dict()
    for part in requested_parts:
        # update the out_dict with the wanted pose keypoint
        out_dict[part] = pose_keypoints[POSE_INDICES[part]]
    return out_dict


def get_specific_pose_keypoint_coords(pose_dict, body_part_list=None):
    if body_part_list is None: # return all of the coords
        body_part_list = list(POSE_INDICES.keys())
    return [pose_dict[part] for part in body_part_list]

def draw_list_of_coords(frame, coords_list, color=draw_service.BGR_RED, dist=1, border_width=4):
    for point_coords in coords_list:
        draw_service.draw_square_around_pixel(frame, point_coords, dist=dist, border_width=border_width, color=color)

class GestureAnalyzer:
    def __init__(self,enabled = True,detect_user_look=True,detect_hands_gesture=True,draw_verbose=True):
        if enabled not in {True,False}:
            raise Exception("Unknown enabled value, expected a boolean")
        self.enabled = enabled
        self.detect_user_look = detect_user_look
        self.detect_hand_gestures = detect_hands_gesture
        self.draw_verbose = draw_verbose
        print("Created new GestureAnalyzer with params:\n\tenabled={}\n\tdetect_user_lookg={}\n\tdetect_hands_gestures={}")

    def is_user_looking(self,pose_coords,dist_factor=60):
        # left and right are reversed since we are looking at left right with respect to the image coords
        right_ear = pose_coords[REar_INDEX]
        # right_eye = keypoints_dict["LEye"]
        nose = pose_coords[Nose_INDEX]
        # left_eye = keypoints_dict["REye"]
        left_ear = pose_coords[LEar_INDEX]
        right_dist = np.linalg.norm(right_ear-nose)
        left_dist = np.linalg.norm(left_ear-nose)
        dist_diff = right_dist-left_dist
        horizontal_distances_ok = -dist_factor<dist_diff<dist_factor
        # print("{} - {} = {}".format(right_dist,left_dist,dist_diff))
        return horizontal_distances_ok

    def detect_palm(self, palm_coords, is_right_hand=True):
        # check to see that thumb is inner and pinky is outer, this means palm is towards the camera
        finger_tips = palm_coords[FINGER_TIP_COORDS]
        finger_bases = palm_coords[FINGER_BASE_COORDS]
        if len(finger_tips)!=len(finger_bases) or np.count_nonzero(finger_bases)==0 or np.count_nonzero(finger_tips)==0:
            return False
        lst_tip = finger_tips if is_right_hand else finger_tips[::-1]
        lst_base = finger_bases if is_right_hand else finger_bases[::-1]
        last = POSITIVE_INF
        # checks to see if any finger tip is below finger base, which indicates incorrect hand orientation
        for (x_tip, y_tip),(x_base, y_base) in zip(lst_tip,lst_base):
            if y_tip>y_base or x_tip >= last:
                return False
            last=x_tip
        return True

    def wrist_lower_than_palm(self, palm, wrist):
        # print(wrist)
        # print(palm)
        wrist_y = wrist[1]
        for x, y in palm[:-1]:  # iterate on all fingers without the thumb
            if y>0 and y < wrist_y:  # meaning the finger is detected and it's higher than the wrist
                return False
        return True

    def do_round(self,frame,datum):
        try:
            pose_coords = np.array(datum.poseKeypoints[0, :, :2]).astype("int")
            left_palm_pose,right_palm_pose = np.array(datum.handKeypoints)[:,0, :, :2]
            # left, right = np.array(datum.handKeypoints)
            # left_palm, right_palm = left[0, :, :2], right[0, :, :2]
        except Exception as e:
            print(e)
            return None,None
        # extract all keypoints that we need
        # left_palm,left_palm_center = right_palm_pose[PALM_POSE_COORDS],right_palm_pose[PALM_CENTER_INDEX]
        # right_palm,right_palm_center = left_palm_pose[PALM_POSE_COORDS],left_palm_pose[PALM_CENTER_INDEX]
        left_palm, left_palm_center = right_palm_pose, right_palm_pose[PALM_CENTER_INDEX]
        right_palm, right_palm_center = left_palm_pose, left_palm_pose[PALM_CENTER_INDEX]
        # shoulder elboy wrist
        # LEFT_ARM_INDICES = [2, 3, 4]
        left_arm_pose = pose_coords[LEFT_ARM_INDICES]
        # RIGHT_ARM_INDICES = [5, 6, 7]
        right_arm_pose = pose_coords[RIGHT_ARM_INDICES]
        face_pose = pose_coords[FACE_INDICES]

        detected_face = False
        if self.detect_user_look:
            detected_face = self.is_user_looking(pose_coords)


        detected_left_arm = False
        detected_right_arm = False
        detected_left_palm = False
        detected_right_palm = False
        detected_left_hold_it = False
        detected_right_hold_it = False
        if self.detect_hand_gestures:
            # ARMS
            left_palm_lower_than_wrist = self.wrist_lower_than_palm(left_palm[FINGER_TIP_COORDS], left_arm_pose[2])
            right_palm_lower_than_wrist = self.wrist_lower_than_palm(right_palm[FINGER_TIP_COORDS], right_arm_pose[2])
            # pinky -> thumb on the right hand on screen
            # PALM_POSE_COORDS = [20, 16, 12, 8, 4]

            # PALMS
            detected_right_palm = self.detect_palm(right_palm, is_right_hand=True)
            detected_left_palm = self.detect_palm(left_palm, is_right_hand=False)

            detected_left_hold_it = detected_left_palm and not left_palm_lower_than_wrist
            detected_right_hold_it = detected_right_palm and not right_palm_lower_than_wrist

        # prepare coords and colors
        face_color = DETECTED_COLOR if detected_face else STATIC_COLOR
        left_arm_color = DETECTED_COLOR if detected_left_arm else STATIC_COLOR
        right_arm_color = DETECTED_COLOR if detected_right_arm else STATIC_COLOR
        left_palm_color = DETECTED_COLOR if detected_left_palm else STATIC_COLOR
        right_palm_color = DETECTED_COLOR if detected_right_palm else STATIC_COLOR

        msg = []
        if detected_face:
            msg.append("USER_LOOK")
        if detected_left_arm:
            msg.append("LEFT_ARM")
        if detected_right_arm:
            msg.append("RIGHT_ARM")
        if detected_left_palm:
            msg.append("LEFT_PALM")
        if detected_right_palm:
            msg.append("RIGHT_PALM")
        if detected_left_hold_it:
            msg.append("LEFT_HOLD_IT")
        if detected_right_hold_it:
            msg.append("RIGHT_HOLD_IT")
        if len(msg)>0:
            print("DETECTED: {}".format(msg))
            print("*"*30)
        keypoint_summary = ((face_pose,face_color), (left_arm_pose,left_arm_color), (right_arm_pose,right_arm_color), (left_palm[FINGER_TIP_COORDS], left_palm_color), (right_palm[FINGER_TIP_COORDS], right_palm_color))
        detection_summary = (detected_face
                             ,detected_left_arm,detected_left_palm, detected_left_hold_it
                             ,detected_right_arm,detected_right_palm,detected_right_hold_it)
        # detection_summary = (
        # detected_face, detected_left_arm, detected_left_palm, detected_right_arm, detected_left_hold_it,
        # detected_right_hold_it)
        return detection_summary,keypoint_summary





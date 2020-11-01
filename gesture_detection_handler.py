"""
Keypoint detection reference:
when running this as is without changing parameters, here's what you would expect:
This will initialize the camera and openpose wrapper.
Then will loop and every few frames will try to find the pose and hands of a single person.
When it finds keypoints, it will mark them (blue/red for right/left hands and green for entire body) and will
highlight the face (light blue) and arms (purple).
Will exit when ESC is pressed.

Note - change the openpose import section so that it will work for you, rest should work as is.
Extra requirements:
    cv2, numpy
"""

import os,sys
import time
import cv2
import draw_service
from gesture_analyzer import GestureAnalyzer

GESTURE_LIST = ["face", "left arm", "left palm", "left hold it", "right arm", "right palm", "right hold it", "stop"]

dir_path = os.path.dirname(os.path.realpath(__file__))
OPENPOSE_DIR = '/home/david/openpose/'
MODEL_DIR = os.path.join(OPENPOSE_DIR,'models/')
try:
    sys.path.append(os.path.join(OPENPOSE_DIR,'build/python/'))
    from openpose import pyopenpose as op
except ImportError as stupid_ass_exception:
    print(
        'ಠ_ಠ: OpenPose library could not be found in {}. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?'.format(os.path.join(OPENPOSE_DIR,'build/python/')))
    raise stupid_ass_exception

ESC_BUTTON_KEY_CODE = 27
CV2_WINDOW_TITLE = "Openpose keypoint detector"
BGR_GREEN = (0, 255, 0)
BGR_RED = (0, 0, 255)
BGR_BLUE = (255, 0, 0)
BGR_LIGHT_BLUE = (255, 155, 155)
BGR_PURPLE = (128, 0, 128)
HAND_DETECTOR_MODEL = 2
FACE_KEYPOINT_PART_NAMES = ["Nose", "LEye", "REye", "LEar", "REar"]
ARMS_KEYPOINT_PART_NAMES = ["RShoulder", "LShoulder","RElbow","LElbow","LWrist","RWrist"]
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


def get_configured_opWrapper(hand=True,face=False,body=1, number_people_max=1,frame_step=3,render_threshold=0.5,model_folder=MODEL_DIR):
    """
    model_folder should basically point to openpose/models/
    Face takes an enormous amount of VRAM, this can make openpose crash due to insufficient VRAM, so face defaults
    to False.
    """
    params = dict()
    params["model_folder"] = model_folder
    params["hand"] = hand
    if hand and body != 1:
        # since body detection is off, we cannot use it's model (the default) so we use hand detection model
        params["hand_detector"] = HAND_DETECTOR_MODEL
    params["body"] = body
    params["face"] = face
    params["number_people_max"] = number_people_max
    params["frame_step"] = frame_step
    params["render_threshold"] = render_threshold
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    return opWrapper

def draw_square_around_pixel(image, pixel, dist, border_width=1, color=BGR_GREEN):
    x,y = pixel
    top_left = (x-dist,y-dist)
    bot_right = (x+dist,y+dist)
    cv2.rectangle(image,top_left,bot_right,color,border_width)

def mark_keypoint_array(frame, keypoint_coords, dist=1, width=1, color=BGR_GREEN):
    """
    Draws squares around all given keypoint coordinates.
    """
    for x,y in keypoint_coords:
        draw_square_around_pixel(frame, (int(x),int(y)), dist=dist, border_width=width, color = color)
    return keypoint_coords

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


def draw_specific_pose_keypoints(frame, pose_dict, body_part_list, color=BGR_RED, dist=1, border_width=4):
    specific_coords = []
    for part in body_part_list:
        draw_square_around_pixel(frame, pose_dict[part], dist=dist, border_width=border_width, color=color)
        specific_coords.append(pose_dict[part])

def detect_keypoints_from_camera(camera,work_in_background=True,enable_speech = False, frames_between_gestures = 15, visualize_detection = True, draw_openpose_render = False, detect_hands=True, detect_face=False, detect_pose=True, seconds_between_frames=0.01, frames_between_detection=5, print_keypoint_traces=True, verbose=False):
    """
    :param camera: the cv2 VideoCapture object that represents our camera
    :param visualize_detection: if True - will enable rendering and showing of frames and detections
    :param draw_openpose_render: if this is True, the render from openpose will be drawn (can be turned off with False)
    :param detect_hands: True to detect, False to ignore hands
    :param detect_face: same as detect_hands
    :param detect_pose: same as detect_hands
    :param seconds_between_frames: self explanatory - lower numbers = higher load but higher numbers = higher latency (lower FPS as well)
    :param frames_between_detection: attempt detection on every n'th frame - lower numbers = higher load but higher numbers = higher latency
    :param print_keypoint_traces: print last known coordinates of all keypoints between frames
    :param verbose: print data to the console
    """
    if camera is None:
        raise Exception("Camera is None.. are you kidding me??")
    print("Initializing...")
    visualize_detection = (not work_in_background) and visualize_detection
    if not work_in_background:
        cv2.namedWindow(CV2_WINDOW_TITLE, cv2.WINDOW_AUTOSIZE)

    opWrapper = get_configured_opWrapper(hand=detect_hands, face=detect_face, body=int(detect_pose), number_people_max=1, frame_step=15)
    opWrapper.start()
    datum = op.Datum()
    finished = False
    current_frame_num = 0
    print("Done\nPress ESC to quit.")
    gesture_analyzer = GestureAnalyzer(draw_verbose=visualize_detection)
    frames_from_last_gesture = frames_between_gestures # enable gesture recognition immediately
    last_detection,last_keypoints = None,None
    while not finished:  # run until user presses ESC
        frames_from_last_gesture += 1
        # frame timing parameters
        current_frame_num = current_frame_num%frames_between_detection
        time.sleep(seconds_between_frames)
        # read a frame from the camera
        _, frame = camera.read()
        # refresh the datum object and detect keypoints
        if current_frame_num == 0:
            datum.cvInputData = frame
            last_detection,last_keypoints = gesture_analyzer.do_round(frame,datum)
            opWrapper.emplaceAndPop([datum])
        if last_keypoints is not None and visualize_detection:
            for area_coords, draw_color in last_keypoints:
                draw_service.mark_keypoint_array(frame, area_coords, color=draw_color)
        if frames_from_last_gesture >= frames_between_gestures and last_detection is not None and any(last_detection):
            frames_from_last_gesture = 0 # reset gesture recognition cooldown
            detected_face, detected_left_arm, detected_left_palm, detected_left_hold_it, detected_right_arm, detected_right_palm, detected_right_hold_it = last_detection
            stop_gesture = detected_right_hold_it and detected_left_hold_it
            detection_list = detected_face, detected_left_arm, detected_left_palm, detected_left_hold_it, detected_right_arm, detected_right_palm, detected_right_hold_it, stop_gesture
            yield detection_list
        if not work_in_background:
            cv2.imshow(CV2_WINDOW_TITLE, frame)
        current_frame_num += 1
        # keypress = cv2.waitKey(1) & 0xFF
        keypress = cv2.waitKey(1)
        if keypress == ESC_BUTTON_KEY_CODE:  # escape button means exit and finish the run
            print("User pressed the exit button (ESC), exiting...")
            exit()

    if not work_in_background:
        cv2.destroyAllWindows()

def wait_for_gesture(show_detection_screen=False,verbose=False):
    # yields gestures as it detects them from the camera
    camera = cv2.VideoCapture(0)
    gesture = detect_keypoints_from_camera(camera, frames_between_detection=4, work_in_background=not show_detection_screen, verbose=verbose)

    for gest in gesture:
        if verbose:
            # detected_face, detected_left_arm, detected_left_palm, detected_left_hold_it, detected_right_arm, detected_right_palm, detected_right_hold_it, stop
            print("Detected the following gestures:")
            for i,detected in enumerate(gest):
                if detected:
                    print("\t{}".format(GESTURE_LIST[i]))
        yield gest
    camera.release()
    return None


if __name__ == '__main__':
    gest = wait_for_gesture(verbose=True)
    for g in gest:
        print()

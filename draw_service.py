import cv2
import numpy as np

BGR_GREEN = (0, 255, 0)
BGR_RED = (0, 0, 255)
BGR_BLUE = (255, 0, 0)
BGR_LIGHT_BLUE = (255, 155, 155)
BGR_PURPLE = (128, 0, 128)
BGR_GRAY = (128,128,128)
BGR_GRORANGE = (255,178,102)
BGR_GRINK = (255,204,255)

def draw_square_around_pixel(image, pixel, dist, border_width=1, color=BGR_GREEN):
    x,y = pixel
    top_left = (x-dist,y-dist)
    bot_right = (x+dist,y+dist)
    cv2.rectangle(image,top_left,bot_right,color,border_width)

def mark_keypoint_array(frame, keypoint_coords, dist=1, width=2, color=BGR_GRAY):
    """
    Draws squares around all given keypoint coordinates.
    """
    for x,y in keypoint_coords:
        draw_square_around_pixel(frame, (int(x),int(y)), dist=dist, border_width=width, color = color)
    return keypoint_coords


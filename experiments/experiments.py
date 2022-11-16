import numpy as np
import cv2
from matplotlib import pyplot as plt
import random 
import math
import time

def run_experiments(filename):

    print("\033[4m" + "Running:" + "\033[0m" + "\033[94m" + " " + filename + "\033[0m")

    start_time = time.time()


    ############# Image Input #############
    img_rgb = cv2.imread(filename)
    img_grey = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    ############# Image Input #############

    ############# Top Casing #############
    img_top_casing = img_grey[150:1200, 50:1150]
    ret, img_top_casing_binary = cv2.threshold(img_top_casing,150,255,cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(img_top_casing_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contour_list = []
    outer_contour = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        area = cv2.contourArea(contour)
        if 500000 < area:
            outer_contour = contour
        if 4000 < area < 5600:
            contour_list.append(contour)

    (x,y),main_radius = cv2.minEnclosingCircle(outer_contour)
    each_pixel = 50 / main_radius

    diameters = []

    for i in range(len(contour_list)):
        (x,y),radius = cv2.minEnclosingCircle(contour_list[i])
        hole_diameter = radius * 2 * each_pixel
        diameters.append(hole_diameter)

    top_casing_error = False

    for i in diameters:
        if not (7.7 < i < 8.7):
            top_casing_error = True

    if top_casing_error:
        print("\033[95m" + "Top Casing: " + "\033[0m" + "\033[91m" + "FAIL" + "\033[0m")
    else:
        print("\033[95m" + "Top Casing: " + "\033[0m" + "\033[92m" + "PASS" + "\033[0m")
    # 100, 8.2
    ############# Top Casing #############

    ############# Bottom Casing #############
    img_bottom_casing = img_grey[1300:2300,100:1100]
    ret, img_bottom_casing_binary = cv2.threshold(img_bottom_casing,220,255,cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(img_bottom_casing_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contour_list = []
    outer_contour = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        area = cv2.contourArea(contour)
        if 500000 < area:
            outer_contour = contour

    (x,y),main_radius = cv2.minEnclosingCircle(outer_contour)
    each_pixel_bottom_casing = 50 / main_radius

    diameters = []

    left_hole = img_bottom_casing[440:550, 360:470]
    left_hole = cv2.equalizeHist(left_hole)
    ret, left_hole_binary = cv2.threshold(left_hole,15,255,cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(left_hole_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contour_list = []
    outer_contour_left = None
    outer_contour_right = None
    for contour in contours:
        area = cv2.contourArea(contour)
        if 500 < area < 1500:
            outer_contour_left = contour
    centre,main_radius_left_hole = cv2.minEnclosingCircle(outer_contour_left)
    diameters.append(main_radius_left_hole * 2 * each_pixel_bottom_casing)

    right_hole = img_bottom_casing[445:555, 550:660]
    right_hole = cv2.equalizeHist(right_hole)
    ret, right_hole_binary = cv2.threshold(right_hole,15,255,cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(right_hole_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contour_list = []
    outer_contour_left = None
    outer_contour_right = None
    for contour in contours:
        area = cv2.contourArea(contour)
        if 500 < area < 1500:
            outer_contour_right = contour
    centre,main_radius_right_hole = cv2.minEnclosingCircle(outer_contour_right)
    diameters.append(main_radius_right_hole * 2 * each_pixel_bottom_casing)

    bottom_casing_error = False

    for i in diameters:
        if not (7.7 < i < 8.7):
            bottom_casing_error = True

    if bottom_casing_error:
        print("\033[95m" + "Bottom Casing: " + "\033[0m" + "\033[91m" + "FAIL" + "\033[0m")
    else:
        print("\033[95m" + "Bottom Casing: " + "\033[0m" + "\033[92m" + "PASS" + "\033[0m")
    ############# Bottom Casing #############

    ############# Small Gear #############
    img_small_gear = img_grey[1000:1160, 1460:1620]
    ret, img_small_gear_binary = cv2.threshold(img_small_gear,70,255,cv2.THRESH_BINARY)
    img_small_gear_binary = cv2.morphologyEx(img_small_gear_binary, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,9)))

    contours, hierarchy = cv2.findContours(img_small_gear_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contour_list = []
    outer_contour = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        area = cv2.contourArea(contour)
        if 5000 < area:
            outer_contour = contour

    centre,main_radius = cv2.minEnclosingCircle(outer_contour)
    main_radius -= 15

    blank = np.full((img_small_gear.shape[0], img_small_gear.shape[1]), 0, dtype=np.uint8)
    img1 = cv2.circle(blank.copy(),(int(centre[0]),int(centre[1])), int(main_radius), 20, 2)
    img2 = cv2.drawContours(blank.copy(), outer_contour, -1, 20, 2)
    intersection = img1 + img2
    ret, intersection = cv2.threshold(intersection,30,255,cv2.THRESH_BINARY)

    cnts = cv2.findContours(intersection, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    small_gear_error = False
    if int(len(cnts)/2) != 14:
        small_gear_error = True

    if small_gear_error:
        print("\033[95m" + "Small Gear: " + "\033[0m" + "\033[91m" + "FAIL" + "\033[0m")
    else:
        print("\033[95m" + "Small Gear: " + "\033[0m" + "\033[92m" + "PASS" + "\033[0m")
    ############# Small Gear #############

    ############# Large Gear #############
    img_large_gear = img_grey[140:490, 1350:1700]
    ret, img_large_gear_binary = cv2.threshold(img_large_gear,100,255,cv2.THRESH_BINARY)
    img_large_gear_binary = cv2.morphologyEx(img_large_gear_binary, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,9)))

    contours, hierarchy = cv2.findContours(img_large_gear_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contour_list = []
    outer_contour = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        area = cv2.contourArea(contour)
        if 40000 < area:
            outer_contour = contour

    centre,main_radius = cv2.minEnclosingCircle(outer_contour)
    main_radius -= 15

    blank = np.full((img_large_gear.shape[0], img_large_gear.shape[1]), 0, dtype=np.uint8)
    img1 = cv2.circle(blank.copy(),(int(centre[0]),int(centre[1])), int(main_radius), 20, 2)
    img2 = cv2.drawContours(blank.copy(), outer_contour, -1, 20, 2)
    intersection = img1 + img2
    ret, intersection = cv2.threshold(intersection,30,255,cv2.THRESH_BINARY)

    cnts = cv2.findContours(intersection, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    large_gear_error = False
    if int(len(cnts)/2) != 28:
        large_gear_error = True

    if large_gear_error:
        print("\033[95m" + "Large Gear: " + "\033[0m" + "\033[91m" + "FAIL" + "\033[0m")
    else:
        print("\033[95m" + "Large Gear: " + "\033[0m" + "\033[92m" + "PASS" + "\033[0m")
    ############# Large Gear #############

    print("\033[1m" + "Runtime: " + "\033[0m" + "\033[93m" + f"{((time.time() - start_time)):.3f}" + " seconds" + "\033[0m")
    print("\n")

run_experiments('set1x.jpg')
run_experiments('set2x.jpg')
run_experiments('set3x_notooth.jpg')
run_experiments('set3x_notooth_rot.jpg')
run_experiments('set4x_worn.jpg')
run_experiments('set5x.jpg')
run_experiments('set6x.jpg')
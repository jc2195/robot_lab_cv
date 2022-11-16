#%%
import cv2
import matplotlib.pyplot as plt
import numpy as np

#%%
#fig, ax = plt.subplots(1, 2, figsize=(18, 6), dpi=100)

## Read
img1 = cv2.imread("real_test.jpg")
img2 = cv2.imread("Lab_big.jpg")
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)


bottom_case = img1[120:1200, 110:1200]
large_gear = img1[100:450, 1450:1780]
small_gear = img1[950:1150, 1510:1700]
top_case = img1[1300:2300,110:1200]


#print(np.array(bottom_case).shape)
def is_object_there(img):

    """
    Fist checks if an image is grey scaled and changes it if not
    This looks at the middle pixel of an image,
    assesses whether it is a part or the black background
    """
    if len(np.array(bottom_case).shape) != 2:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    half = len(img)//2
    if img[half, half] > 100:
        return True
    else:
        return False




#%%

gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

ret, threshed = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY)
kernel = np.ones((3, 3), np.uint8)

img_dilate = cv2.dilate(threshed, kernel, iterations=1)
contours, hierachy= cv2.findContours(img_dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


#%%


if len(contours) != 0:


    # find the biggest countour (c) by the area
    c = max(contours, key = cv2.contourArea)

## Approx the contour
arclen = cv2.arcLength(c, True)
approx = cv2.approxPolyDP(c, 0.005*arclen, True)

## Draw and output the result
for pt in approx:
    cv2.circle(img1, (pt[0][0],pt[0][1]), 3, (0,255,0), -1, cv2.LINE_AA)

msg = "Total: {}".format(len(approx)//2)
cv2.putText(img1, msg, (20,40),cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2, cv2.LINE_AA)

## Display
#cv2.imshow("res", img1);cv2.waitKey()



# %%



# %%

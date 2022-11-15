#%%
import cv2
import matplotlib.pyplot as plt
import numpy as np
#%%
fig, ax = plt.subplots(1, 2, figsize=(18, 6), dpi=100)

## Read
img1 = cv2.imread("real_test.jpg")
img2 = cv2.imread("Lab_big.jpg")

bottom_case = img1[120:1200, 110:1200]
large_gear = img1[100:450, 1450:1780]
small_gear = img1[950:1150, 1510:1700]
top_case = img1[1300:2300,110:1200]


#%%

gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

ret, threshed = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY)
kernel = np.ones((3, 3), np.uint8)

img_dilate = cv2.dilate(threshed, kernel, iterations=1)
contours, hierachy= cv2.findContours(img_dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
ax[0].imshow(img_dilate, cmap='gray')
ax[1].imshow(threshed, cmap='gray')

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
cv2.imshow("res", img1);cv2.waitKey()



# %%

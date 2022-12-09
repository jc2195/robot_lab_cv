import numpy as np
import cv2

class ImageManipulation:
    def trimImage(image, boundary):
        image = image[
                boundary[0]:boundary[1],
                boundary[2]:boundary[3]
            ]
        return image

    def binaryFilter(image, min_limit, max_limit):
        ret, image = cv2.threshold(image, min_limit, max_limit, cv2.THRESH_BINARY)
        return image

    def morphologyOpen(image):
        return cv2.morphologyEx(image, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,9)))

    def presenceDetection(image):
        if len(np.array(image).shape) != 2:
            image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        half = len(image)//2
        if image[half, half] > 100:
            return True
        else:
            return False

    def displayImagePassFailValues(self, results):
        pass_fail_values = {}
        total_fail = 0
        if results["Gearbox"] == 0:
            results["Gearbox"] = 1
        else:
            results["Gearbox"] = 0
        for part_key in ["Large Gear", "Small Gear", "Top Casing", "Bottom Casing"]:
            if results[part_key] == 0 and total_fail < 2:
                pass_fail_values[part_key] = ["FAIL", (0, 0, 255)]
                total_fail += 1
            else:
                pass_fail_values[part_key] = ["PASS", (0, 255, 0)]
        return pass_fail_values

    def displayImageProcessor(self, arguments):
        inputs = arguments.get()
        image = inputs[0]
        results_cache = inputs[1]
        gearbox_result = inputs[2]
        inspection_time = inputs[3]
        number = inputs[4]
        results_cache["Gearbox"] = gearbox_result
        vals = self.displayImagePassFailValues(results_cache)

        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        image = cv2.putText(image, vals["Bottom Casing"][0], (100, 250), cv2.FONT_HERSHEY_SIMPLEX, 
                   4, vals["Bottom Casing"][1], 10, cv2.LINE_AA)
        image = cv2.putText(image, vals["Top Casing"][0], (100, 1400), cv2.FONT_HERSHEY_SIMPLEX, 
                   4, vals["Top Casing"][1], 10, cv2.LINE_AA)
        image = cv2.putText(image, vals["Large Gear"][0], (1250, 250), cv2.FONT_HERSHEY_SIMPLEX, 
                   4, vals["Large Gear"][1], 10, cv2.LINE_AA)
        image = cv2.putText(image, vals["Small Gear"][0], (1350, 1000), cv2.FONT_HERSHEY_SIMPLEX, 
                   4, vals["Small Gear"][1], 10, cv2.LINE_AA)
        image = cv2.putText(image, 'Gearbox:', (1400, 1500), cv2.FONT_HERSHEY_SIMPLEX, 
                   4, (255, 255, 0), 10, cv2.LINE_AA)
        image = cv2.putText(image, vals["Gearbox"][0], (2000, 1500), cv2.FONT_HERSHEY_SIMPLEX, 
                   4, vals["Gearbox"][1], 10, cv2.LINE_AA)
        image = cv2.putText(image, 'Time: ', (1400, 1650), cv2.FONT_HERSHEY_SIMPLEX, 
                   4, (255, 255, 0), 10, cv2.LINE_AA)
        image = cv2.putText(image, f'{inspection_time:.0f}ms', (2000, 1650), cv2.FONT_HERSHEY_SIMPLEX, 
                   4, (0, 255, 255), 10, cv2.LINE_AA)
        image = cv2.putText(image, 'Number: ', (1400, 1800), cv2.FONT_HERSHEY_SIMPLEX, 
                   4, (255, 255, 0), 10, cv2.LINE_AA)
        image = cv2.putText(image, f'{number}', (2000, 1800), cv2.FONT_HERSHEY_SIMPLEX, 
                   4, (255, 0, 255), 10, cv2.LINE_AA)
        cv2.imwrite("images/live/99.jpg", image)

class Contours:
    def getContourByArea(image, minArea = -float('Inf'), maxArea = float('Inf')):
        contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        outer_contour = None
        getArea = cv2.contourArea

        for contour in contours:
            area = getArea(contour)
            if minArea < area < maxArea:
                outer_contour = contour
                break

        return outer_contour
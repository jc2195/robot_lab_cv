from ..models.gearbox_model import Gearbox
from ..helpers.hardware import Camera
from ..helpers.cv import ImageManipulation
from ..helpers.network import S3, Database
from dotenv import load_dotenv
from multiprocessing import Queue
from multiprocessing.pool import ThreadPool
import cv2
import time
import os

class InspectionProcedure:
    def __init__(self):
        load_dotenv()
        self.inspection_number = 0
        self.gearbox = Gearbox()
        self.s3 = S3()
        self.db = Database()
        self.image_manipulation = ImageManipulation()
        self.camera = Camera()
        # self.image = cv2.imread("experiments/blank_1.jpg", cv2.IMREAD_GRAYSCALE)
        # self.image = self.image[0:2350, 0:2500]
        self.epochtime = None
        self.inspection_time = None
        self.pool = ThreadPool(3)
        self.display_image_queue = Queue()
        self.s3_queue = Queue()
        self.db_queue = Queue()
        self.display_image_result = None
        self.s3_result = None
        self.db_result = None
        self.result_cache = {
            "Top Casing": 0,
            "Bottom Casing": 0,
            "Small Gear": 0,
            "Large Gear": 0
        }

    def writeToS3(self, arguments):
        self.s3.writeImage(arguments)

    def writeToDb(self, arguments):
        self.db.write(arguments)

    def takePicture(self):
        self.epochtime = time.time()
        self.camera.takePicture()

    def uploadImage(self):
        self.s3_queue.put([self.camera.image_trimmed, self.epochtime])
        self.s3_result = self.pool.map_async(func=self.writeToS3, iterable=[self.s3_queue])

    def uploadData(self):
        self.db_queue.put(self.retrieveSqlData())
        self.db_result = self.pool.map_async(func=self.writeToDb, iterable=[self.db_queue])

    def upload(self):
        self.uploadImage()
        self.uploadData()

    def writeDisplayImage(self, arguments):
        self.image_manipulation.displayImageProcessor(arguments)

    def outputDisplayImage(self):
        self.display_image_queue.put([self.camera.image_trimmed, self.gearbox.passing_parts, self.gearbox.status["code"], self.inspection_time, self.inspection_number])
        self.display_image_result = self.pool.map_async(func=self.writeDisplayImage, iterable=[self.display_image_queue])

    def consoleLog(self):
        print("\033[4m" + "Running:" + "\033[0m" + "\033[94m" + " " + f"{self.epochtime}" + "\033[0m")
        self.gearbox.report()
        print("\033[1m" + "Runtime: " + "\033[0m" + "\033[93m" + f"{self.inspection_time:.3f}" + " ms" + "\033[0m")
        print("\n")

    def updateResultsCache(self):
        for key in self.gearbox.passing_parts:
            if self.gearbox.passing_parts[key] == 0:
                self.result_cache[key] += 1

    def inspect(self):
        print("\033[4m" + "Running:" + "\033[0m" + "\033[94m" + " " + f"{self.epochtime}" + "\033[0m")
        self.inspection_number += 1
        print("\033[4m" + "Number:" + "\033[0m" + "\033[94m" + " " + f"{self.inspection_number}" + "\033[0m")
        self.gearbox.inspect(self.camera.image_trimmed)
        self.inspection_time = (time.time() - self.epochtime) * 1000
        print("\033[1m" + "Runtime: " + "\033[0m" + "\033[93m" + f"{self.inspection_time:.3f}" + " ms" + "\033[0m")
        print("\n")
        self.updateResultsCache()
        self.outputDisplayImage()
        return self.retrieveValidationVector(self.gearbox.passing_parts)

    def retrieveSqlData(self):
        return (self.epochtime, self.gearbox.status["code"], self.gearbox.components["Top Casing"].status["code"], 
        self.gearbox.components["Bottom Casing"].status["code"], self.gearbox.components["Large Gear"].status["code"], self.gearbox.components["Small Gear"].status["code"], 
        self.gearbox.components["Top Casing"].hole_diameters["left"], self.gearbox.components["Top Casing"].hole_diameters["right"], 
        self.gearbox.components["Bottom Casing"].hole_diameters["left"], self.gearbox.components["Bottom Casing"].hole_diameters["right"], 
        self.inspection_time, f'https://{os.environ["S3_BUCKET_NAME"]}.s3.{os.environ["AWS_REGION_NAME"]}.amazonaws.com/{str(int(self.epochtime * 100000000))}.jpg',)

    def retrieveValidationVector(self, report):
        output = [1, 1, 1, 1]
        total_failing = 0
        if report["Large Gear"] == 0:
            if total_failing < 2:
                output[3] = 0
                total_failing += 1
        if report["Small Gear"] == 0:
            if total_failing < 2:
                output[2] = 0
                total_failing += 1
        if report["Top Casing"] == 0:
            if total_failing < 2:
                output[0] = 0
                total_failing += 1
        if report["Bottom Casing"] == 0:
            if total_failing < 2:
                output[1] = 0
                total_failing += 1
        return output

# inspection_procedure = InspectionProcedure()
# counter = 0
# total = 0
# for i in range(9):
#     print("\n")
#     start = time.time()
#     inspection_procedure.takePicture()
#     inspection_procedure.image = cv2.imread(f"images/live/{counter}.jpg", cv2.IMREAD_GRAYSCALE)
#     inspection_procedure.image = inspection_procedure.image[0:2350, 0:2500]
#     inspection_procedure.inspect()
#     # cv2.imwrite("images/live/99.jpg", inspection_procedure.image)
#     total += time.time() - start
#     # inspection_procedure.upload()
#     time.sleep(2)
#     counter += 1
# print(total/9)
from ..models.gearbox_model import Gearbox
from ..helpers.hardware import Camera
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
        self.gearbox = Gearbox()
        self.s3 = S3()
        self.db = Database()
        self.camera = Camera()
        # self.image = cv2.imread("experiments/166930071242325536.jpg", cv2.IMREAD_GRAYSCALE)
        # self.image = cv2.cvtColor(self.image, cv2.COLOR_RGB2YUV)
        # self.image = self.image[0:2350, 0:1760, 0]
        self.epochtime = None
        self.inspection_time = None
        self.pool = ThreadPool(2)
        self.s3_queue = Queue()
        self.db_queue = Queue()
        self.s3_result = None
        self.db_result = None

    def writeToS3(self, arguments):
        self.s3.writeImage(arguments)

    def writeToDb(self, arguments):
        self.db.write(arguments)

    def takePicture(self):
        self.epochtime = time.time()
        self.camera.takePicture()

    def uploadImage(self):
        self.s3_queue.put([self.image, self.epochtime])
        self.s3_result = self.pool.map_async(func=self.writeToS3, iterable=[self.s3_queue])

    def uploadData(self):
        self.db_queue.put(self.retrieveSqlData())
        self.db_result = self.pool.map_async(func=self.writeToDb, iterable=[self.db_queue])

    def upload(self):
        self.uploadImage()
        self.uploadData()

    def consoleLog(self):
        print("\033[4m" + "Running:" + "\033[0m" + "\033[94m" + " " + f"{self.epochtime}" + "\033[0m")
        self.gearbox.report()
        print("\033[1m" + "Runtime: " + "\033[0m" + "\033[93m" + f"{self.inspection_time:.3f}" + " ms" + "\033[0m")
        print("\n")

    def inspect(self):
        print("\033[4m" + "Running:" + "\033[0m" + "\033[94m" + " " + f"{self.epochtime}" + "\033[0m")
        self.gearbox.inspect(self.image)
        self.inspection_time = (time.time() - self.epochtime) * 1000
        print("\033[1m" + "Runtime: " + "\033[0m" + "\033[93m" + f"{self.inspection_time:.3f}" + " ms" + "\033[0m")
        print("\n")
        return self.retrieveValidationVector(self.gearbox.passing_parts)

    def retrieveSqlData(self):
        return (self.epochtime, self.gearbox.status["code"], self.gearbox.components["Top Casing"].status["code"], 
        self.gearbox.components["Bottom Casing"].status["code"], self.gearbox.components["Large Gear"].status["code"], self.gearbox.components["Small Gear"].status["code"], 
        self.gearbox.components["Top Casing"].hole_diameters["left"], self.gearbox.components["Top Casing"].hole_diameters["right"], 
        self.gearbox.components["Bottom Casing"].hole_diameters["left"], self.gearbox.components["Bottom Casing"].hole_diameters["right"], 
        self.inspection_time, f'https://{os.environ["S3_BUCKET_NAME"]}.s3.{os.environ["AWS_REGION_NAME"]}.amazonaws.com/{str(int(self.epochtime * 100000000))}.jpg',)

    def retrieveValidationVector(self, report):
        output = []
        output.append(report["Top Casing"])
        output.append(report["Bottom Casing"])
        output.append(report["Small Gear"])
        output.append(report["Large Gear"])
        return output

# inspection_procedure = InspectionProcedure()
# total = 0
# for i in range(5):
#     print("\n")
#     start = time.time()
#     inspection_procedure.takePicture()
#     inspection_procedure.inspect()
#     total += time.time() - start
#     inspection_procedure.upload()
#     time.sleep(1)
# print(total/5)
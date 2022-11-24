import numpy as np
import boto3
import os
import cv2
import MySQLdb

class S3:
    def __init__(self):
        self.session = boto3.Session(
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
            region_name=os.environ["AWS_REGION_NAME"]
        )
        self.resource = self.session.resource('s3')

    def writeImage(self, queue):
        arguments = queue.get()
        image = arguments[0]
        filename = arguments[1]
        image = np.array(image)
        data_serial = cv2.imencode('.jpg', image)[1].tobytes()
        try:
            response = self.resource.Object(os.environ["S3_BUCKET_NAME"], str(int(filename * 100000000)) + ".jpg").put(Body=data_serial, ContentType="image/JPG", ACL='public-read')
            print(f"{filename} written S3")
        except ClientError as e:
            logging.error(e)
            return False
        return True

class Database:
    def __init__(self):
        try:
            self.db = MySQLdb.connect(host=os.environ["RDS_ENDPOINT"], port=int(os.environ["RDS_PORT"]), user=os.environ["RDS_USERNAME"], passwd=os.environ["RDS_PASSWORD"], db=os.environ["RDS_DATABASE"])
            self.cursor = self.db.cursor()
        except Exception as e:
            print("FATAL DB CONNECTION ERROR")
            print(e)

    def write(self, queue):
        sql_data = queue.get()
        sql_string = f"""INSERT INTO {os.environ["RDS_TABLE"]} 
        (local_inspection_time_start, gearbox_code, top_casing_code, 
        bottom_casing_code, large_gear_code, small_gear_code, 
        top_casing_left_hole_diameter, top_casing_right_hole_diameter,
        bottom_casing_left_hole_diameter, bottom_casing_right_hole_diameter,
        total_inspection_time, gearbox_image) VALUES 
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        try:
            self.cursor.execute(sql_string, sql_data)
            self.db.commit()
            print(f"{sql_data[0]} written DB")
        except Exception as e:
            print("UNABLE TO WRITE DATA TO DB")
            print(e)
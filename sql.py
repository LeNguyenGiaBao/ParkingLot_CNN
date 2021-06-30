import mysql.connector
from mysql.connector import Error
import numpy as np
import cv2
# from datetime import datetime
def connect():
        connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678",
        database="baixe"
        )
        return connection

# connection =connect()
# cursor = connection.cursor()
# cursor.execute("CREATE DATABASE baixe;")
# cursor.execute("USE baixe;")
# cursor.execute("CREATE TABLE bang (id INT NOT NULL AUTO_INCREMENT, mssv VARCHAR(50) NULL, bienso VARCHAR(50) NULL, trangthai BIT NULL, thoigianthue DATETIME NULL, thoigiantra DATETIME NULL, anh MEDIUMBLOB NULL, PRIMARY KEY (id))")


def insert_data(mssv,bienso,img):
        try:
                connection =connect()
                cursor = connection.cursor()
                sql = "INSERT INTO bang (mssv,bienso,trangthai,thoigianthue,anh) values (%s,%s,0,CURRENT_TIMESTAMP,%s)"
                import cv2
                success, encoded_image = cv2.imencode('.jpg', img)
                content2 = encoded_image.tobytes()
                val = (mssv,bienso,content2)
                cursor.execute(sql, val)
                connection.commit()
                # print(cursor.rowcount, "record(s) affected")
                
        except mysql.connector.Error as error:
                        print("loi {}".format(error))

        finally:
                if (connection.is_connected()):
                        cursor.close()
                        connection.close()
                        # print("MySQL connection is closed")
		
        #return cursor.lastrowid
def update_data(mssv):
        try:
                connection =connect()
                cursor = connection.cursor()
                sql = "UPDATE bang SET trangthai = %s,thoigiantra=CURRENT_TIMESTAMP WHERE mssv = %s and trangthai=0 "
                val = (1,mssv)
                cursor.execute(sql, val)
                connection.commit()
                # print(cursor.rowcount, "record(s) affected")
        except mysql.connector.Error as error:
                        print("loi {}".format(error))

        finally:
                if (connection.is_connected()):
                        cursor.close()
                        connection.close()
                        # print("MySQL connection is closed")
def delete_data(id):
        try:
                connection =connect()
                cursor = connection.cursor()
                sql = "DELETE FROM bang WHERE id = %s"
                val = (id)
                cursor.execute(sql, val)
                connection.commit()
                # print(cursor.rowcount, "record(s) affected")
        except mysql.connector.Error as error:
                        print("loi {}".format(error))

        finally:
                if (connection.is_connected()):
                        cursor.close()
                        connection.close()
                        # print("MySQL connection is closed")
def get_all_data():
        try:
                connection =connect()
                cursor = connection.cursor()
                sql = "SELECT * FROM bang "
                cursor.execute(sql)
                myresult = cursor.fetchall()
                return myresult
        except mysql.connector.Error as error:
                        print("loi {}".format(error))

        finally:
                if (connection.is_connected()):
                        cursor.close()
                        connection.close()
                        # print("MySQL connection is closed")
def get_by_mssv(mssv):
        try:
                connection =connect()
                cursor = connection.cursor()
                sql = "SELECT * FROM bang WHERE mssv = %s and trangthai=0 "
                adr = (mssv, )
                cursor.execute(sql, adr)
                myresult = cursor.fetchall()
                return myresult
        except mysql.connector.Error as error:
                        print("loi {}".format(error))

        finally:
                if (connection.is_connected()):
                        cursor.close()
                        connection.close()
                        # print("MySQL connection is closed")



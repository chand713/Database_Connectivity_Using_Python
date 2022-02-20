import os
import pathlib
import tkinter
from datetime import datetime
from tkinter import filedialog

import PyPDF2
import mysql.connector
import pandas
from mysql.connector import errorcode

directory = tkinter.filedialog.askdirectory()
files= os.listdir(directory)
print(list(files))
for pdf_files in files:
    fileext = pathlib.Path(pdf_files).suffix
    if fileext == ".pdf":
        inputpdf = PyPDF2.PdfFileReader(pdf_files)
        if inputpdf.isEncrypted:
            print(pdf_files,"is Encrypted")
            continue
        pages_no = inputpdf.numPages
        enc_file_name = datetime.now().strftime("%Y_%b_%d_%H_%M_%S") + '.pdf'  # creating a filename for encrypted one
        print(pages_no)
        output = PyPDF2.PdfFileWriter()
        password = input("Enter your password")
        for i in range(pages_no):
            input_pdf = PyPDF2.PdfFileReader(pdf_files)

            output.addPage(inputpdf.getPage(i))
            output.encrypt(password)

        with open(enc_file_name, "wb") as outputStream:
            output.write(outputStream)

        size = round((os.path.getsize(pdf_files)) / 1024 ** 2,2)

        print(enc_file_name)
        print(size)
        modified_time = datetime.now().strftime("%Y/%b/%d %H:%M:%S")
        print(modified_time)
        if os.path.exists('file_data.csv') == True:
            my_data = {"FileName": [enc_file_name], "Size": [size], "DateModified": [modified_time]}
            my_csv_data = pandas.DataFrame(my_data)
            my_csv_data.to_csv('file_data.csv', mode='a', index=None, header=False)
        else:
            my_data = {"FileName": [enc_file_name], "Size": [size], "DateModified": [modified_time]}
            my_csv_data = pandas.DataFrame(my_data)
            my_csv_data.to_csv('file_data.csv', index=None)

#         db operation
        print(enc_file_name)
        print(type(enc_file_name))
        print(size)
        print(type(size))
        print(modified_time)
        print(type(modified_time))

        try:

            connection = mysql.connector.connect(user="dhoni", password="dhoni07", host="localhost", port=3306,
                                                 database="demo1")
            query = """create table if not exists file_data2 (File_Name varchar(200) , size float(20,2),Date_Modified varchar(200),password varchar(20))"""
            insert_query = """insert into file_data2 values(%s,%s,%s,%s)"""
            val = [(enc_file_name,size,modified_time,password)]
            mycursor = connection.cursor()
            mycursor.execute(query)
            mycursor.executemany(insert_query,val)
            print("connected")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
                print(err)
            elif err.errno == errorcode.ER_NO_SUCH_TABLE:
                print("No such table exists in database")

            else:
                print(err)
        finally:
            connection.commit()
            connection.close()
            print("connection was closed")










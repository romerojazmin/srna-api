# Import here the corresponding headers
from flask import Response
from flask import json
from flask import send_file
import io
import os
from sys import platform
from werkzeug import secure_filename
from datetime import datetime

class fileSystem_Provider:

    def create_folder(self, path, folder):
        fullpath = os.path.join(path, folder)
        if not os.path.exists(fullpath):
            os.makedirs(fullpath)


    def create_folder_fullpath(self, folder):
        if not os.path.exists(folder):
            os.makedirs(folder)


    def upload_file(self, folder, file, name):
        if file and name:
            #path = 'srna-data/input_files'
            filename = secure_filename(name)
            if not os.path.exists(folder):
                os.makedirs(folder)
            fullpath = os.path.join(folder, filename)
            file.save(fullpath)
            return fullpath

    def download_file(self, folder , filename):
        filename = filename + '.xlsx'
        fullpath = folder + filename
        if os.path.exists(fullpath):
            with open(fullpath, 'rb') as binary:
                return send_file(
                    io.BytesIO(binary.read()),
                    attachment_filename=filename,
                    as_attachment=True,
                    mimetype="application/binary")

        error = {"message": "File does not exist"}
        return Response(json.dumps(error), 404, mimetype="application/json")

    def remove_file(self,filename):
        if os.path.exists(filename):
            os.remove(filename)

    def remove_files_with_prefix(self, path, prefix):
        for file in os.listdir(path):
            if file.startswith(prefix):
                print(file)
                filename = path + file
                self.remove_file(filename)
        print ('done')
        return


    def remove_files_in_folder(self, folder):
        for file in os.listdir(folder):
            filename = folder + file
            self.remove_file(filename)
        return



    def remove_folder(self, folder):
        if os.path.exists(folder):
            os.rmdir(folder)


    def remove_files_old_days(self, folder, days):
        for subfolder in os.listdir(folder):
            if not subfolder.startswith('.'):
                subfolder_path = os.path.join(folder, subfolder)
                #Remove files older than days
                for file in os.listdir(subfolder_path):
                    file_path = os.path.join(subfolder_path, file)
                    if os.path.isfile(file_path):
                        #print(file)
                        file_created_datetime = os.stat(file_path).st_birthtime
                        current_datetime = datetime.timestamp(datetime.now())
                        dif = current_datetime - file_created_datetime   #Dif in seconds between two days
                        #86400 = Number of secs in 1 day
                        old_days = dif / 86400
                        #print(old_days)
                        if old_days>=days:
                            try:
                                os.remove(file_path)
                                #print ('File removed')
                            except OSError as e:
                                print("Error: %s : %s" % (file_path, e.strerror))
                #Remove subfolder if empty
                try:
                    print (subfolder_path)
                    if not os.listdir(subfolder_path):
                        os.rmdir(subfolder_path)
                        #print ('Subfolder Removed')
                except OSError as e:
                    print("Error: %s : %s" % (file_path, e.strerror))




    def remove_file_older_than(self, filepath, days):
        if os.path.isfile(filepath):
            if days>0:
                if platform == "linux" or platform == "linux2":
                    file_created_datetime = os.stat(filepath).st_ctime
                elif platform == "darwin":
                    file_created_datetime = os.stat(filepath).st_birthtime
                current_datetime = datetime.timestamp(datetime.now())
                dif = current_datetime - file_created_datetime  # Dif in seconds between two days
                # 86400 = Number of secs in 1 day
                old_days = dif / 86400
                # print(old_days)
                if old_days >= days:
                    try:
                        os.remove(filepath)
                        # print ('File removed')
                    except OSError as e:
                        print("Error: %s : %s" % (filepath, e.strerror))
            else:
                self.remove_file(filepath)



    def clean_history(self, folder, remove_folder, days=None):
        try:
            if not os.path.exists(folder):
                return

            if not days:
                days=0

            for path in os.listdir(folder):
                if not path.startswith('.'):
                    #It is directory (folder)
                    fullpath = os.path.join(folder, path)
                    if os.path.isdir(fullpath):
                        #Remove files older than days
                        for file in os.listdir(fullpath):
                            filepath = os.path.join(fullpath, file)
                            self.remove_file_older_than(filepath, days)
                        #Remove subfolder -if empty
                        try:
                            #print (fullpath)
                            if not os.listdir(fullpath):
                                os.rmdir(fullpath)
                                #print ('Subfolder Removed')
                        except OSError as e:
                            print("Error: %s : %s" % (fullpath, e.strerror))

                    if os.path.isfile(fullpath):
                        self.remove_file_older_than(fullpath, days)

            if remove_folder:
                self.remove_folder(folder)
        except OSError as e:
            print("Error: %s : %s" % (folder, e.strerror))


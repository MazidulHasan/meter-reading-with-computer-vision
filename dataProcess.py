import pyrebase
import zipfile
import os
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
from combineAll import print_all_digits
from csvWork.sendCsvToFirebase import uploadCSVToFirebae

def processDataWithZipFileName(zipFileName):
    config = {
        "apiKey": "AIzaSyCw9nBF4EMtkM3FpK2ONtOdmkRFQjpp-3U",
        "authDomain": "computervision-f3825.firebaseapp.com",
        "databaseURL": "https://computervision-f3825-default-rtdb.firebaseio.com/",
        "projectId": "computervision-f3825",
        "storageBucket": "computervision-f3825.appspot.com",
        "messagingSenderId": "811571419343",
        "appId": "1:811571419343:web:a41770b10d5c521db7ffba",
        "measurementId": "G-921FTZZHHR"
    }

    firebase = pyrebase.initialize_app(config)
    storage = firebase.storage()

    fireFolderName = "FRDC"
    fireFileName = zipFileName

    try:
        # storage.child("FRDC/2023-12-06_18:14.zip").download("/","zipData.zip")
        storage.child("FRDC/"+zipFileName).download("/","zipData.zip")
        print(f"File '{fireFileName}' downloaded successfully")
    except Exception as e:
        print(f"Error downloading file '{fireFileName}': {e}")


    def extract_zip(zip_file_path, extract_to_folder):
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to_folder)

    def print_for_all_files(folder_path):
        files = os.listdir(folder_path)
        for file_name in files:
            print(file_name)
            print_all_digits(file_name)

    zip_file_path = "zipData.zip"
    extract_to_folder = 'unzip'

    # extract_zip(zip_file_path, extract_to_folder)
    print_for_all_files(extract_to_folder)

    uploadCSVToFirebae()
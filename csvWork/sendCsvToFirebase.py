import pyrebase

def uploadCSVToFirebae():
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
    storage_folder = "CSVFiles/"
    localcsv_file_path = 'csvWork/allData.csv'

    # Upload the CSV file to the Firebase storage folder
    storage.child(storage_folder + 'allData.csv').put(localcsv_file_path)

from flask import Flask, render_template , request
import csv
from dataProcess import processDataWithZipFileName

app = Flask(__name__)

@app.route('/')
def index():
    # Read data from CSV file
    csv_file_path = 'csvWork/allData.csv'
    data = read_csv(csv_file_path)

    return render_template('index.html', data=data)

def read_csv(file_path):
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = list(csv_reader)
    return data


# Data processing form raspberry pi request
@app.route('/process_data', methods=['POST'])
def process_data():
    file_name = request.json.get('file_name')

    # Call the function to process data based on the file name
    print("File name is "+file_name)
    processDataWithZipFileName(file_name)
    return 'Data processing initiated.'

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)

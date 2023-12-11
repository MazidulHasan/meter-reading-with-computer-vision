import csv

def saveAsCSVFile(imageName,imageValue):
    data = [
        (imageName, imageValue)
    ]

    # Write data to CSV file
    with open('csvWork/allData.csv', 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(data)

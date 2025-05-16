import requests
from bs4 import BeautifulSoup as ak
# Base URL to check result
base_url = "http://school.sanjivanicollege.com/OnlineResult/Result_XI_XII_Prnt_I.aspx"

# Headers to mimic browser
headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36"
}

import json
import csv

def create_person_files(name, father_name, mobile_no, mother_name, dob,address):
    # Create a dictionary with the person details
    person_details = {
        "name": name,
        "father_name": father_name,
        "mother_name": mother_name,
        "mobile_no": mobile_no,
        "dob": dob,
        "address": address
    }

    # Create and write the data to a JSON file
    with open('storage/shared/person_details.json', 'a') as json_file:
        json.dump(person_details, json_file, indent=4)

    # Create and write the data to a CSV file
    with open('storage/shared/person_details.csv', 'a', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=person_details.keys())
#        writer.writeheader()
        writer.writerow(person_details)

# Define roll number range
start_roll = int(input("Starting Roll no:- "))
end_roll = int(input("End Roll number:- "))

print(f"Checking roll numbers from {start_roll} to {end_roll}...\n")
n=1
for roll_no in range(start_roll, end_roll + 1):
    # Build URL with dynamic roll number
    params = {
        "RollNo": roll_no,
        "Class": "11",
        "Year": "12"
    }

    try:
        # Send GET request
        response = requests.get(base_url, headers=headers, params=params, timeout=10)

        # Check for the error message
        if "No result found" not in response.text:
            soup = ak(response.content,"html.parser")
            father=soup.find("span",id="fatherNameLabel").text
            mother = soup.find("span",id="motherNameLabel").text
            mobile = soup.find("span",id="telephoneLabel").text
            address = soup.find("span",id="residentAddressLabel").text
            dob = soup.find("span",id="dobLabel").text
            name = soup.find("span",id="nameLabel").text
            print(f"({n}).......[VALID RESULT] Found result for Roll No: {roll_no} \n Name:- {name}\n")
#            file(name,roll_no,response.url)
            create_person_files(name,father,mobile,mother,dob,address)
            n+=1
        #else:
         #   print(f"{roll_no} :- Not found")
    except requests.exceptions.RequestException as e:
        print(f"[Error] Roll No: {roll_no} -> {str(e)}")

print("complete")

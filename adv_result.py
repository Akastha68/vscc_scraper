import requests
from bs4 import BeautifulSoup as ak

# Target URL
base_url = "http://school.sanjivanicollege.com/OnlineResult/Result_XI_XII_Prnt_I.aspx"

# Headers to mimic browser
headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36"
}

def save_result(name, roll, link):
    with open("file1.txt", "a") as f:
        f.write(f"//Result Scraped By ShadowCoder//\nName :- {name}\nRoll no:- {roll}\nResult:- {link}\n\n")

n = 1

print("Starting result scraping for students admitted from 2015 to 2024...\n")
m=2
for year in range(15, 25):  # Admission years: 2015 to 2024
    for roll in range(1, 115):  # Roll numbers: 001 to 999
        roll_str = str(roll).zfill(3)
        classes = str(m).zfill(2)
        roll_no = f"{year}{classes}{roll_str}"  # Constructed Roll No like 2209001

        params = {
            "RollNo": roll_no,
            "Class": "11",   # Class in which result is to be fetched
            "Year": "12"     # Appeared year maybe?
        }

        try:
            response = requests.get(base_url, headers=headers, params=params, timeout=10)
            if "No result found" not in response.text:
                soup = ak(response.content, "html.parser")
                name = soup.find("span", id="nameLabel").text.strip()
                print(f"({n}) [VALID] Roll No: {roll_no} | Name: {name}")
                save_result(name, roll_no, response.url)
                n += 1
        except requests.exceptions.RequestException as e:
            print(f"[Error] Roll No: {roll_no} -> {str(e)}")
    m += 1
print("Scraping complete.")

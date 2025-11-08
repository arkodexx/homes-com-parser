from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import csv

options = Options()
user =  UserAgent().random
options.add_argument(f"--user-agent={user}")
options.add_argument("--headless")

service = Service(executable_path=GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=options)

houses = []
def getting_info(pagenation):
    counter = 0
    for i in range(pagenation):
        counter += 1
        driver.get(f"https://www.homes.com/los-angeles-ca/p{i}/")
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(("class name", "price-container"))
        )
        cards = driver.find_elements("class name", "placard-container")
        for i in cards:
            try:
                address = i.find_element("xpath", "article/div[3]/a").get_attribute("title")
            except Exception:
                address = ""
            try:
                price = i.find_element("class name", "price-container").text
            except Exception:
                price = ""
            try:
                info = i.find_element("class name", "detailed-info-container").text.replace("\n", " ")
            except Exception:
                info = ""
            try:
                agent_name = i.find_element("class name", "agent-name").text
            except Exception:
                agent_name = ""
            try:
                agency_name = i.find_element("class name", "agency-name").text
            except Exception:
                agency_name = ""
            try:
                agency_number = i.find_element("class name", "agency-number").text
            except Exception:
                agency_number = ""
            try:
                link = i.find_element("xpath", "article/div[3]/a").get_attribute("href")
            except Exception:
                link = ""
            houses.append({
                "Address": address,
                "Price": price,
                "Info": info,
                "Agent name": agent_name,
                "Agency name": agency_name,
                "Agency number": agency_number,
                "Link": link,
            })
        print(f"Succesfully parsed page №{counter}")
        
def saving_info(info):
    with open("houses.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Address", "Price", "Info", "Agent name", "Agency name", "Agency number", "Link"])
        for i in houses:
            writer.writerow([i["Address"],i["Price"], i["Info"], i["Agent name"], i["Agency name"], i["Agency number"], i["Link"]])

def parser():
    pagen = int(input("How much pages you want to parse?: "))
    getting_info(pagen)
    saving_info(houses)
    print("Succesfully saved into to a houses.csv file!")
    driver.close()

parser()
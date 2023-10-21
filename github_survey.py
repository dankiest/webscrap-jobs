from bs4 import BeautifulSoup
import re
import pandas as pd
import os 

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

url = "https://madnight.github.io/githut/#/{action}/{year}/{quarter}"

## Setup chrome options
chrome_options = Options()
chrome_options.add_argument("--headless") # Ensure GUI is off
#chrome_options.add_argument("")

# Set path to chromedriver as per your configuration
homedir = os.path.expanduser("~")
print(f"{homedir}/chromedriver/stable/chromedriver")
webdriver_service = Service(f"{homedir}/chromedriver/stable/chromedriver")

# Choose Chrome Browser
browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)
def request_survey(action, year, quarter):
    browser.get(url.format(action=action, year=year, quarter=quarter))
    site = BeautifulSoup(browser.page_source, "html.parser")
    if site:
        rows = []
        for tr in site.find("div", class_="react-bs-container-body").find('table').find_all('tr'):
            row = [year, quarter, action]
            row.extend([v.text.replace('\xa0','') for v in tr.find_all('td') if v.text])
            rows.append(row)
        return rows
    

if __name__ == '__main__':
    ds = []
    years = range(2013, 2024)
    quarters = range(1,5)
    actions = ['pull_requests', 'pushes', 'stars', 'issues']

    for year in years:
        for quarter in quarters:
            for action in actions:
                ds.extend(request_survey(action, year, quarter))

    df = pd.DataFrame(ds, columns=['year', 'quarter', 'action', 'ranking', 'language', 'percent'])
    df.to_csv("github_survey.csv", index=False)

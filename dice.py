import requests
from bs4 import BeautifulSoup
import csv
import time
import httpx
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


# language = 'python'
# pages = 2
search_timeout = 0.1


# base_url = 'https://www.dice.com'
# search_url = f'/jobs?q={language}&vjk=1111'

# print(base_url + search_url)

response = requests.get('https://www.dice.com/jobs?q=java&location=Europe')

print(response.status_code)

if response.status_code == 200:

    soup = BeautifulSoup(response.text, 'html.parser')

    # print(soup)

    # chrome_options = Options()
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome()

    driver.get('https://www.dice.com/jobs?q=java&location=Europe')
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'dhi-search-card')))

    soup = BeautifulSoup(driver.page_source, "html.parser")

    titles_element = soup.find_all('dhi-search-card')

    for el in titles_element:
        link = f"https://www.dice.com/job-detail/{el.find('a')['id']}"

        job = {
            'title': '',
            'date-posted': '',
            'date-updated': '',
            'company': '',
            'work-mode': '',
            'travel-required': '',
            'contract-mode': '',
            'skills': '',
            'description': '',
            'id': '',
            'position-id': '',
            'compensation': '',
            'link': ''
        }

        time.sleep(search_timeout)
        # driver.get("https://www.dice.com/job-detail/77f82657-aff9-420c-b6e2-64c22519cc84?searchlink=search%2F%3Fq%3Djava%26location%3DEurope%26latitude%3D54.5259614%26longitude%3D15.2551187%26countryCode%3DUS%26locationPrecision%3DCity%26radius%3D30%26radiusUnit%3Dmi%26page%3D1%26pageSize%3D20%26language%3Den&searchId=19a234b4-550c-423a-8aca-da98b8570a09")
        # driver.get('https://www.dice.com/job-detail/a70373ae-d223-4b08-a265-90343dac1fc6?searchlink=search%2F%3Fq%3Djava%26location%3DEurope%26latitude%3D54.5259614%26longitude%3D15.2551187%26countryCode%3DUS%26locationPrecision%3DCity%26radius%3D30%26radiusUnit%3Dmi%26page%3D1%26pageSize%3D20%26language%3Den&searchId=2eff239e-8270-48f8-b8aa-0551a0e98cfa')
        driver.get(link)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        if 'No Longer Accepting Applications' in soup.text:
            job['description'] = 'No Longer Accepting Applications'
        else:
            wait = WebDriverWait(driver, 20)
            wait.until(EC.presence_of_element_located((By.ID, 'descriptionToggle')))

            button_element = driver.find_element(By.ID, 'descriptionToggle')

            if button_element:
                try:
                    button_element.click()
                except:
                    button_element.click()

            job['title'] = soup.find('h1', {'data-cy': 'jobTitle'}).text.strip()
            job['company'] = soup.find('a', { 'data-cy': 'companyNameLink'}).text
            job['work-mode'] = soup.find('li', { 'data-cy': 'companyLocation'}).text
            job['compensation'] = soup.find('p', { 'data-cy': 'compensationText'}).text
            job['contract-mode'] = soup.find('p', { 'data-cy': 'employmentType'}).text
            job['date-posted'] = soup.find('dhi-time-ago')['posted-date']

            skills_list = soup.find('ul', {'data-cy': 'skillsList'}).find_all('li')
            job['skills'] = ', '.join([a.text for a in skills_list])
            # job['description'] = soup.find(id='jobDescription').text
            job['id'] = soup.find('li', {'data-testid': 'legalInfo-companyName'}).text.split(':')[1].strip()
            job['position-id'] = soup.find('li', {'data-testid': 'legalInfo-referenceCode'}).text.split(':')[1].strip()

            if soup.find('li', {'data-cy': 'travelPercentage'}):
                job['travel-required'] = soup.find('li', {'data-cy': 'travelPercentage'}).text

            if soup.find('dhi-time-ago')['modified-date']:
                job['date-updated'] = soup.find('dhi-time-ago')['modified-date']
            
        print(job)

















driver.quit()
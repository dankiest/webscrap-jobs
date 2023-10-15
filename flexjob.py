import requests
from bs4 import BeautifulSoup
import csv
import time

language = 'python'
pages = 2
search_timeout = 0.1


base_url = 'https://www.flexjobs.com'
search_url = f'/search?search={language}&page='

jobs = []

print(f'iniciando scrap de jobs buscando por linguagem - {language} buscando até: {pages} paginas')

for page in range(1, pages + 1):
    
    print(f'page - {page} iniciada')

    response = requests.get(base_url + search_url + str(page))

    if response.status_code == 200:

        print('pagina obtida com sucesso')
        
        soup = BeautifulSoup(response.text, 'html.parser')

        pag_tag = soup.find('ul', {'class': "pagination"}).find_all('li')

        ul_tag = soup.find(id="job-list")

        li_items = ul_tag.find_all('li')

        print(f'{len(li_items)} jobs encontrados na pagina {page}')

        for li in li_items:

            job = {
                'id': li['data-job'],
                'title': li['data-title'],
                'url': base_url + li['data-url']
            }
            
            time.sleep(search_timeout)
            li_response = requests.get(base_url + li['data-url'])

            if li_response.status_code == 200:
                li_soup = BeautifulSoup(li_response.text, 'html.parser')

                job['description'] = li_soup.find('div', {"class": 'job-description'}).text

                table = li_soup.find('table', {"class": 'job-details'})
                table_contents = table.find_all('td')

                job['date-posted'] = table_contents[0].text.strip()
                job['work-mode'] = table_contents[1].text.strip()
                job['location'] = table_contents[2].text.strip()
                job['job-type'] = table_contents[3].text.strip()
                job['job-schedule'] = table_contents[4].text.strip()
                job['carrer-level'] = table_contents[5].text.strip()
                job['travel-required'] = table_contents[6].text.strip()

                a_tags = table_contents[7].find_all('a')
                job['categories'] = ', '.join([a.text for a in a_tags])

            jobs.append(job)

    else:
        print("Scrap faiô. Status code:", response.status_code)

    print(f'page - {page} terminada')


print(f'{len(jobs)} jobs encontrados no scrap')

print('iniciando criação de arquivo')

file_name = f'flexjob-{language}.csv'

with open(file_name, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=list(jobs[0].keys()))
    writer.writeheader()

    for row in jobs:
        writer.writerow(row)

print('arquivo criado com sucesso')
print('importação terminada')
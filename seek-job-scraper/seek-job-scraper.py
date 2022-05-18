import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

'''
job_url -> https://www.seek.com.au/job/56834934?type=promoted

'''


def create_url(page):
    base_url = 'https://www.seek.com.au/'
    page_url = base_url + f'data-analyst-jobs/in-All-Adelaide-SA?page={page}'
    return page_url


def get_page(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/101.0.4951.67 Safari/537.36'}
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup


def extract_job_url(soup):
    job_links = []
    base_url = 'https://www.seek.com.au/'
    jobs = soup.find_all('article', {'data-automation': ['normalJob', 'premiumJob']})

    for item in jobs:
        link = item.find('a', href=True)
        job_links.append(base_url + link['href'])
    return job_links




def get_all_job_links(page):
    job_links = []

    for i in range(1, page):
        page_url = create_url(i)
        page_soup = get_page(page_url)
        job_links.append(extract_job_url(page_soup))
        time.sleep(1)
        print(f'getting links from page {i}')
    return job_links


job_links = get_all_job_links(3)
job_links = [item for elem in job_links for item in elem]

df = pd.DataFrame(job_links, columns=['link'])
df.to_csv('data/job-links', index=False)



import requests
import lxml.html as lh
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from pathlib import Path

'''
job_url -> https://www.seek.com.au/job/56834934?type=promoted

'''


def create_url(keyword, location):
    base_url = 'https://www.seek.com.au/'
    return f'{base_url}{keyword}-jobs/in-{location}?page='


def get_page(url):
    r = session.get(url)
    return BeautifulSoup(r.content, 'html.parser')


def get_urls_in_page(soup):
    url_list = []
    base_url = 'https://www.seek.com.au/'
    jobs = soup.find_all('article', {'data-automation': ['normalJob', 'premiumJob']})

    for item in jobs:
        a = item.find('a', href=True)
        url_list.append(base_url + a['href'])
    return url_list


def get_all_job_urls(page):
    params = []
    for k in keywords:
        for l in location:
            params.append(
                {
                    'keyword': k,
                    'location': l
                }
            )

    page_urls = []
    for idx, val in enumerate(params):
        page_urls.append(create_url(val['keyword'].replace(' ', '-'), val['location'].replace(' ', '-')))

    links = []
    for url in page_urls:
        for i in range(1, page):
            page_url = f'{url}{i}'
            page_soup = get_page(page_url)
            links.append(get_urls_in_page(page_soup))
            # time.sleep(0.5)
            print(f'getting urls from page {i}')
    return links


def create_file(job_links):
    today = datetime.now().strftime("%Y-%m-%d")
    title = keywords[0].replace(" ", "-").lower()
    loc = location[0].replace(" ", "-").lower()

    file_name = f'{today}-{title}-jobs-in-{loc}.csv'
    file_path = Path('data', 'links', file_name)

    if file_path.exists():
        print("Replacing existing file! \n", file_name)
    else:
        print("Creating a new file.. \n", file_name)

    df = pd.DataFrame(job_links, columns=['link'])
    df.to_csv(file_path, index=False)


def main(pages):
    # flatten the 2D list
    job_links = [item for elem in get_all_job_urls(pages) for item in elem]
    print(f'{len(job_links)} jobs extracted...')

    create_file(job_links)


if __name__ == '__main__':
    session = requests.session()
    keywords = ['data analyst', 'data scientist']
    location = ['All Adelaide SA']
    main(30)

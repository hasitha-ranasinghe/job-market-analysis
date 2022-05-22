import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
from pathlib import Path


def get_page(url):
    r = session.get(url)
    return BeautifulSoup(r.content, 'html.parser')


def clean_posted_date(date):

    lst = re.split('(\d+)', date)
    symbol = lst[2]
    today = datetime.now()
    day = timedelta(days=int(lst[1]))

    if symbol in ['d', 'd+']:
        post_date = today - day
    elif symbol in ['h']:
        post_date = today
    else:
        post_date = today - timedelta(days=30)

    return post_date.strftime("%d/%m/%Y")


def extract_job_content(soup, url):
    # title and company
    title = soup.find('h1', {'data-automation': 'job-detail-title'}).text.strip()
    company = soup.find('span', {'data-automation': 'advertiser-name'}).text.strip()

    # location
    divs_location_classification = soup.find_all('div', class_='yvsb870 _14uh9944y o76g430')
    location = divs_location_classification[0].text.strip()
    classification = divs_location_classification[1].text.strip()
    sub_classification = divs_location_classification[2].text.strip()

    # salary and work-type
    if len(divs_location_classification) > 4:
        salary = divs_location_classification[3].text.strip()
        work_type = divs_location_classification[4].text.strip()
    else:
        salary = 0
        work_type = divs_location_classification[3].text.strip()

    # posted date
    date_div = soup.find_all('span', class_='yvsb870 _14uh9944u _1qw3t4i0 _1qw3t4i1y _1qw3t4i1 _1d0g9qk4 _1qw3t4ib')

    if len(date_div) > 1:
        date = date_div[1].text.split()[1]
    else:
        date = date_div[0].text.split()[1]

    # description
    tags_description = soup.find('div', class_='yvsb870 _1v38w810').prettify()

    job = {
        'title': title,
        'company': company,
        'location': location,
        'classification': classification,
        'sub_classification': sub_classification,
        'salary': salary,
        'work_type': work_type,
        'posted_date': clean_posted_date(date),
        'url': url,
        'description': tags_description
    }
    return job


def save_file(job_list, file_name):
    file_path = Path('data', 'content', file_name)
    if file_path.exists():
        print("\nReplacing existing file! \n", file_name)
    else:
        print("\nCreating a new file.. \n", file_name)

    df = pd.DataFrame(job_list)
    df.to_csv(file_path, index=False)


def main():
    job_list = []
    file_name = '2022-05-22-data-analyst-jobs-in-all-adelaide-sa.csv'
    links = pd.read_csv(f'data/links/{file_name}')
    links = links['link'].values.tolist()
    rejected = 0
    for idx, val in enumerate(links, start=1):
        try:
            soup = get_page(val)
            job_list.append(extract_job_content(soup, val))
            # time.sleep(0.5)
            print(f'job {idx} done')

        except Exception as e:
            print(f'Error: {e}')
            print(f'Error class: {e.__class__}')
            print(f'job link: {val}')
            rejected += 1
            continue

    save_file(job_list, file_name)

    print(f'\n--- Extraction summary --- \n'
          f'Extracted jobs: {len(links) - rejected}\n'
          f'Rejected jobs: {rejected}\n')


if __name__ == '__main__':
    session = requests.session()
    start = datetime.now()
    main()
    finish = datetime.now() - start
    print(f'time spent: {finish}')

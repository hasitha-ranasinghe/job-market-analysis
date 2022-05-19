import time
import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_page(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/101.0.4951.67 Safari/537.36'}
    r = requests.get(url, headers)
    return BeautifulSoup(r.content, 'html.parser')


def extract_job_content(soup):
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
        'posted_date': date,
        'description': tags_description
    }
    return job


def main():
    job_list = []
    links = pd.read_csv('data/job-links.csv')
    links = links['link'].values.tolist()
    for idx, val in enumerate(links, start=1):
        try:
            soup = get_page(val)
            job_list.append(extract_job_content(soup))
            # time.sleep(0.5)
            print(f'job {idx} done')

        except Exception as e:
            print(f'Error: {e}')
            print(f'Error class: {e.__class__}')
            print(f'job link: {val}')
            continue

    df = pd.DataFrame(job_list)
    df.to_csv('data/job-content.csv', index=False)
    print('file created')


if __name__ == '__main__':
    main()

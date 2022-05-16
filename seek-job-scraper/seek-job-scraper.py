import requests
from bs4 import BeautifulSoup

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


def extract_job_urls(soup):
    base_url = 'https://www.seek.com.au/'
    jobs = soup.find_all('article', {'data-automation': ['normalJob', 'premiumJob']})

    for item in jobs:
        link = item.find('a', href=True)
        job_links.append(base_url+link['href'])
    return job_links

# extract method for main pages
# def extract_page_content(soup):
#     jobs = soup.find_all('article', {'data-automation': ['normalJob', 'premiumJob']})
#     print(len(jobs))
#
#     for item in jobs:
#         job_title = item.find('a', {'data-automation': 'jobTitle'}).text.strip()
#         link = item.find('a', href=True)
#         print(link['href'])
#         company = item.find('a', {'data-automation': 'jobCompany'}).text.strip()
#
#         try:
#             if item.find('span', {'data-automation': 'jobPremium'}).text == 'Featured':
#                 is_featured = True
#
#         except AttributeError as error:
#             is_featured = False
#
#         location = item.find('a', {'data-automation': 'jobLocation'}).text.strip()
#         classification = item.find('a', {'data-automation': 'jobClassification'}).text.strip()
#         sub_classification = item.find('a', {'data-automation': 'jobSubClassification'}).text.strip()
#
#         job = {
#             'job_title': job_title,
#             'company': company,
#             'is_featured': is_featured,
#             'location': location,
#             'classification': classification,
#             'sub_classification': sub_classification
#         }
#
#         job_list.append(job)
#     return job_list


def extract_job_content(soup):
    title = soup.find('h1', {'data-automation': 'job-detail-title'}).text.strip()
    company = soup.find('span', {'data-automation': 'advertiser-name'}).text.strip()
    location = soup.find('div', class_='yvsb870 _14uh9944y o76g430').text.strip()

    print(f'title: {title}, company: {company}, location: {location}')

    # job_title = item.find('a', {'data-automation': 'jobTitle'}).text.strip()
    # link = item.find('a', href=True)
    # print(link['href'])
    # company = item.find('a', {'data-automation': 'jobCompany'}).text.strip()
    #
    # try:
    #     if item.find('span', {'data-automation': 'jobPremium'}).text == 'Featured':
    #         is_featured = True
    #
    # except AttributeError as error:
    #     is_featured = False
    #
    # location = item.find('a', {'data-automation': 'jobLocation'}).text.strip()
    # classification = item.find('a', {'data-automation': 'jobClassification'}).text.strip()
    # sub_classification = item.find('a', {'data-automation': 'jobSubClassification'}).text.strip()
    #
    # job = {
    #     'job_title': job_title,
    #     'company': company,
    #     'is_featured': is_featured,
    #     'location': location,
    #     'classification': classification,
    #     'sub_classification': sub_classification
    # }




job_links = []
job_list = []

page_url = create_url(1)
page_soup = get_page(page_url)
job_links = extract_job_urls(page_soup)

# print(*job_links, sep='\n')
print(job_links[0])

job_soup = get_page(job_links[0])
extract_job_content(job_soup)
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
        job_links.append(base_url + link['href'])
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

    divs_location_classification = soup.find_all('div', class_='yvsb870 _14uh9944y o76g430')

    location = divs_location_classification[0].text.strip()
    classification = divs_location_classification[1].text.strip()
    sub_classification = divs_location_classification[2].text.strip()

    if len(divs_location_classification) > 4:
        salary = divs_location_classification[3].text.strip()
        work_type = divs_location_classification[4].text.strip()

    else:
        salary = 0
        work_type = divs_location_classification[3].text.strip()

    date_div = soup.find_all('span', class_='yvsb870 _14uh9944u _1qw3t4i0 _1qw3t4i1y _1qw3t4i1 _1d0g9qk4 _1qw3t4ib')

    if len(date_div) > 1:
        date = date_div[1].text.split()[1]
    else:
        date = date_div[0].text.split()[1]

    div_description = soup.find('div', class_='yvsb870 _1v38w810')
    # print(div_description.findAll('strong'))

    list_header = []
    list_dictionary = {}
    description = []

    # for item in div_description.contents:
    #     bullets = []
    #     if item.name == 'p' and item.text.strip() != '':
    #         if item.next.name == 'strong':
    #             list_header.append(item.text.strip())
    #             # print(item.nextSibling.name)
    #             if item.nextSibling.name == 'ul':
    #                 for li in item.nextSibling():
    #                     bullets.append(li.text.strip())
    #
    #                 list_dictionary[list_header[-1]] = bullets
    #         else:
    #             description.append(item.text.strip())
    #             list_dictionary['No Header'] = description

    d = div_description.find()

    for item in div_description:
        if len(item.find_all()) != 0:
            for i in item.find_all():
                print(f'child: {i.name}')

        print(f'item: {item.name}')

    for item in div_description.contents:
        bullets = []
        if item.name == 'p' and item.text.strip() != '':
            list_header.append(item.text.strip())

            if item.next.name == 'strong':
                list_header.append(item.text.strip())
                # print(item.nextSibling.name)
                if item.nextSibling.name == 'ul':
                    for li in item.nextSibling:
                        bullets.append(li.text.strip())

                    list_dictionary[list_header[-1]] = bullets
            else:
                description.append(item.text.strip())
                list_dictionary['No Header'] = description


    # print(list_header)
    # print(list_dictionary)
    # print(description)

    # print(f'\ntitle: {title}, company: {company}, location: {location}, ' f'classification: {classification},
    # sub_classification: {sub_classification}, work-type: {work_type}, salary: {salary},' f'date: {date}')

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
# print(job_links[0])

job_soup = get_page('https://www.seek.com.au/job/56834934?type=promoted#sol=038f232f723e05334090555b9702357a2e095e9b')
extract_job_content(job_soup)

# for link in job_links:
#     job_soup = get_page(link)
#     extract_job_content(job_soup)

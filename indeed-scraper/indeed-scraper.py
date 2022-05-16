import requests
from bs4 import BeautifulSoup
import pandas as pd

''' sample url and parameters 

'https://au.indeed.com/jobs?q=Data%20Analyst&l=Adelaide%20Region%20SA&radius=5&rbl=South%20Australia&jt=fulltime&fromage=3&vjk=9f295382cccd3b9a'

date_posted = ['1', '3', '7', '14', 'last']
radius = [0, 5, 10, 15, 25, 50, 100]
    radius 0 -> exact location only
job_type = ['', 'fulltime', 'contract', 'permanent']
rbl=South Australia -> choose the location between Adelaide and South Australia

'''
params = {
    'job_title': 'data analyst',
    'location': 'Adelaide',
    'radius': 50,
    'job_type': '',
    'date_posted': 'last'
}


def generate_url(params, page):
    url = f'https://au.indeed.com/jobs?q={params["job_title"]}' \
          f'&l={params["location"]}' \
          f'&radius={params["radius"]}' \
          f'&jt={params["job_type"]}' \
          f'&fromage={params["date_posted"]}' \
          f'&start={page}'
    return url


def extract(page):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/101.0.4951.67 Safari/537.36'}
    url = generate_url(params, page)
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup


def transform(soup):
    divs = soup.find_all('div', class_='cardOutline')

    for item in divs:
        title = item.find('a').text.strip()
        company = item.find('span', class_='companyName').text.strip()
        try:
            salary = item.find('div',
                               class_='heading6 tapItem-gutter metadataContainer noJEMChips salaryOnly').text.strip()

        except:
            salary = ''

        summary = item.find('div', class_='job-snippet').text.strip().replace('\n', '')

        # using a dictionary
        # summary = item.find('div', {'class' = 'job-snippet'}).text.strip()

        job = {
            'title': title,
            'company': company,
            'salary': salary,
            'summary': summary
        }
        joblist.append(job)

    print(*joblist, sep='\n')
    return


joblist = []

c = extract(0)
# transform(c)

print(c)

# for i in range(0, 60, 10):
#     print(f'Getting page {i}')
#     c = extract(i)
#     transform(c)
#
# df = pd.DataFrame(joblist)
# df.to_csv('data/indeed-jobs.csv')

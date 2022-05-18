
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

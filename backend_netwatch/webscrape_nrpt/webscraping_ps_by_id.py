import requests, csv, re
import numpy as np
from bs4 import BeautifulSoup
from datetime import date
from geopy.geocoders import Nominatim

ids_14k = [14144,14203,14211,14250,14259,14188,14271,14126,14421,14425,14400,14461,14463,14405,14383,14644,14707,14681,14682,14743,14602,14715,14716,14575,14730,14782,14794, 14849]
ids_15k = [15252,15259, 15198, 15344, 15148, 15210, 15465,15030,15371,15034, 15504,15298, 15512,15495,15042, 15313,15241,15242,15244]
ids_16k = [16468,16507, 16509, 16904,16973, 16975,16721,16681]
ids_26k = [26470, 26690, 26498,26499, 26521,26736,26525,26529, 26760,26945,26465, 26967,27332,26891,27079, 26844]
ids_27k = [27257, 27532,27534,27802, 27459,27549,27809, 27560,27564,27567,27486,27852,27992,27996, 27917]
ids_28k = [28275, 28178,27942, 28031,28205,28206, 27960,28470, 28472, 28045,28548, 28225, 28632,28050,28636]
ids_29k = [29188,29284,29379,29289, 29290,29198, 29389,29297, 29484, 29209, 29579, 29489,29581,29212,29583, 29584,29585, 29586, 29021,29589, 29399, 29114, 29494,29402,29219,29133,29134, 29048,29326,29429, 29515, 29431, 29517,29056,29435,29437, 29613, 29333,29616, 29335,29338, 29339,29064, 29065,29528,29066, 29069,29626,29345, 29534,29632, 29087,29463, 29089,29093,29271,29646, 29557, 29369,29561]
ids_30k = [30786,30887,30891,30800, 30978, 30979,30980,30804,30897,30809,30717,30718,30908,30821, 30822,31078,30826,30830,30999, 31083,30733,31089,31092,31093,31166,31012,31015, 30666,30668,30674,30936,31180,30681,31027,31028, 31029, 31032,30687, 30945,30759,30760,30691,30766, 30772, 31196, 30777,31121,31354,30779]
ids_31k = [31445,31202, 31054,31449, 31128, 31206, 30961,31274, 31133, 31058, 31364,31136, 30967,31217, 31458, 31141,31372,31555, 30971, 31148,31462, 31288,31375, 31376, 31633,31726,31727,31224, 31227, 31153,31637,31381, 31230, 31384,31735, 31472,31473, 31737,31393,31820,31741, 31743,31744, 31746,31747,31573, 31825,31481,31751,31402,31310,31655,31249, 31578, 31407,31408, 31831,31409,31658, 31659, 31756,31757, 31581, 31582,31411,31315,31834,31490, 31836, 31586,31663,31319,31915,31917,31422,31842,31843, 31919,31920,31766,31921, 31922, 31923, 31672,31925,31329,31846,31595,31770,31774,31850,31851,31930,31931,31932,31933, 31678,31776,31777,31935,31336,31509,31779,31602,31855,31435,31940,31943,31944,31683,31860,31946, 31607,31787,31517,31949,31950,31951,31952,31953,31790,31864,31865,31955,31956, 31957,31792, 31522,31959,31960,31690,31797,31798,31528,31963,31871,31872,31873,31875,31693,31801,31530,31696,31967,31619,31805,31879,31969,31880,31881,31882,31883,31884,31885,31886,31887,31888,31889,31890,31891,31808,31810,31811,31972,31974,31975,31976,31625,31626,31703,31704,31706,31707,31895,31896,31630,31898,31980,31982,31983,31984,31985, 31713,31986,31714,31987,31988,31715,31990,31991,31992,31993,31994,31995,31996,31997,31998,31999,31904,31719,31721,31909,31724,31910,31911]
ids_32k = [32002,32003,32008,32010,32011,32015,32016, 32018,32019,32021,32026,32028,32030,32032, 32036,32039, 32040, 32043,32044,32047,32050, 32052,32054,32058]
ps_ids = np.concatenate([ids_14k,ids_15k,ids_16k,ids_26k,ids_27k,ids_28k,ids_29k,ids_30k, ids_31k,ids_32k])

def find_trainer_details(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    ##############################################################
    if soup.title:
        name = soup.title.text
        name = name.replace(' - Personal Trainer', '')
    else:
        name = None
    
    if soup.find('span', class_="tel-full"):
        number = soup.find('span', class_="tel-full").text
    else:
        number = None
    
    if soup.find('p', class_="purpleblock"):
        website = soup.find('p', class_="purpleblock").text
    else:
        website = None
    if website == '\n':
        website = website.replace('\n', '')
    ##############################################################
    find_location = soup.find('ul', class_='areas')
    print(url)
    html_areas = find_location.find_all('li')

    areas = []

    for area in html_areas:
        areas.append(area.text)
    ##############################################################
    social_media_location = soup.find('div', class_="mashup mashupdetails")
    social_media = social_media_location.find_all('a')
    website_linkedin = None
    website_twitter = None
    website_facebook = None
    website_youtube = None
    website_instagram = None

    for social in social_media:
        if social.find('img', alt=True):
            current_website = social.find('img', alt=True)['alt']

            if current_website == 'LinkedIn':
                website_linkedin = social['href']
            if current_website == 'Facebook':
                website_facebook = social['href']
            if current_website == 'YouTube':
                website_youtube = social['href']
            if current_website == 'Twitter':
                website_twitter = social['href']
            if current_website == 'Instagram':
                website_instagram = social['href']

    ##############################################################
    age = None if not soup.find('strong', text='Age') else (soup.find('strong', text='Age').parent.text).replace('\n', '')
    gender = None if not soup.find('strong', text='Gender') else (soup.find('strong', text='Gender').parent.text)
    member_since = None if not soup.find('strong', text='Member Since') else soup.find('strong', text='Member Since').parent.text
    date_today = date.today()
    if age:
        age = age.replace('Gender: MaleAge: ', '')
        age = age.replace('Gender: FemaleAge: ', '')
    if member_since:
        member_since = member_since.replace('Member Since: ', '')
    gender = 'Male' if 'Male' in gender else 'Female'
    ##############################################################
    return name, number, age, gender, member_since, date_today, website, areas, website_twitter, website_linkedin, website_facebook, website_youtube, website_instagram

profiles = {}
t_id = []
group_details = []
for id in ps_ids:
    URL = f'https://nrpt.co.uk/profiles/trainers/{id}/-.htm'
    
    name, number, age, gender, member_since, date_today, website, areas, twitter, linkedin, facebook, youtube, instagram = find_trainer_details(URL)


    profiles[name] = {
        'name': name,
        'trainer_id': id,
        'number': number,
        'age': age,
        'gender': gender,
        'member_since': member_since,
        'date_today': date_today,
        'website': website,
        'areas': areas,
        'twitter': twitter,
        'linkedin': linkedin,
        'facebook': facebook,
        'youtube': youtube,
        'instagram': instagram
        }

fieldnames = ['name', 'trainer_id', 'number',  'age', 'gender', 'member_since', 'date_today','address', 'website', 'areas', 'twitter', 'linkedin', 'facebook', 'youtube', 'instagram']
with open('personal_trainers_ids.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(profiles.values())

# 356 City
# 398 Town
# 387 County

# 417 Total





import requests, csv, re
from bs4 import BeautifulSoup
from datetime import date
from geopy.geocoders import Nominatim


URL = ''
weblinks = set()

locations_city = ['Aberdeen', 'Belfast', 'Birmingham', 'Brighton', 'Bradford', 'Bristol', 'Cardiff', 'Coventry', 'Dundee',
 'Edinburgh', 'Exeter', 'Glasgow', 'Hull', 'Leeds', 'Leicester', 'Liverpool',  'London', 'Manchester', 'Newcastle', 'Newcastle-Upon-Tyne',
  'Norwich', 'London', 'Reading',  'Sheffield', 'Southampton', 'Sunderland', 'Tunbridge-Wells', 'York']

locations_town = ['Altrincham', 'Ashford', 'Aylesbury', 'Banbury', 'Barnsley','Basingstoke', 'Beaconsfield', 'Bromley',
 'Bath', 'Bedford','Blackburn', 'Blackpool', 'Bournemouth', 'Bracknell', 'Cambridge','Carlisle', 'Chelmsford', 'Cheltenham', 'Chester', 'Colchester', 'Crawley', 'Croydon',
 'Derby', 'Doncaster', 'Dover', 'Dundee', 'Durham', 'Eastbourne','Egham', 'Gloucester', 'Grimsby', 'Guildford', 'Hemel-Hempstead', 'High-Wycombe', 'Huddersfield','Hull',
  'Inverness', 'Ipswich', 'Kingston-Upon-Thames', 'Lancaster','Leamington-Spa', 'Lincoln', 'Marlow', 'Maidenhead', 'Middlesbrough', 'Milton-Keynes',
   'Newport', 'Northampton','Nottingham', 'Oxford', 'Perth', 'Peterborough', 'Plymouth','Portsmouth', 'Preston', 'Rugby', 'Sevenoaks','Slough', 'stoke-on-trent', 'Swansea',
    'Swindon', 'Tonbridge','Torquay', 'Twickenham','Winchester', 'Wolverhampton', 'Worcester', 'Wrexham']

locations_county = ['Aberdeenshire','Angus','Ayrshire','Banffshire','Bedfordshire','Berkshire','Buckinghamshire','Caithness','Cambridgeshire','Carmarthenshire','Cheshire',
'Clackmannanshire','Cornwall','Denbighshire','Derbyshire','Devon','Dorset','Dumfriesshire','East-Lothian','East-Sussex','Essex','Fife',
'Flintshire','Gloucestershire','Hampshire','Herefordshire','Hertfordshire','Inverness-Shire','Kent','Lanarkshire','Lancashire','Leicestershire','Lincolnshire',
'Middlesex','Midlothian','Monmouthshire','Norfolk','Northamptonshire','Northumberland','Nottinghamshire','Oxfordshire',
'Pembrokeshire','Perthshire','Renfrewshire','Rutland','Scottish-Borders','Selkirkshire','Shropshire','Somerset','Staffordshire','Stirlingshire','Suffolk','Surrey','Worcestershire','Wiltshire',
'Wigtownshire', 'Westmorland', 'West-Sussex', 'West-Lothian', 'Warwickshire','Yorkshire']

geopraphy = [locations_city, locations_town, locations_county]

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
for k in range(3):
    locations = geopraphy[k]
    for location in locations:
        URL_city = 'https://nrpt.co.uk/city/personal-trainers-' + location + '.htm?page='
        URL_town = 'https://nrpt.co.uk/town/personal-trainers-' + location + '.htm?page='
        URL_county = 'https://nrpt.co.uk/location/personal-trainers-' + location + '.htm?page='
        URLS = [URL_city, URL_town , URL_county]
        URL = URLS[k]
        i = 1
        while True:

            page = requests.get(URL + str(i))
            i += 1

            soup = BeautifulSoup(page.content, 'html.parser')

            trainers_weblinks = soup.find_all('a', class_="wtrk-click", href=True)
            if not trainers_weblinks:
                break
            ##########################################################
            address_book = []
            trainers_id = []
            list_profiles = (soup.find('ul', class_="searchresults")).find_all('li')
            for prof in list_profiles:
                if 'There are no results for your search.' in prof.text:
                    continue                
                long, lat = prof['data-item-latitude'], prof['data-item-longitude']
                trainer_id = prof['data-item-trainerid']
                if long and lat:
                    locator = Nominatim(user_agent='myGeocoder')
                    coordinates = long, lat
                    location = locator.reverse(coordinates)
                    address = location.raw['display_name']
                else:
                    address = None
                address_book.append(address)
                trainers_id.append(trainer_id)
                t_id.append(trainer_id)
            ##########################################################
            print(URL + str(i))
            seen = set()
            weblinks = []
            for trainer in trainers_weblinks:
                weblink = trainer['href']
                if weblink not in seen:
                    weblinks.append(weblink)
                    seen.add(weblink)
            for q in range(len(weblinks)):
                weblink = weblinks[q]
                address = address_book[q]
                trainer_id = trainers_id[q]
                group_details.append((weblink, address, trainer_id))

        
    for weblink, address, trainer_id in group_details:

        url = 'https://nrpt.co.uk' + weblink
        
        name, number, age, gender, member_since, date_today, website, areas, twitter, linkedin, facebook, youtube, instagram = find_trainer_details(url)

        profile_id = re.sub("[^0-9]", "", weblink)

        profiles[name] = {
            'name': name,
            'trainer_id': trainer_id,
            'number': number,
            'age': age,
            'gender': gender,
            'member_since': member_since,
            'date_today': date_today,
            'address': address,
            'website': website,
            'areas': areas,
            'twitter': twitter,
            'linkedin': linkedin,
            'facebook': facebook,
            'youtube': youtube,
            'instagram': instagram
            }

fieldnames = ['name', 'trainer_id', 'number',  'age', 'gender', 'member_since', 'date_today','address', 'website', 'areas', 'twitter', 'linkedin', 'facebook', 'youtube', 'instagram']
with open('personal_trainers.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(profiles.values())

print(t_id)
# 356 City
# 398 Town
# 387 County

# 417 Total





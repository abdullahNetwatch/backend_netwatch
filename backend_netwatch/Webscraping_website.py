import requests
from bs4 import BeautifulSoup

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
    ##############################################################
    find_location = soup.find('ul', class_='areas')
    html_areas = find_location.find_all('li')

    areas = []

    for area in html_areas:
        areas.append(area.text)
    ##############################################################
    return name, number, website, areas

profiles = {}
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

            for trainer in trainers_weblinks:
                weblink = trainer['href']
                weblinks.add(weblink)

    for weblink in weblinks:

        url = 'https://nrpt.co.uk' + weblink
        
        name, number, website, areas = find_trainer_details(url)

        profiles[name] = {
            'name': name,
            'number': number,
            'website': website,
            'areas': areas
            }
        

print(len(profiles.keys()))
print(profiles.keys())
# 356 City
# 398 Town
# 387 County

# 417 Total




import re, json
from norm_north_america import state_to_country


with open('Data/prefix_to_country.json', 'r') as json_file:
    prefix_to_country = json.load(json_file)

with open('Data/country_to_prefix.json', 'r') as json_file:
    country_to_prefix = json.load(json_file)

with open('Data/national_number_length.json', 'r') as json_file:
    national_number_length = json.load(json_file)



custom_prefixes = {
    '+440': 'UK',
    '440': 'UK'
}

prefix_to_country = prefix_to_country | custom_prefixes


def stripping_number(number):
    # gets rid of non-numeric values
    num = re.sub("[^0-9]", "", number)

    # remove leading zeros
    num = num.strip('0')

    # adds + if present in original
    if number[0] == '+':
        num = '+' + num

    return num


def normalising_number(number):

    for i in reversed(range(5)):
        prefix = number[:i+1]
        prefix_length = len(prefix)

        if prefix in prefix_to_country or prefix in state_to_country:
            if prefix in state_to_country:
                country, area_code = state_to_country[prefix]
            else:
                country, area_code = prefix_to_country[prefix], ''

                # check length of number within countries boundries
                if type(national_number_length[country][0]) == str or type(national_number_length[country][0]) == str:
                    pass
                
                elif not (national_number_length[country][0] <= len(number[prefix_length:]) <= national_number_length[country][1]):
                    continue


            return area_code + number[prefix_length:], country

    # number does not contain country code
    return number, None
 


def normalise_number(number, country):

    prefix = country_to_prefix[country]
    return prefix + number


def normalisation(number, input_country=None):
    original_number = number
    number = stripping_number(number)
    number, country = normalising_number(number)

    country = country or input_country

    if country is not None:
        number = normalise_number(number, country)
    else:
        # further investigation
        return 'unknown location', original_number, number, country, input_country
        

    return original_number, number, country, input_country

numbers = [{ 
"phone": "07429061100",
"country": "UK"},

{ 
"phone": "+4407429061100",
"country": "UK"},

{ 
"phone": "07429061100",
"country": None},

{ 
"phone": "07429061100",
"country": 'UK'},

{ 
"phone": "44(0)7429061100",
"country": "UK"},

{ 
"phone": "+1-604-555-0184",
"country": None},

{ 
"phone": "+1 (416) 440-0289",
"country": None},

{ 
"phone": "+1 212-554-1515",
"country": None}
]

details = [('RU', '9848168244'), ('RS', '+38164274286'), ('RU', '886-932-60451'), ('IT', '+39030213029'), ('DE', '+49602145348'), ('RS', '+38164286904'), ('RS', '+38164115322'), ('IT', '+39338253232'), ('CU', '532376173'), ('TR', '904445135'), ('IT', '+39392462357'), ('AT', '+436647510401'), ('ID', '+628135100683'), ('ID', '+628180819766'), ('IT', '+3902643753'), ('RU', '3851481790'), ('RU', '92 42 757965'), ('FI', '+35844266616'), ('CH', '41213015317'), ('KR', '+82109112031'), ('RS', '+38169117755'), ('IT', '+39 366356560'), ('SE', '+4631755870'), ('AT', '+43676384304'), ('CU', '533346064'), ('RU', '88697952377'), ('VN', '847997350'), ('IT', '+39 095 717800')]
for detail in details:
    number, country = detail[1], detail[0]
    print(normalisation(number, country))





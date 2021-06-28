import requests, json, csv

def get_user_name_info(user_name):

    url = f'https://api.untappd.com/v4/user/info/{user_name}?compact=enhanced&limit=5&badges=true&badgeLimit=5&rating_breakdown=true&beers=true&utv=3.5.4&access_token=1D2343A752622BD2971BDBF0B587366723CD2DBD'
    response = requests.get(url)
    obj = json.loads(response.content)['response']['user']
    first_name = obj['first_name']
    last_name = obj['last_name']
    user_avatar = obj['user_avatar']

    profile = {
        'user_name': user_name,
        'first_name': first_name,
        'last_name': last_name,
        'user_avatar': user_avatar
    }
    
    filename = 'profiles.jsonl'

    with open(filename, 'a', newline='', encoding='UTF8') as jsonlfile:
        json.dump(profile, jsonlfile)
        jsonlfile.write('\n')
    jsonlfile.close()

    return

def get_profile_from_location(location_id, unique_user_names):

    profiles = set()
    url = f'https://api.untappd.com/v4/beer/info/{location_id}?compact=enhanced&ratingEnhanced=true&utv=3.5.4&access_token=1D2343A752622BD2971BDBF0B587366723CD2DBD'
    response = requests.get(url)
    if json.loads(response.content)['response']:
        if 'items' in json.loads(response.content)['response']['beer']['checkins']:
            obj = json.loads(response.content)['response']['beer']['checkins']['items']
            for profile in obj:
                user_name = profile['user']['user_name']
                if user_name not in unique_user_names:
                    profiles.add(user_name)
                    unique_user_names.add(user_name)
                else:
                    print('duplicate user: ' + user_name)

    filename = 'usernames_from_location.csv'

    with open(filename, 'a', encoding='UTF8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for user_name in profiles:
            writer.writerow([user_name])
    
    csvfile.close()


    return unique_user_names

def get_usernames_from_locations(upper_bound):

    filename = 'profiles.jsonl'
    jsonlfile = open(filename, 'w')
    jsonlfile.close()

    filename = 'usernames_from_location.csv'
    csvfile = open(filename, 'w')
    csvfile.close()

    unique_user_names = set()

    for i in range(1, upper_bound):
        get_profile_from_location(i, unique_user_names)
    

    with open(filename, 'r', encoding='UTF8') as csvfile:
        reader = csv.reader(csvfile)

        for user_name in reader:
            get_user_name_info(user_name[0])

    csvfile.close()
    return 


# get_usernames_from_locations(10)
# print(get_profile(845096))

def find_friends(user_name):
    x = 0
    friends = set()
    while True:
        url = f'https://api.untappd.com/v4/user/friends/{user_name}?utv=3.5.4&access_token=1D2343A752622BD2971BDBF0B587366723CD2DBD&offset={x}'
        response = requests.get(url)

        obj = json.loads(response.content)['response']['items']
        
        if obj == []:
            break

        for profile in obj:
            friend_user_name = profile['user']['user_name']
            friends.add(friend_user_name)
        x += 25

    print(user_name + ' has ' + str(len(friends)) + ' friends')

    return friends

# print(find_friends('magilljl'))
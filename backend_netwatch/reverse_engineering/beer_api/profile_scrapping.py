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

    return profile

def get_profile(location_id):

    profiles = []
    url = f'https://api.untappd.com/v4/beer/info/{location_id}?compact=enhanced&ratingEnhanced=true&utv=3.5.4&access_token=1D2343A752622BD2971BDBF0B587366723CD2DBD'
    response = requests.get(url)
    obj = json.loads(response.content)['response']['beer']['checkins']['items']
    for profile in obj:
        user_name = profile['user']['user_name']
        profiles.append(get_user_name_info(user_name))

    csv_file = 'profiles_' + str(location_id) + '.csv'

    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=['user_name', 'first_name', 'last_name', 'user_avatar'])

        for profile in profiles:
            writer.writerow(profile)
    csvfile.close()

    with open(csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile,fieldnames=['user_name', 'first_name', 'last_name', 'user_avatar'])

        for profile in reader:
            print(profile)
    csvfile.close()
    return


# print(get_profile(845096))

def find_friends(user_name):
    x = 0
    friends = set()
    while True:
        friends_api = f'https://api.untappd.com/v4/user/friends/{user_name}?utv=3.5.4&access_token=1D2343A752622BD2971BDBF0B587366723CD2DBD&offset={x}'
        response = requests.get(friends_api)

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
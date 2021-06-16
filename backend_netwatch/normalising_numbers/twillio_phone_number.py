# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
import twilio
from random_numbers import nums

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)

numbers = ['+447429061100','+4407429061100','+44(0)7429061100',
            '+447429061100','+4407429061100','+44(0)7429061100',
            '07429061100', '+7429061100']

located_numbers = []
for number in nums:
    try:
        phone_number = client.lookups \
                            .v1 \
                            .phone_numbers(number) \
                            .fetch(country_code='RU')

        located_numbers.append((phone_number.country_code, number))

    except twilio.base.exceptions.TwilioRestException as err:
        pass

print(located_numbers)

# 1000 = 175s
# 10000 = 1886s

# original = 9848168244
# Iranian = 98-48168244
# Indian = (91) 9848168244

# original = 904445135
# turkish = 90-4445135 ?

# original = 847997350
# vitenam = 84-7997350
# vitenam number = +84-933715573
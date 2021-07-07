import requests
from bs4 import BeautifulSoup
from datetime import datetime
from multiprocessing import Pool

######################################################
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print(current_time, 1)
######################################################
names = []
def find_profile(index):
    URL = f'https://nrpt.co.uk/profiles/trainers/{index}/-.htm'
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.title.text
    if 'could not be found' not in title:
        names.append(title)
        print(title, index)
#####################################################
indexes = [i for i in range(26000, 27000)]

def main():
    p = Pool()
    p.map(find_profile, indexes)
    p.terminate()
    p.join()
######################################################
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(current_time)
    print(names)
######################################################

if __name__ == '__main__':
    main()

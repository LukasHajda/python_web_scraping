import requests
from bs4 import BeautifulSoup
import re

class Soup:
    def __init__(self):
        self.main_page = 'https://www.hyperia.sk'


    def get_elements(self):
        request = requests.get(self.main_page + '/kariera/')
        webpage = BeautifulSoup(request.content, 'html.parser')
        all_positions = webpage.select('#positions > div > div.row > div')

        result = []
        for pos in all_positions:
            position = Position()
            request = requests.get(self.main_page + pos.select('a')[0]['href'])
            position_page = BeautifulSoup(request.content, 'html.parser')

            title = pos.find('h3').text
            type = re.search(r'<p.*<strong.*</strong>(.+).*</p>', str(position_page.select('#__layout > div > div > section.position-hero > div:nth-child(2) > div > div > div:nth-child(3) > p')[0])).group(1)
            salary = re.search(r'<p.*<strong.*</strong>(.+).*</p>', str(position_page.select('#__layout > div > div > section.position-hero > div:nth-child(2) > div > div > div:nth-child(2) > p')[0])).group(1)
            place = re.search(r'<p.*<strong.*</strong>(.+).*</p>', str(position_page.select('#__layout > div > div > section.position-hero > div:nth-child(2) > div > div > div:nth-child(1) > p')[0])).group(1)
            email = position_page.select('a[href^="mailto"]')[0]['href']

            type = re.sub('<br[^>]*>', '', type)
            salary = re.sub('<br[^>]*>', '', salary)
            place = re.sub('<br[^>]*>', '', place)

            position.salary = salary
            position.type = type
            position.place = place
            position.email = email
            position.title = title

            result.append(position)
        return result


class Position:
    def __init__(self):
        self.title = None
        self.salary = None
        self.place = None
        self.type = None
        self.email = None

if __name__ == '__main__':
    soup = Soup()
    result = soup.get_elements()
    result = list(map(lambda x: x.__dict__, result))

    print(result)


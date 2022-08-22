import requests
from bs4 import BeautifulSoup
import re
import json

"""
Class: Soup
------------------------
Sending requests to specific URL and parse given response
"""
class Soup:
    def __init__(self):
        self.main_page = 'https://www.hyperia.sk'

    def get_elements(self):
        request = requests.get(self.main_page + '/kariera/')
        webpage = BeautifulSoup(request.content, 'html.parser')

        # Get all positions
        all_positions = webpage.select('#positions > div > div.row > div')

        result = []
        # Loop through all positions and process them
        for pos in all_positions:

            # Open URL of current position
            request = requests.get(self.main_page + pos.select('a')[0]['href'])
            position_page = BeautifulSoup(request.content, 'html.parser')

            # Get title
            title = pos.find('h3').text

            # Type, Salary and Place texts are in <p> tags but inside this tag there are <strong> and <br> tags which have to be cleared to get required text.
            # Use CSS selectors as far as we can. Next with help of regex we ensure that <strong> tags will be cleared
            type = re.search(r'<p.*<strong.*</strong>(.+).*</p>', str(position_page.select('#__layout > div > div > section.position-hero > div:nth-child(2) > div > div > div:nth-child(3) > p')[0])).group(1)
            salary = re.search(r'<p.*<strong.*</strong>(.+).*</p>', str(position_page.select('#__layout > div > div > section.position-hero > div:nth-child(2) > div > div > div:nth-child(2) > p')[0])).group(1)
            place = re.search(r'<p.*<strong.*</strong>(.+).*</p>', str(position_page.select('#__layout > div > div > section.position-hero > div:nth-child(2) > div > div > div:nth-child(1) > p')[0])).group(1)
            email = position_page.select('a[href^="mailto"]')[0]['href']

            # Remove all <br> tags
            type = re.sub('<br[^>]*>', '', type)
            salary = re.sub('<br[^>]*>', '', salary)
            place = re.sub('<br[^>]*>', '', place)

            # Create new instance of class Position
            position = Position(title, salary, place, type, email)

            result.append(position)
        return result

"""
Class: Position
------------------------
Keep position data in class 
"""
class Position:
    def __init__(self, title, salary, place, type, email):
        self.title = title
        self.salary = salary
        self.place = place
        self.contract_type = type
        self.contact_email = email

if __name__ == '__main__':
    soup = Soup()
    result = soup.get_elements()

    # Change all instances to JSON format
    result = list(map(lambda x: x.__dict__, result))

    # Save them to the result.json file
    with open('result.json', 'w', encoding = 'utf8') as file:
        json.dump(result, file, indent = 2, ensure_ascii = False)



import requests
from bs4 import BeautifulSoup
from retry import retry
import time


class PEPScrap:
    FIELDS = ('PEP:', 'Title:', 'Author:', 'Status:', 'Type:', 'Created:')

    def __init__(self, endpoint):
        self.endpoint = endpoint

    @retry(exceptions=Exception, tries=5, delay=2, backoff=2, max_delay=10)
    def data_pep(self) -> dict:
        """scrap data from PEPs"""
        fields = PEPScrap.FIELDS
        div = self.__get_main_data()
        for pep_data in self.__get_peps_links(div):
            time.sleep(0.3)
            db = {}
            count = 0
            for pep_one in pep_data:
                column = pep_one.find('th').text
                if column in fields:
                    column_data = pep_one.find('td').text
                    db[column.strip(':')] = column_data
                    if count == 6:
                        break
                    count += 1
            yield db

    def __make_soup(self):
        """make soup from endpoints"""
        response = requests.get(self.endpoint)
        if response.status_code == 200:
            return BeautifulSoup(response.content, 'html.parser')

    def __get_main_data(self):
        """from main site get links data"""
        soup = self.__make_soup()
        if soup:
            div_numeric = soup.find('div', attrs={"class": "section", "id": "numerical-index"})
            return div_numeric.find_all("a", attrs={"class": "reference external"})

    def __get_peps_links(self, div):
        """create links from href and return data from each PEP"""
        for links in div:
            link = links.get('href')
            self.endpoint = f'https://www.python.org{link}'
            soup = self.__make_soup()
            if soup:
                pep_div = soup.find('tbody', attrs={'valign': 'top'})
                yield pep_div.find_all('tr')

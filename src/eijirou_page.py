import urllib.parse
import urllib.request
from bs4 import BeautifulSoup

class EijirouPage:
    _URL_FORMAT = "https://eow.alc.co.jp/search?q={}"
    _CSS_SELECTOR_PRONUNCIATION = "span.pron"
    _PRONUNCIATION_DELIMITER = "｜"
    _PRONUNCIATION_EXTRA_US = "[US]"
    _PRONUNCIATION_EXTRA_UK = "[UK]"
    _PRONUNCIATION_EXTRA_SUFFIX = "、"

    def __init__(self, query_word:str):
        url_encoded_query = urllib.parse.quote(query_word)
        url = self._URL_FORMAT.format(url_encoded_query)
        response = urllib.request.urlopen(url)
        self._soup = BeautifulSoup(response, "html.parser")
        response.close()
    
    def get_pronunciation(self):
        container = self._soup.select_one(self._CSS_SELECTOR_PRONUNCIATION)
        if container:
            text = container.get_text().strip()
            text = text.split(self._PRONUNCIATION_DELIMITER)[0]
            text = text.replace(self._PRONUNCIATION_EXTRA_US, "")
            text = text.replace(self._PRONUNCIATION_EXTRA_UK, "")
            text = text.replace(self._PRONUNCIATION_EXTRA_SUFFIX, "")
            text = text.strip()
            return text
        else:
            return ""
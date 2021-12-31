import re
from typing import Optional
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup

class WeblioPage:
    _URL_FORMAT = "https://ejje.weblio.jp/content/{}"
    _CSS_SELECTOR_JAPANESE_WORDS = "div.summaryM td.content-explanation"
    _CSS_SELECTOR_PRONUNCIATION = "div.summaryM span.phoneticEjjeDesc"
    _CSS_SELECTOR_SOUND_FILE = "#ePsdDl a"
    _JAPANESE_DELIMITER = "、"
    _JAPANESE_DELIMITER_JOIN = "、"

    def __init__(self, query_word:str):
        url_encoded_query = urllib.parse.quote(query_word)
        url = self._URL_FORMAT.format(url_encoded_query)
        response = urllib.request.urlopen(url)
        self._soup = BeautifulSoup(response, "html.parser")
        response.close()
    
    def get_japanese_words(self) -> list[str]:
        container = self._soup.select_one(self._CSS_SELECTOR_JAPANESE_WORDS)
        if container:
            text = container.get_text().strip()
            return text.split(self._JAPANESE_DELIMITER)
        else:
            return []

    def get_joined_japanese_words(self) -> str:
        return self._JAPANESE_DELIMITER_JOIN.join(self.get_japanese_words())
    
    def get_pronunciation(self) -> str:
        container = self._soup.select_one(self._CSS_SELECTOR_PRONUNCIATION)
        if container:
            text = container.get_text().strip()
            if re.match(r"^‐", text):
                # -ist等、前部分が省略されている場合は取得失敗扱いで空を返す
                return ""
            else:
                return text
        else:
            return ""
    
    def get_sound_file_url(self) -> str:
        link = self._soup.select_one(self._CSS_SELECTOR_SOUND_FILE)
        if link and ('href' in link.attrs):
            url = link.attrs['href']
            return url
        else:
            return ""

    def get_sound_file_data(self) -> Optional[bytes]:
        url = self.get_sound_file_url()
        if url:
            response = urllib.request.urlopen(url)
            data = response.read()
            response.close()
            return data
        else:
            return None
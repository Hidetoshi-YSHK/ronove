import os
import re
import csv
import time
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup

INPUT_FILE = "input.csv"
INPUT_FILE_ENCODING = "utf_8"
OUTPUT_FILE = "intermediate.csv"
OUTPUT_FILE_ENCODING = "utf_8"
# サウンドファイル出力先
OUTPUT_SOUND_FILE_DIR = "sound"
# サウンドファイル接頭辞
OUTPUT_SOUND_FILE_PREFIX = "ronove"
# 単語間の実行間隔(秒)
INTERVAL_SEC = 10

# 英単語データクラス
class EnglishWord:
    word = ""
    japanese_words = []
    pronunciation = ""
    sound_file_name = ""

    def __init__(self, word):
        self.word = word

# Weblioページのクラス
class WeblioPage:
    _URL_FORMAT = "https://ejje.weblio.jp/content/{}"
    _CSS_SELECTOR_JAPANESE_WORDS = "div.summaryM td.content-explanation"
    _CSS_SELECTOR_PRONUNCIATION = "div.summaryM span.phoneticEjjeDesc"
    _CSS_SELECTOR_SOUND_FILE = "#ePsdDl a"
    _JAPANESE_DELIMITER = "、"
    _soup = None
    def __init__(self, query_word):
        url_encoded_query = urllib.parse.quote(query_word)
        url = self._URL_FORMAT.format(url_encoded_query)
        print(url)
        response = urllib.request.urlopen(url)
        self._soup = BeautifulSoup(response, "html.parser")
        response.close()
    
    def get_japanese_words(self):
        container = self._soup.select_one(self._CSS_SELECTOR_JAPANESE_WORDS)
        if container:
            text = container.get_text().strip()
            return text.split(self._JAPANESE_DELIMITER)
        else:
            return []
    
    def get_pronunciation(self):
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
    
    def get_sound_file_url(self):
        link = self._soup.select_one(self._CSS_SELECTOR_SOUND_FILE)
        if link and ('href' in link.attrs):
            url = link.attrs['href']
            return url
        else:
            return ""

# 英辞郎ページのクラス
class EijirouPage:
    _URL_FORMAT = "https://eow.alc.co.jp/search?q={}"
    _CSS_SELECTOR_PRONUNCIATION = "span.pron"
    _PRONUNCIATION_DELIMITER = "｜"
    _PRONUNCIATION_EXTRA_US = "[US]"
    _PRONUNCIATION_EXTRA_UK = "[UK]"
    _PRONUNCIATION_EXTRA_SUFFIX = "、"
    _soup = None

    def __init__(self, query_word):
        url_encoded_query = urllib.parse.quote(query_word)
        url = self._URL_FORMAT.format(url_encoded_query)
        print(url)
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

class GoogleImageSearchPage:
    _URL_FORMAT = "https://www.google.com/search?q={}&tbm=isch"

    def __init__(self, query_word):
        url_encoded_query = urllib.parse.quote(query_word)
        url = self._URL_FORMAT.format(url_encoded_query)
        print(url)
        response = urllib.request.urlopen(url)
        self._soup = BeautifulSoup(response, "html.parser")
        response.close()

# メイン処理
def main():
    english_words = []

    os.makedirs(OUTPUT_SOUND_FILE_DIR, exist_ok=True)

    with open(INPUT_FILE, encoding=INPUT_FILE_ENCODING) as f:
        reader = csv.reader(f)
        english_words = [EnglishWord(row[0]) for row in reader]
    
    for english_word in english_words:
        # Weblioから情報取得
        weblio = WeblioPage(english_word.word)
        japanese_words = weblio.get_japanese_words()
        pronunciation = weblio.get_pronunciation()
        sound_file_url = weblio.get_sound_file_url()
        print(japanese_words) 
        print(pronunciation)
        print(sound_file_url)

        # 日本語の取得に失敗したら単語をスキップ
        if not japanese_words:
            print("----")
            time.sleep(INTERVAL_SEC)
            continue

        # 発音記号の取得に失敗したら英辞郎を試す
        if not pronunciation:
            eijirou = EijirouPage(english_word.word)
            pronunciation = eijirou.get_pronunciation()
            print(pronunciation)

        # サウンドファイルのダウンロード
        sound_file_name = ""
        if sound_file_url:
            sound_file_name = (OUTPUT_SOUND_FILE_PREFIX + "_" +
                                urllib.parse.quote(english_word.word) + ".mp3")
            sound_file = (OUTPUT_SOUND_FILE_DIR + "/" + sound_file_name)
            urllib.request.urlretrieve(sound_file_url, sound_file)

        # 取得結果を詰める
        english_word.pronunciation = pronunciation
        english_word.japanese_words = japanese_words
        english_word.sound_file_name = sound_file_name

        # csvに出力
        with open(OUTPUT_FILE, 'a', encoding=OUTPUT_FILE_ENCODING, newline="") as f:
            writer = csv.writer(f)
            sound_column = ""
            if english_word.sound_file_name:
                sound_column = "[sound:" + english_word.sound_file_name + "]"
            writer.writerow([
                english_word.word,
                english_word.pronunciation,
                "、".join(english_word.japanese_words),
                sound_column,
                ""]) # 画像ファイルのカラム（別途入力するので空）

        print("----")
        time.sleep(INTERVAL_SEC)

main()
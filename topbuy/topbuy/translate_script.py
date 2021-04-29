from google_trans_new import google_translator
import re
from bs4 import BeautifulSoup

example_text = ''

class Translator_Jomi:
    def __init__(self, text):
        self.text = text
    def clean_strong(self):
        self.text = self.text.replace('<strong>', '').replace('</strong>', '')
        self.text = self.text.replace('<span class="fontstyle0">', '')
        self.text = self.text.replace('</span>', '')
    def clean_a(self):
        output = re.findall('<a href.*</a>', self.text, re.MULTILINE)
        for i in output:
            # Replace </a>
            clean_i = i.replace('</a>', '')
            find_a_start = re.match(r'<a href.*>', clean_i, re.MULTILINE)
            clean_i = clean_i.replace(find_a_start.group(0), '')
            self.text = self.text.replace(i, clean_i)
    def translations(self):
        splited_text = self.text.splitlines()
        translator = google_translator()

        for i in splited_text:
            # Search for image
            search_for_image = re.search(r'<img.*/>', i, re.MULTILINE)

            # Search for shortcode
            search_for_shortcode = re.search(r'\[.*]', i, re.MULTILINE)

            if search_for_image:
                clean_image = i.replace(search_for_image.group(0), '')
                translated = translator.translate(clean_image, lang_tgt='hr')
                soup_trans = BeautifulSoup(translated, "html.parser")
                soup = BeautifulSoup(clean_image, "html.parser")
                text_eng = soup.get_text()
                text_hr = soup_trans.get_text()
                self.text = self.text.replace(text_eng, text_hr)
            elif search_for_shortcode:
                is_box = re.search(r'\[box.*\[/box]', i, re.MULTILINE)
                if is_box:
                    i = i.replace('[/box]', '')
                    remove_box = re.search(r'\[.*]', i, re.MULTILINE)
                    clean_text_box = i.replace(remove_box.group(0), '')
                    translated = translator.translate(clean_text_box, lang_tgt='hr')
                    self.text = self.text.replace(clean_text_box, translated)
                else:
                    i = i.replace(search_for_shortcode.group(0), '')
                    translated = translator.translate(i, lang_tgt='hr')
                    self.text = self.text.replace(i, translated)
            else:
                translated = translator.translate(i, lang_tgt='hr')
                self.text = self.text.replace(i, translated)

        self.text = self.text.replace('</ Ul>', '</ul>')
        self.text = self.text.replace('<Ul>', '<ul>')
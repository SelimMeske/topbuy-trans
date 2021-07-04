from googletrans import Translator
import re
from bs4 import BeautifulSoup
import time

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
        translator = Translator()
        print("TRANSLATION IS STARTING !!!! \n")
        print("TRANSLATION IS STARTING !!!! \n")
        print("TRANSLATION IS STARTING !!!! \n")
        print("TRANSLATION IS STARTING !!!! \n")
        for i in splited_text:

            if not (i):
                print('-------------------')
                print('Skiped ' + i)
                continue
            print('Current ' + i)
            # Search for image
            search_for_image = re.search(r'<img.*/>', i, re.MULTILINE)

            # Search for shortcode
            search_for_shortcode = re.search(r'\[.*]', i, re.MULTILINE)

            if search_for_image:
                clean_image = i.replace(search_for_image.group(0), '')
                print('\u001b[34mSection one\u001b[37m')
                translated = translator.translate(clean_image, dest="hr")
                soup_trans = BeautifulSoup(translated.text, "html.parser")
                soup = BeautifulSoup(clean_image, "html.parser")
                text_eng = soup.get_text()
                text_hr = soup_trans.get_text()
                self.text = self.text.replace(text_eng, text_hr)
            elif search_for_shortcode:
                is_box = re.search(r'\[box.*\[/box]', i, re.MULTILINE)
                if is_box:
                    print('\u001b[34mSection two current text is \u001b[37m' + i)
                    remove_box_start = re.search(r'\[.*]', i, re.MULTILINE)
                    remove_box_end = re.search(r'\[\/box]', i, re.MULTILINE)
                    i = i.replace(remove_box_start.group(0), '')
                    i = i.replace(remove_box_end.group(0), '')
                    translated = translator.translate(i, dest="hr")
                    self.text = self.text.replace(i, translated.text)
                #else:
                    #print('Section three')
                    #i = i.replace(search_for_shortcode.group(0), '')
                    #translated = translator.translate(i, dest="hr")
                    #self.text = self.text.replace(i, translated.text)
            else:
                print('\u001b[34mSection four current text is \u001b[37m' + i)
                translated = translator.translate(i, dest="hr")
                self.text = self.text.replace(i, translated.text)
                

        self.text = self.text.replace('</ ', '</')
        self.text = self.text.replace('</Ul>', '</ul>')
        self.text = self.text.replace('<Ul>', '<ul>')
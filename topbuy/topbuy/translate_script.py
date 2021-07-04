from googletrans import Translator
import re
from bs4 import BeautifulSoup
import time



class Translator_Jomi:
    def __init__(self, text, language):
        self.text = text
        self.translator = Translator()
        self.language = language

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
    def sort_text_with_box(self, data):
        boxed_text = re.search(r'\[box.*\[/box]', data, re.MULTILINE)
        boxed_text = boxed_text.group(0)
        rest = data.replace(boxed_text, "")

        #Strip the box around the text
        remove_box_start = re.search(r'\[box.*?]', boxed_text, re.MULTILINE)
        remove_box_start = remove_box_start.group(0)
        remove_box_end = re.search(r'\[\/box]', boxed_text, re.MULTILINE)
        remove_box_end = remove_box_end.group(0)
        boxed_text = boxed_text.replace(remove_box_start, '')
        boxed_text = boxed_text.replace(remove_box_end, '')

        translated_rest = self.translator.translate(rest, dest=self.language)
        #sleep
        self.sleep()
        translated_boxed_text = self.translator.translate(boxed_text, dest=self.language)
        translated_boxed_text = remove_box_start + translated_boxed_text.text + '[/box]'
        return data.replace(boxed_text, translated_boxed_text).replace(rest, translated_rest.text)

    def sleep(self):
        time.sleep(5)
        print("\u001b[36mGood night. Sleeping...\u001b[37m")

    def translations(self):
        splited_text = self.text.splitlines()
        print("TRANSLATION IS STARTING !!!! \n")
        print("TRANSLATION IS STARTING !!!! \n")
        print("TRANSLATION IS STARTING !!!! \n")
        print("TRANSLATION IS STARTING !!!! \n")
        for i in splited_text:

            #If the current line is an empty string, skip.    
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
                translated = self.translator.translate(clean_image, dest=self.language)
                soup_trans = BeautifulSoup(translated.text, "html.parser")
                soup = BeautifulSoup(clean_image, "html.parser")
                text_eng = soup.get_text()
                text_hr = soup_trans.get_text()
                self.text = self.text.replace(text_eng, text_hr)
            elif search_for_shortcode:
                is_box = re.search(r'\[box.*\[/box]', i, re.MULTILINE)
                if is_box:
                    print('\u001b[34mSection two current text is \u001b[37m' + i)
                    translated_content = self.sort_text_with_box(i)
                    self.text = self.text.replace(i, translated_content)
                #else:
                    #print('Section three')
                    #i = i.replace(search_for_shortcode.group(0), '')
                    #translated = translator.translate(i, dest=self.language)
                    #self.text = self.text.replace(i, translated.text)
            else:
                print('\u001b[34mSection four current text is \u001b[37m' + i)
                translated = self.translator.translate(i, dest=self.language)
                self.text = self.text.replace(i, translated.text)
                

        self.text = self.text.replace('</ ', '</')
        self.text = self.text.replace('</Ul>', '</ul>')
        self.text = self.text.replace('<Ul>', '<ul>')
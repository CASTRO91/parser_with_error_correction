import string
import re
import ru_alphbet
from correct_text import correct_list
from model_text import *


class parser_text:
    def text_open(self):
        # открывает файл и перебирает строки
        remove_file()
        for row in open_text_file():
            if row[0] in string.ascii_letters + string.digits:
                ru_eng_text = self.split_text(row)
                if len(ru_eng_text[0]) == 0 or len(ru_eng_text[1]) == 0:
                    print('alert missing arg: ', ru_eng_text)

                self.translator(ru_eng_text)

    def split_text(self, row):
        # разбивает на две части ru и eng
        split_text_primary = row.split('\t')
        split_text_primary[1] = re.sub("\n", "", split_text_primary[1])

        def nice_text(list_with_text, number_language: int):
            # убирает повторения кавычки и скобки
            split_text = []
            for text in list_with_text:
                text = re.sub(r'\([^()]*\)', '', text.strip())
                text = text.replace("\"", "")
                if number_language == 0 and text[0] in string.ascii_letters + string.digits:
                    if text not in split_text and text.lower() not in split_text:
                        split_text.append(text)
                elif number_language == 1 and text[0] in ru_alphbet.cyrillic_letters + string.digits:
                    if text not in split_text and text.lower() not in split_text:
                        split_text.append(text)
            if len(split_text) == 0:
                split_text.append(list_with_text[0])

            return split_text

        def split_eng_ru(text, language_id: int):
            split_text = []
            if ';' in text:
                split_text = text.split(';')
                split_text = nice_text(split_text, language_id)
            else:
                split_text.append(text)
            return split_text

        english_split_text = correct_list(0, split_eng_ru(split_text_primary[0], 0))
        russian_split_text = correct_list(1, split_eng_ru(split_text_primary[1], 1))
        return english_split_text, russian_split_text

    def translator(self, ru_en_text):
        # записывает резултат в файлы в директорию /files
        if len(ru_en_text[0]) == 1 and len(ru_en_text[1]) == 1:
            write_text_file('eng', ru_en_text[0][0])
            write_text_file('ru', ru_en_text[1][0])
        else:
            for ru_text in ru_en_text[1]:
                for eng_text in ru_en_text[0]:
                    write_text_file('eng', eng_text)
                    write_text_file('ru', ru_text)

if __name__ == '__main__':
    start = parser_text()
    start.text_open()

####### БУДУ ОЧЕНЬ БЛАГОДАРЕН ЗА  FEEDBACK

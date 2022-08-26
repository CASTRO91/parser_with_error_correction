import os
import re
import string
import ru_alphbet
import collections

with open(os.getcwd() + '\\files\\template_text\\big_eng_text.txt',
          encoding='utf-8') as task_text:
    row_text = task_text.read()
with open(os.getcwd() + '\\files\\template_text\\big_russian_text.txt',
          encoding='utf-8') as task_text_ru:
    row_text_ru = task_text_ru.read()
WORDS_eng = re.findall(r'[a-z-\']+', row_text.lower())
COUNTS_eng = collections.Counter(WORDS_eng)
WORDS_ru = re.findall(r'[а-я-\']+', row_text_ru.lower())
COUNTS_ru = collections.Counter(WORDS_ru)


def correct(language, word):
    try:
        if word[0].isdigit():
            return word
    except IndexError:
        pass
    if language == 0:
        COUNTS = COUNTS_eng
        alphabet = string.ascii_lowercase + string.digits + '-'
    else:
        alphabet = ru_alphbet.cyrillic_lowercase + string.digits + '-'
        COUNTS = COUNTS_ru
    # Поиск лучшего исправления ошибки для данного слова.
    # предрассчитать edit_distance==0, затем 1, затем 2; в противном случае оставить слово "как есть".
    candidates = (known(edits0(word), COUNTS) or
                  known(edits1(word, alphabet), COUNTS) or
                  known(edits2(word, alphabet), COUNTS) or
                  [word])

    return (max(candidates, key=COUNTS.get).upper() if word.isupper() else
            max(candidates, key=COUNTS.get).lower() if word.islower() else
            (max(candidates, key=COUNTS.get)).title() if word.istitle() else
            max(candidates, key=COUNTS.get))


def known(words, COUNTS):
    # Вернуть подмножество слов, которое есть в нашем словаре.
    return {w for w in words if w in COUNTS}


def edits0(word):
    # Вернуть все строки, которые находятся на edit_distance == 0 от word (т.е., просто само слово).
    return {word}


def edits2(word, alphabet):
    # Вернуть все строки, которые находятся на edit_distance == 2 от word.
    return {e2 for e1 in edits1(word, alphabet) for e2 in edits1(e1, alphabet)}


def edits1(word, alphabet):
    # Возвращает список всех строк на расстоянии edit_distance == 1 от word.
    pairs = splits(word)
    deletes = [a + b[1:] for (a, b) in pairs if b]
    transposes = [a + b[1] + b[0] + b[2:] for (a, b) in pairs if len(b) > 1]
    replaces = [a + c + b[1:] for (a, b) in pairs for c in alphabet if b]
    inserts = [a + c + b for (a, b) in pairs for c in alphabet]
    return set(deletes + transposes + replaces + inserts)


def splits(word):
    # Возвращает список всех возможных разбиений слова на пару (a, b).
    return [(word[:i], word[i:])
            for i in range(len(word) + 1)]


def deduplication(correct_text):
    l_text = []
    for text in correct_text:
        if text not in l_text:
            l_text.append(text)
    return l_text


def correct_list(language, list_text):
    correct_text = []
    deep_text = ''
    if len(list_text) == 1:
        return [correct(language, list_text[0])]
    else:
        for word in list_text:
            if ' ' not in word:
                correct_text.append(correct(language, word))
            else:
                word = word.split(' ')
                for deep_word in word:
                    deep_text += correct(language, deep_word) + ' '
                correct_text.append(''.join(deep_text.strip()))
                deep_text = ''
        return deduplication(correct_text)

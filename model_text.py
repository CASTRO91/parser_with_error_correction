import os


def open_text_file():
    with open(os.getcwd() + '\\files\\PythonTest.txt',
              encoding='utf-8') as task_text:
        row_text = task_text.readlines()
        return row_text


def write_text_file(file_language: str, text: str):
    if file_language == 'eng':
        file_name = 'English.txt'
    elif file_language == 'ru':
        file_name = 'Russian.txt'
    else:
        file_name = 'error.txt'
    with open(os.getcwd() + '\\files\\' + file_name, 'a', encoding='utf-8') as task_text:
        task_text.write(text + '\n')
    return print(f'{file_name} done: {text}' )


def remove_file():
    if os.path.exists(os.getcwd() + '\\files\\' + 'English.txt') and os.path.exists(
            os.getcwd() + '\\files\\' + 'Russian.txt'):
        os.remove(os.getcwd() + '\\files\\' + 'English.txt')
        os.remove(os.getcwd() + '\\files\\' + 'Russian.txt')


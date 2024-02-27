import requests
import random
import string
import time
import os

API = 'https://www.1secmail.com/api/v1/'
domains = [
  "1secmail.com",
  "1secmail.org",
  "1secmail.net",
  "wwjmp.com",
  "esiix.com",
  "xojxe.com",
  "yoggm.com"
]
domain = random.choice(domains)
timer = 5


def start():
    print('Приложение для создания временной электронной почты. '
          'Если сообщение не приходит попробуйте пересоздать почту\n'
          'Автор: https://github.com/itbert')
    start_command = input('Если вы готовы приступить к созданию временной (анонимной) электронной почты напишите '
                          'в чат: start\n')
    if start_command == 'start':
        main()
    else:
        print('Вы ввели команду неправильно или желаете изменить время. Программа перезапустится автоматически')
        start()


def create_user():
    symbols = string.ascii_lowercase + string.digits
    user = ''.join(random.choice(symbols) for i in range(10))
    return user


def check_email(email):
    req_link = f'{API}?action=getMessages&login={email.split("@")[0]}&domain={email.split("@")[1]}'
    r = requests.get(req_link).json()
    length = len(r)

    if length == 0:
        print('На почте нет писем...')
    else:
        id_list = []
        for i in r:
            for k, v in i.items():
                if k == 'id':
                    id_list.append(v)

        print(f'Вам пришло {length} сообщений')
        directory = os.getcwd()
        final_directory = os.path.join(directory, 'messages')

        if not os.path.exists(final_directory):
            os.makedirs(final_directory)
        for i in id_list:
            read_mess = f'{API}?action=readMessage&login={email.split("@")[0]}&domain={email.split("@")[1]}&id={i}'
            r = requests.get(read_mess).json()
            sender = r.get('from')
            subject = r.get('subject')
            date = r.get('date')
            content = r.get('textBody')
            email_pathfile = os.path.join(final_directory, f'{i}.txt')

            with open(email_pathfile, 'w') as file:
                file.write(f'Отправитель: {sender}\n'
                           f'Получатель: {email}\n'
                           f'Предмет: {subject}\n'
                           f'Дата отправки: {date}\n'
                           f'Сообщение: {content}')


def main():
    try:
        user = create_user()
        email = f'{user}@{domain}'
        print(f'Ваш временный почтовый адрес: {email}')

        email_request = requests.get(f'{API}?login={email.split("@")[0]}&domain={email.split("@")[1]}')

        while True:
            check_email(email=email)
            time.sleep(timer)

    except KeyboardInterrupt:
        print('Создание почтового адреса прервано...')


def delete(email=''):
    url = 'https://www.1secmail.com/mailbox'
    data = {'action': 'deleteMailbox', 'login': email.split('@')[0], 'domain': email.split('@')[1]}
    req = requests.post(url, data=data)
    print(f'Адрес {email} был удален...')


if __name__ == "__main__":
    start()

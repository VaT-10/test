import requests
import time

API_URL = 'https://api.telegram.org/bot'
TOKEN = '6798514474:AAFfj-qLZv7mAQTWvjq2daG8dtgQt4CDv2g'
TEXT = 'Ваше сообщение отправлено @VaTkac1'
offset_num = -2
line = []
checking = False
checking_id = None

while True:
    updates = requests.get(f'{API_URL}{TOKEN}/getUpdates?offset={offset_num + 1}').json()

    if updates.get('result'):
        for result in updates['result']:
            offset_num = result['update_id']
            if result.get('edited_message'):
                requests.get(
                    f"{API_URL}{TOKEN}/sendMessage?chat_id={result['edited_message']['chat']['id']}&text=Нельзя редактировать сообщения!")
            else:
                chat_id = result['message']['chat']['id']
                check = chat_id == 5873667382 and result['message']['text'] == '/check_updates'
                try:
                    result['message']['text']
                    flag = True
                    if not checking and not check:
                        line.append(result)
                        print(line)
                except KeyError:
                    requests.get(f'{API_URL}{TOKEN}/sendMessage?chat_id={chat_id}&text=Можно отправлять только текст!')
                    flag = False

                if flag:
                    if chat_id == 5873667382 and result['message']['text'] == '/check_updates':
                        checking = True
                        requests.get(
                            f'{API_URL}{TOKEN}/sendMessage?chat_id=5873667382&text=У вас {len(line)} новых сообщений!')
                        if line:
                            last_message = line.pop(0)
                        else:
                            requests.get(
                                f'{API_URL}{TOKEN}/sendMessage?chat_id=5873667382&text=Вы ответили на все сообщения!')
                            continue
                        checking_id = last_message['message']['chat']['id']
                        first_name = last_message['message']['from']['first_name']
                        if last_message['message']['from'].get('last_name'):
                            last_name = ' ' + last_message['message']['from']['last_name']
                        else:
                            last_name = ''
                        text = last_message['message']['text']
                        requests.get(
                            f'{API_URL}{TOKEN}/sendMessage?chat_id=5873667382&text={first_name}{last_name}: {text}')
                    elif chat_id == 5873667382 and checking:
                        requests.get(
                            f'{API_URL}{TOKEN}/sendMessage?chat_id={checking_id}&text=@VaTkac1 ответил: {result["message"]["text"]}')
                        if not line:
                            checking = False
                            requests.get(
                                f'{API_URL}{TOKEN}/sendMessage?chat_id=5873667382&text=Вы ответили на все сообщения!')
                            continue
                        else:
                            last_message = line.pop(0)
                        checking_id = last_message['message']['chat']['id']
                        first_name = last_message['message']['from']['first_name']
                        if last_message['message']['from'].get('last_name'):
                            last_name = ' ' + last_message['message']['from']['last_name']
                        else:
                            last_name = ''
                        text = last_message['message']['text']
                        requests.get(
                            f'{API_URL}{TOKEN}/sendMessage?chat_id=5873667382&text={first_name}{last_name}: {text}')

                    if not checking:
                        requests.get(f'{API_URL}{TOKEN}/sendMessage?chat_id={chat_id}&text={TEXT}')
                        cat_photo = requests.get('https://api.thecatapi.com/v1/images/search')
                        if cat_photo.status_code == 200:
                            requests.get(f'{API_URL}{TOKEN}/sendPhoto?chat_id={chat_id}&photo={cat_photo.json()[0]["url"]}')
                            requests.get(
                                f'{API_URL}{TOKEN}/sendMessage?chat_id={chat_id}&text=Посмотрите на котика, пока ждёте ответа :)')
                        else:
                            requests.get(
                                f'{API_URL}{TOKEN}/sendMessage?chat_id={chat_id}&text=Тут должно было быть фото котика, но что-то пошло не так...')
                        requests.get(
                            f'{API_URL}{TOKEN}/sendMessage?chat_id=5873667382&text=Вы получили новое сообщение!')
    now_end = False
    time.sleep(1)

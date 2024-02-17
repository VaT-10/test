import requests
import time

API_URL = 'https://api.telegram.org/bot'
TOKEN = '6798514474:AAFfj-qLZv7mAQTWvjq2daG8dtgQt4CDv2g'
TEXT = 'Ваше сообщение отправлено @VaTkac1'
offset_num = -2

while True:
    updates = requests.get(f'{API_URL}{TOKEN}/getUpdates?offset={offset_num + 1}').json()

    if updates.get('result'):
        for result in updates['result']:
            offset_num = result['update_id']
            if result.get('edited_message'):
                requests.get(f"{API_URL}{TOKEN}/sendMessage?chat_id={result['edited_message']['chat']['id']}&text=Нельяз редактировать сообщения!!!")
            else:
                chat_id = result['message']['chat']['id']
                try:
                    if result['message']['from'].get('last_name'):
                        print(f"Новое сообщение от {result['message']['from']['first_name']} {result['message']['from']['last_name']}: {result['message']['text']}")
                    else:
                        print(f"Новое сообщение от {result['message']['from']['first_name']}: {result['message']['text']}")
                    flag = True
                except KeyError:
                    requests.get(f'{API_URL}{TOKEN}/sendMessage?chat_id={chat_id}&text=Можно отправлять только текст!!!')
                    if result['message']['from'].get('last_name'):
                        print(f"{result['message']['from']['first_name']} {result['message']['from']['last_name']} попытался отправить не текст.. ну и зачем?")
                    else:
                        print(f"{result['message']['from']['first_name']} попытался отправить не текст.. ну и зачем?")
                    flag = False
                if flag:
                    requests.get(f'{API_URL}{TOKEN}/sendMessage?chat_id={chat_id}&text={TEXT}')
                    cat_photo = requests.get('https://api.thecatapi.com/v1/images/search')
                    if cat_photo.status_code == 200:
                        requests.get(f'{API_URL}{TOKEN}/sendPhoto?chat_id={chat_id}&photo={cat_photo.json()[0]["url"]}')
                        requests.get(f'{API_URL}{TOKEN}/sendMessage?chat_id={chat_id}&text=Посмотрите на котика, пока ждёте ответа :)')
                    else:
                        requests.get(f'{API_URL}{TOKEN}/sendMessage?chat_id={chat_id}&text=Тут должно было быть фото котика, но что-то пошло не так...')
                    requests.get(f'{API_URL}{TOKEN}/sendMessage?chat_id={chat_id}&text=@VaTkac1 ответил: {input("Введите свой ответ: ")}')
    time.sleep(1)
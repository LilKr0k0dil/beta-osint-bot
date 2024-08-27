#!/usr/bin/python3

import re 							# import re
import os 		 					# import os
import datetime
import telebot 						# Import telebot library
from telebot import types, util 			# Import types from telebot
import vk_api	
import hashlib
import requests
import json
import codecs
from telethon import TelegramClient, events
import asyncio
from intelxapi import intelx
import shodan 
import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Создание таблицы пользователей, если она не существует
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (id INTEGER PRIMARY KEY, chat_id INTEGER, phone_number TEXT, is_admin INTEGER DEFAULT 0, is_subscribed INTEGER DEFAULT 0)''')
conn.commit()

# Создание таблицы сообщений, если она не существует
cursor.execute('''CREATE TABLE IF NOT EXISTS messages
                  (id INTEGER PRIMARY KEY, chat_id INTEGER, message TEXT)''')
conn.commit()

# Команды для администратора
admin_commands = ['/block_access', '/view_requests', '/view_all_requests', '/view_all_users', '/set_subscription_limit', '/give_subscription']
admin_ids =[]
# Проверка прав доступа администратора
def check_admin_access(message):

    if message.chat.id in admin_ids:
        return True
    return False


api_id = "your_api_id without '' "
api_hash = "yuor_telegram_api hash"
bot = telebot.TeleBot('your_bot_token')
api = shodan.Shodan('your_shodan_api')

async def dataleaks(message):
    q = message.text
    rez = []
    client = TelegramClient('session_name', api_id, api_hash)
    await client.start()
    await client.send_message("data1eaks_bot", q)
    @client.on(events.NewMessage(from_users="data1eaks_bot"))
    async def handler(event):
      a = str(event.message.message)
      if 'найден' in a:
          if 'не найден' in a or 'Неверный ввод' in a:
             rez.append({"st":False,"data":""})
          else:
             rez.append({"st":True,"data":a})
          client.disconnect()
    await client.run_until_disconnected()
    return rez[0]['data']



async def poshuk(message):
    q = message.text
    rez = []
    client = TelegramClient('session_name', api_id, api_hash)
    await client.start()
    await client.send_message("ce_poshuk_bot", q)
    @client.on(events.NewMessage(from_users="ce_poshuk_bot"))
    async def handler(event):
      a = str(event.message.message)
      if '👉' in a or 'Результатів за запитом не знайдено' in a:
          if 'Результатів за запитом не знайдено' in a:
             rez.append({"st":False,"data":""})
          else:
             rez.append({"st":True,"data":a.split("👆")[0]})
          client.disconnect()
    await client.run_until_disconnected()
    return rez[0]['data']



def search_shodan(message):
    try:

        results = api.search(message.text)


        for i, result in enumerate(results['matches']):
            if i >= 5:
                break

            response = 'IP: {}\n{}'.format(result['ip_str'], result['data'])
            bot.reply_to(message, response)

    except shodan.APIError as e:
        bot.reply_to(message, 'Ошибка: {}'.format(e))

def intelxx(message):
    q = message.text
    intel = intelx('your_intelx_api')
    results = intel.search(q)
    intel.FILE_READ(results['records'][0]['systemid'], 0, results['records'][0]['bucket'], "file.txt")
    bot.send_document(message.chat.id, 'file.txt')
    os.remove('file.txt')
    

def print_json_data(data, prefix=""):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                print_json_data(value, prefix=f"{prefix}{key}: ")
            else:
                bot.send_message(chat_id, f"{prefix}{key}: {value}")
    elif isinstance(data, list):
        for index, item in enumerate(data):
            if isinstance(item, (dict, list)):
                print_json_data(item, prefix=f"{prefix}[{index}]: ")
            else:
                bot.send_message(chat_id, f"{prefix}[{index}]: {item}")
    else:
        bot.send_message(chat_id, f"{prefix}{data}")

def get_data_from_api(url):
    try:
        response = requests.get(url)

        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        return f"Ошибка при запросе {url}: {e}"
    except requests.exceptions.HTTPError as he:
        return f"Ошибка HTTP при запросе {url}: {he}"
    except requests.exceptions.JSONDecodeError as je:
        return f"Ошибка при декодировании JSON из {url}: {je}"
    except Exception as ex:
        return f"Ошибка при обработке {url}: {ex}"


def other_message9(message):
    q= message.text
    async def start(q):
        rez = []
        client = TelegramClient('session_name', api_id, api_hash).start('0')
        await client.start()
        await client.send_message("ce_poshuk_bot", q)
        @client.on(events.NewMessage(from_users="ce_poshuk_bot"))
        async def handler(event):
            a = str(event.message.message)
            if '👉' in a or 'Результатів за запитом не знайдено' in a:
                if 'Результатів за запитом не знайдено' in a:
                   rez.append({"st":False,"data":""})
                else:
                   rez.append({"st":True,"data":a.split("👆")[0]})
                client.disconnect()
        await client.run_until_disconnected()
        return rez[0]
    try:
        ce = asyncio.run(start(q))
        bot.send_message(message.chat.id, ce)
    except Exception as e:
        bot.send_message(message.chat.id, 'тех работы')


def agent(message):
    q= message.text
    r = requests.get(f"https://statsnet.co/_next/data/13qfJaxG1WkeV6ls3fji6/ru/search/kz/{q}.json?jurisdiction=kz&value={q}").json()
    pretty_print(r)
    def pretty_print(data, indent=0):
        output=''
        nested_output = None
        if isinstance(data, dict):
            for key, value in data.items():
                if value is not None:
                    output += f"{key.capitalize()}: +{value}\n"

        elif isinstance(data, list):
            for item in data:
                nested_output = pretty_print(item, indent)
                if nested_output is not None:
                    output += nested_output
        else:
            if data is not None:
                output+= f"{' ' * (indent + 4)}{data}\n"
        # Prepare the message text
        split = util.smart_split(output, chars_per_string=3000)
        for text in split:
            bot.send_message(message.chat.id, text)
    
    
def quick(message):
    query = message.text
    t = 'your_quick_osint_api'
    url = f'https://quickosintapi.com/api/v1/search/agregate/{query}'
    headers = {
                "Authorization": f"Bearer {t}",
                "X-ClientId": f"myClient-36560634"
    }
    response = requests.get(url, headers=headers)
    a = response.json()
    query = a['query']
    items = a['items']
        
        # Prepare the message text
    message_text = f"Query: {query}\n\n"
    for item in items:
        for key, value in item.items():
            if isinstance(value, list):
                value = ", ".join(value)
            message_text += f"{key.capitalize()}: {value}\n"

    message_text += "\n"
        
        # Send the message
    split = util.smart_split(message_text, chars_per_string=3000)
    for text in split:
        bot.send_message(message.chat.id, text) 

def gai(message):
    output =''
    data = message.text
    r = requests.get(f'https://baza-gai.com.ua/nomer/{data}', headers={"Accept": "application/json", "X-Api-Key": "gai_ua_api"})
    d = r['region']['name']
    output+= (d)
    d = r['vendor']
    d1 = r['model']
    output+=  d+'  ' +d1
    bot.send_message(message.chat.id, output)            
def encrypt_text(text):
    md5_hash = hashlib.md5()
    md5_hash.update(text.encode('utf-8'))
    encrypted_text = md5_hash.hexdigest()
    return encrypted_text
def vv(message):
    q = message.text 
    key4 = requests.get("https://api.vinformer.online/v8/?id=8e53DabotanalystQ5Zh&auth&decoder").json()["access"]["str4key"]
    text = key4 + 'de4dV34' 
    encrypted_text = encrypt_text(text)

    url = f"https://api.vinformer.online/v8/?id=8e53DabotanalystQ5Zh&vin={q}&key={encrypted_text}&decoder"
    vin =requests.get(url).json()
        
    def pretty_print(data, indent=0):
        output=''
        nested_output = None
        if isinstance(data, dict):
            for key, value in data.items():
                if value is not None:
                    output += f"{key.capitalize()}: +{value}\n"

        elif isinstance(data, list):
            for item in data:
                nested_output = pretty_print(item, indent)
                if nested_output is not None:
                    output += nested_output
        else:
            if data is not None:
                output+= f"{' ' * (indent + 4)}{data}\n"
        # Prepare the message text
        split = util.smart_split(output, chars_per_string=3000)
        for text in split:
            bot.send_message(message.chat.id, text)
    pretty_print(vin)
def main_KZ(message):
    q = message.text
    api_urls = [
        f"https://pk-api.adata.kz/api/v1/data/user/notes/by-company/?uin={q}&counterparty_type_code=company&order_direction=desc&page=1"
        f"https://pk-api.adata.kz/api/v1/data/participation-company/more/director/?id={q}&initial=1&page=1",
        f"https://pk-api.adata.kz/api/v1/data/participation-company/more/founder/?id={q}&initial=1&page=1",
        f"https://pk-api.adata.kz/api/v1/data/company/market/rating/?id={q}",
        f"https://pk-api.adata.kz/api/v1/data/company/status/?id={q}",
        f"https://pk-api.adata.kz/api/v1/data/company/short/?id={q}&initial=1&page=1",
        f"https://pk-api.adata.kz/api/v1/data/company/tax/short/?id={q}&initial=1",
        f"https://pk-api.adata.kz/api/v1/data/company/contact/more/?id={q}&initial=1&page=1",
        f"https://pk-api.adata.kz/api/v1/data/company/address/?id={q}&initial=1&page=1",
        f"https://pk-api.adata.kz/api/v1/data/company/nds/short/?id={q}&initial=1&page=1"
        f"https://pk-api.adata.kz/api/v1/data/company/director-company/short/?id={q}&initial=1&page=1",
        f"https://pk-api.adata.kz/api/v1/data/company/oked/more/?id={q}&initial=1&page=1",
        f"https://pk-api.adata.kz/api/v1/data/same-counterparty/more/other-companies/?id={q}&initial=1&page=1&type=Iin",
        f"https://pk-api.adata.kz/api/v1/data/counterparty-parse/?id={q}&entity_type=company",
        f"https://pk-api.adata.kz/api/v1/data/company/market/leader/?id={q}&initial=1",
        f"https://pk-api.adata.kz/api/v1/data/company/short/?id={q}&initial=1",
        f"https://pk-api.adata.kz/api/v1/data/company/zakup/goszakup/short/?initial=1&id={q}&type_id=1",
        f"https://pk-api.adata.kz/api/v1/data/company/contract/short/?initial=1&id={q}&type_id=1",
        f"https://pk-api.adata.kz/api/v1/data/company/zakup/nadloc/short/?initial=1&id={q}&type_id=1",
        f"https://pk-api.adata.kz/api/v1/data/company/zakup/unreliable-nis/short/?initial=1&id={q}&type_id=1",
        f"https://pk-api.adata.kz/api/v1/data/company/zakup/fms/short/?initial=1&id={q}&type_id=1",
        f"https://pk-api.adata.kz/api/v1/data/company/zakup/unreliable-samruk/short/?initial=1&id={q}&type_id=1",
        f"https://pk-api.adata.kz/api/v1/data/company/zakup/unreliable-goszakup/short/?initial=1&id={q}&type_id=1",
        f"https://pk-api.adata.kz/api/v1/data/company/zakup/samruk/short/?initial=1&id={q}&type_id=1",
        f"https://pk-api.adata.kz/api/v1/data/company/trustworthy/inactivity/?initial=1&id={q}&type_id=1"
        f"https://pk-api.adata.kz/api/v1/data/company/trustworthy/inactivity/?initial=1&id={q}&type_id=1",
        f"https://pk-api.adata.kz/api/v1/data/company/arrest/short/?initial=1&id={q}&type_id=1&type=Bin",
        f"https://pk-api.adata.kz/api/v1/data/company/tax-inspection/short/?initial=1&id={q}&type_id=1",
        f"https://pk-api.adata.kz/api/v1/data/company/enforcement-debt/short/?initial=1&id={q}&type_id=1",
        f"https://pk-api.adata.kz/api/v1/data/company/trustworthy/bankruptcy/?initial=1&id={q}&type_id=1",
        f"https://pk-api.adata.kz/api/v1/data/company/tax-debt/short/?initial=1&id={q}&type_id=1",
        f"https://pk-api.adata.kz/api/v1/data/company/liquidating-taxpayer/?initial=1&id={q}&type_id=1",
        f"https://pk-api.adata.kz/api/v1/data/company/trustworthy/unreliability/?initial=1&id={q}&type_id=1",
        f"https://pk-api.adata.kz/api/v1/data/company/zakup/taxpayers-workless/short/?initial=1&id={q}&type_id=1",
        f"https://pk-api.adata.kz/api/v1/data/same-counterparty/unreliable-companies/?initial=1&id={q}&type_id=1&type=Bin",
        f"https://pk-api.adata.kz/api/v1/data/director/trustworthy/short/?initial=1&id={q}&type_id=1",
        f"https://pk-api.adata.kz/api/v1/data/company/risk-degree/short/?initial=1&id={q}&type_id=1",
        f"https://pk-api.adata.kz/api/v1/data/company/sanction/short/?initial=1&id={q}&type_id=1",
        f"https://pk-api.adata.kz/api/v1/data/company/court-case/short/?initial=1&id={q}&type_id=1",
        f"https://pk-api.adata.kz/api/v1/data/company/esf-taxpayer/?initial=1&id={q}&type_id=1&type=Bin",
        f"https://pk-api.adata.kz/api/v1/data/company/trustworthy/?initial=1&id={q}",
        f"https://pk-api.adata.kz/api/v1/data/company/contract/short/?initial=1&id={q}",
        f"https://pk-api.adata.kz/api/v1/data/analytics/company/graph/pie/count/?id={q}&case_type=tru&type=supplier",
        f"https://pk-api.adata.kz/api/v1/data/company/zakup/nadloc/short/?initial=1&id={q}",
        f"https://pk-api.adata.kz/api/v1/data/company/zakup/unreliable-nis/short/?initial=1&id={q}",
        f"https://pk-api.adata.kz/api/v1/data/company/zakup/unreliable-mitwork/short/?initial=1&id={q}",
        f"https://pk-api.adata.kz/api/v1/data/company/zakup/unreliable-national-bank/short/?initial=1&id={q}",
        f"https://pk-api.adata.kz/api/v1/data/company/zakup/goszakup/short/?initial=1&id={q}",
        f"https://pk-api.adata.kz/api/v1/data/company/zakup/fms/short/?initial=1&id={q}",
        f"https://pk-api.adata.kz/api/v1/data/company/zakup/samruk/short/?initial=1&id={q}",
        f"https://pk-api.adata.kz/api/v1/data/company/zakup/unreliable-goszakup/short/?initial=1&id={q}",
        f"https://pk-api.adata.kz/api/v1/data/company/contract/graph/?initial=1&id={q}&type=customers&sorted_by=sum&type_id=1",
        f"https://pk-api.adata.kz/api/v1/data/company/zakup/unreliable-samruk/short/?initial=1&id={q}",
        f"https://pk-api.adata.kz/api/v1/data/analytics/company/graph/pie/count/?id={q}&case_type=contract&type=supplier",
        f"https://pk-api.adata.kz/api/v1/data/analytics/company/graph/pie/methods/?id={q}&type=supplier",
        f"https://pk-api.adata.kz/api/v1/data/analytics/company/graph/pie/count/?id={q}&case_type=contract&type=customer",
        f"https://pk-api.adata.kz/api/v1/data/analytics/company/graph/pie/count/?id={q}&case_type=tru&type=customer"
    ]

    global chat_id
    chat_id = message.chat.id

    for url in api_urls:
        data = get_data_from_api(url)
        if isinstance(data, dict) or isinstance(data, list):
            print_json_data(data)
        else:
            bot.send_message(chat_id, data)
        bot.send_message(chat_id, "-" * 30)

def x(message):
    output = ''
    q = message.text
    id = requests.post("https://kompra.kz/api/search/company?size=20",json={"code":"KZ","filter":{"inn":q}}).json()['content'][0]['id']
    r = requests.get(f'https://kompra.kz/open-company/{id}').json()
    r1 =r['lawAddress']
    output+= 'law ' + r1 + '\n'
    r2 =r['owner']
    r3 = r2['name']
    output+= 'owner ' + r3 + '\n'
    rx =r['oked']
    rx1 = requests.get(f'https://kompra.kz/api2/oked?oked_id={rx}').json()['name']
    output+= 'oked ' + rx1 + '\n'
    bot.send_message(message.chat.id, output)

def main_RU(message):
    q = message.text
    api_urls = [
        f"https://indicator.bifit.ru/api-portal/business-entities/search?query={q}&size=10&page=0&region=&economicActivity=&industry=&registeredAfter=&registeredBefore="
        f"https://indicator.bifit.ru/api-portal/business-entities/{q}/card",
        f"https://indicator.bifit.ru/api-portal//business-entities/{q}/markers",
        f"https://indicator.bifit.ru/api-portal/business-entities/{q}/finances/summary",
        f"https://indicator.bifit.ru/api-portal/business-entities/{q}/contracts/summary",
        f"https://indicator.bifit.ru/api-portal//business-entities/{q}/arbitration/summary?status=&type=&side=&registeredAfter=",
        f"https://indicator.bifit.ru/api-portal/business-entities/{q}/contracts?type=&size=10&page=0",
        f"https://indicator.bifit.ru/api-portal/business-entities/{q}/proceedings/summary",
        f"https://indicator.bifit.ru/api-portal/business-entities/{q}/finances/bookkeeping/summary-by-years",
        f"https://indicator.bifit.ru/api-portal/business-entities/proxy/nalogru/account/lock/{q}?isFromFns=false"
        f"https://indicator.bifit.ru/api-portal//business-entities/{q}/arbitration/summary?status=&type=&side=&registeredAfter=",
        f"https://indicator.bifit.ru/api-portal/business-entities/{q}/contracts?type=WON&size=10&page=0",
        f"https://indicator.bifit.ru/api-portal//business-entities/{q}/licenses?status=ACTIVE&size=10&page=0",
        f"https://indicator.bifit.ru/api-portal//business-entities/{q}/licenses/summary",
        f"https://indicator.bifit.ru/api-portal//business-entities/{q}/arbitration?status=active&type=&side=plaintiff&registeredAfter=&page=0",
        f"https://indicator.bifit.ru/api-portal/business-entities/{q}/proceedings?size=10&page=0",
        f"https://indicator.bifit.ru/api-portal/business-entities/{q}/inspections?kind=&category=&result=&size=10&page=0",
        f"https://indicator.bifit.ru/api-portal/business-entities/{q}/inspections/summary?kind=&category=&result="

    ]

    global chat_id
    chat_id = message.chat.id

    for url in api_urls:
        data = get_data_from_api(url)
        if isinstance(data, dict) or isinstance(data, list):
            print_json_data(data)
        else:
            bot.send_message(chat_id, data)
        bot.send_message(chat_id, "-" * 30)
    
def searching(message):
    data = message.text
    output = ''
    response = requests.get(
        f'https://iscerberus.ru/api/searching?value={data}&cerberusid=',
        headers={
            'Cookie': f"cauth="
        }
    )
    response_json = response.json()['html']

    
    # Write the HTML content to the output file
    with open('output.html', 'w') as f:
        f.write(response_json)

        # Prepare the message text
    with open('output.html', 'r') as f:
        bot.send_document(message.chat.id, f)
    os.remove('output.html')



def valid(message):
    mail = message.text
    url = f"https://api.smtp.bz/v1/check/email/{mail}"
    headers = {
        "accept": "application/json",
        "Authorization": ""}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()["result"]
        if data == True:
            bot.send_message(message.chat.id, "валидная")
        else:
            bot.send_message(message.chat.id, "не валидная")
    # Обработка данных
    else:
        bot.send_message("Ошибка при выполнении запроса:", response.status_code)


def calculate_age(birth_date):
    today = datetime.date.today()
    age = today.year - birth_date.year
    # Проверяем, был ли уже день рождения в текущем году
    if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
        age -= 1
    return age

def info_handler(message):
    # получение ссылки из сообщения

    screen_name = message.text.split('/')[-1]
    # авторизация в VK API
    vk_session = vk_api.VkApi(token="")

    vk = vk_session.get_api()

    # получение id пользователя из ссылки
    vk_id = vk.utils.resolveScreenName(screen_name=screen_name).get('object_id')

    # получение информации о пользователе
    user_info = vk.users.get(user_ids=vk_id, fields='sex, bdate, city, country, photo_max, domain, online, last_seen')[0]

    # вычисление возраста по дате рождения
    if 'bdate' in user_info:
        birth_date = datetime.datetime.strptime(user_info['bdate'], "%d.%m.%Y").date()
        age = calculate_age(birth_date)
        user_info['age'] = age

    # форматирование информации в строку
    output = f"👤 {user_info['first_name']} {user_info['last_name']} (https://vk.com/{user_info['domain']})\n"
    output += f"       ID: {user_info['id']}\n"
    if 'city' in user_info:
        output += f"       Город: {user_info['city']['title']}\n"
        if 'country' in user_info:
            output += f"       └─ ({user_info['country']['title']})\n"
    if 'bdate' in user_info:
        output += f"       День рождения: {user_info['bdate']}\n"
        if 'age' in user_info:
            output += f"       Возраст: {user_info['age']} лет\n"
    if 'online' in user_info:
        online_status = "Онлайн" if user_info['online'] == 1 else "Оффлайн"
        output += f"       {online_status}: {user_info['last_seen']['time']}\n"
        output += f"       ├─ {user_info['last_seen']['time']} дней и {user_info['last_seen']['time']} часа назад\n"

    output += f"       Создан: {user_info['first_name']} {user_info['last_name']}\n"
    output += f"       └─ {user_info['age']} лет и месяц назад\n"
    output += f"       Упоминания: Посмотреть (https://vk.com/feed?obj={user_info['id']}&q=&section=mentions)\n"
    output += f"       Web Archive: id{user_info['id']} (https://web.archive.org/web/*/https://vk.com/id{user_info['id']})\n"
    output += f"       Архивные базы: Посмотреть (https://t.me/VKHistoryRobot)\n"
    output += f"       Архив профиля: Посмотреть (https://vk.watch/{user_info['id']}/profile)\n"
    output += f"       Действия профиля: Посмотреть (https://onli-vk.ru/id{user_info['id']})\n"
    output += f"       Интересы: Посмотреть (http://ininterests.com/user{user_info['id']})\n"
    output += f"       Мой Мир: Посмотреть (https://my.mail.ru/vk/{user_info['id']})\n"
    output += f"       bigbookname: Посмотреть (https://bigbookname.com/user/id-{user_info['id']})\n"
    output += f"       topdb: Посмотреть (https://topdb.ru/id{user_info['id']})\n\n"

    # получение информации о друзьях пользователя
    friends = vk.friends.get(user_id=vk_id, fields='sex, bdate, city, country, photo_max, domain')['items']
    num_friends = len(friends)

    output += f"Друзей: {num_friends}\n"
    if num_friends > 0:
        online_friends = sum(1 for friend in friends if friend.get('online') == 1)
        output += f"Активных: {online_friends}\n\n"

    # получение информации о популярных городах пользователя
    cities = {}
    for friend in friends:
        if 'city' in friend:
            city = friend['city']['title']
            cities[city] = cities.get(city, 0) + 1

    if cities:
        output += "🏙 Популярные города\n"
        for city, count in sorted(cities.items(), key=lambda x: x[1], reverse=True):
            if count > 2:
                output += f"       {city} - {count} ~ {count / num_friends * 100:.0f} %\n"
        output += "\n"

    # получение информации о популярных школах пользователя
    schools = {}
    for friend in friends:
        if 'schools' in friend:
            for school in friend['schools']:
                school_name = school['name']
                schools[school_name] = schools.get(school_name, 0) + 1

    if schools:
        output += "🏫 Популярные школы\n"
        for school, count in sorted(schools.items(), key=lambda x: x[1], reverse=True):
            if count > 2:
                output += f"       {school} - {count} ~ {count / num_friends * 100:.0f} %\n"
        output += "\n"

    # получение информации о популярных ВУЗах пользователя
    universities = {}
    for friend in friends:
        if 'universities' in friend:
            for university in friend['universities']:
                university_name = university['name']
                universities[university_name] = universities.get(university_name, 0) + 1

    if universities:
        output += "👨‍🎓 Популярные ВУЗы\n"
        for university, count in sorted(universities.items(), key=lambda x: x[1], reverse=True):
            if count>2:
                output += f"       {university} - {count} ~ {count / num_friends * 100:.0f} %\n"
        output += "\n"

    # получение информации о популярных способах входа пользователя
    platforms = {}
    for friend in friends:
        if 'online_info' in friend:
            platform = friend['online_info']['platform']
            platforms[platform] = platforms.get(platform, 0) + 1

    if platforms:
        output += "📲 Популярные виды входа\n"
        for platform, count in sorted(platforms.items(), key=lambda x: x[1], reverse=True):
            if count >2:
                output += f"       {platform} - {count} ~ {count / num_friends * 100:.0f} %\n"
        output += "\n"

    # получение информации о популярных фамилиях пользователя
    last_names = {}
    for friend in friends:
        if 'last_name' in friend:
            last_name = friend['last_name']
            last_names[last_name] = last_names.get(last_name, 0) + 1

    if last_names:
        output += "👫 Популярные фамилии\n"
        for last_name, count in sorted(last_names.items(), key=lambda x: x[1], reverse=True):
            if count > 2:
                output += f"       {last_name} - {count}\n"
        output += "\n"



    # отправка сообщения с информацией в Telegram
    split = util.smart_split(output, chars_per_string=3000)
    for text in split:
        bot.send_message(message.chat.id, text)


#############################################################
######                    HANDLERS                     ######
#############################################################

@bot.message_handler(commands=['start'])
def start_message(message):
	# Command: /start
    bot.send_message(message.chat.id, 'Добро пожаловать в Bot Analyst. Это Информационная Аналитическая Система для поиска информации. Система проводит поиск по трем странам: Россия, Украина и Казахстан. Вы можете сделать поиск по:\nНомеру телефона:\n8999999999, +7999999999\nЭлектронной почте:\nnominal@gmail.com\nФИО: Номинальный Номинал Номиналович\nФИО+Дата рождения:\nНоминальный Номинал Номиналович 31.12.1999 или Номинальный Номинал Номиналович 1999.12.31\nФИО+Город:\nНоминальный Номинал Номиналович Москва\nФИ+Город:\nНоминальный Номинал Москва\nГос номер, VIN (Только по РФ и Украине)\nВ676ХМ777\nАК1234АВ\nZ94CT41DAHR556549\nИНН/КПП, ИИН, ОГРН, ОГРНИП:\n7719825349\nНаименование Компании:\nРОДЕКССТРОЙ\nVK:\nhttps://vk.com/kmizulina\nhttps://vk.com/id618472499\nTelegram:\n28148530\nOdnoklassniki:\nhttps://ok.ru/profile/572523960642\nInstagram:\nhttps://instagram.com/durov\nFacebook:\nhttps://www.facebook.com/durov\nhttps://www.facebook.com/profile.php?id=100087116036507\nIP:\n8.8.8.8\nsite.com:\ngoogle.com')


@bot.message_handler(func=lambda message: message.text.startswith("+7"))
def menu(message):
    bot.register_next_step_handler(message, other_messages5)

@bot.message_handler(func=lambda message: len(message.text.split()) == 3)
def menu(message):
    bot.register_next_step_handler(message, other_messages5)

@bot.message_handler(func=lambda message: len(message.text) == 17)
def vin(message):
    bot.register_next_step_handler(message, other_messages1)

@bot.message_handler(func=lambda message: message.text.startswith("https"))
def menu(message):
    bot.register_next_step_handler(message, vk)    
    
@bot.message_handler(func=lambda message: not message.text.startswith("https") and '.' in message.text)
def menu(message):
    bot.register_next_step_handler(message, inet)

@bot.message_handler(func=lambda message: message.text.isdigit())
def handle_numbers(message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton(text="ИНН", callback_data="button1")
    button2 = types.InlineKeyboardButton(text="ИИН", callback_data="button2")
    button3 = types.InlineKeyboardButton(text="ТГ", callback_data="button3")
    button4 = types.InlineKeyboardButton(text="НОМЕР", callback_data="button4")
    keyboard.add(button1, button2, button3, button4)
    bot.reply_to(message, "Вы отправили только цифры", reply_markup=keyboard)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.reply_to(message, "Неизвестная команда")


@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    phone_number = message.contact.phone_number
    save_user(message.chat.id, phone_number)  # Сохраняем пользователя в базе данных
    bot.reply_to(message, "что вы отправили ?")
    
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    if call.data == "button1":
        try:
            main_RU(call.message)
        except Exception as e:
            print(e)
        pass
    elif call.data == "button2":
        try:
            main_KZ(call.message)
        except Exception as e:
            print(e)
        pass

        try:
            x(call.message)
        except Exception as e:
            print(e)
        pass
    elif call.data == "button3":
        bot.send_message(call.message.chat.id, "Вы выбрали кнопку 3")
    elif call.data == "button4":
        other_messages5(call.message)
        
#@bot.message_handler(func=lambda message: message.text == 'боты')
#def menu(message):
#   bot.send_message(message.chat.id, 'Введите хз что')
#   bot.register_next_step_handler(message, other_message9)
@bot.message_handler(func=lambda message: True)
def valid(message):
    try:
        valid(message)
    except Exception as e:
        print (e)
    pass
def other_messages1(message):
    try:
        vv(message)
    except Exception as e:
        print (e)
        bot.send_message(message.chat.id, "проверьте корректность запроса")
    pass

def nomerror(message):
    try:
        gai(message)
    except Exception as e:
        print (e)
    pass
    b = asyncio.run(poshuk(message))
    bot.send_message(message.chat.id, b)
def vk(message):
    try:
        info_handler(message)
    except Exception as e:
        print (e)
    pass

def other_messages5(message):
    try:
        searching(message)
    except Exception as e:
        print (e)
    pass
    try:
        intelxx(message)
    except Exception as e:
        print (e)
    pass
    a = asyncio.run(dataleaks(message))
    b = asyncio.run(poshuk(message))
    bot.send_message(message.chat.id, a)
    bot.send_message(message.chat.id, b)
def inet(message):
    try:
        searching(message)
    except Exception as e:
        print (e)
    pass
    try:
        intelxx(message)
    except Exception as e:
        print (e)
    pass
    try:
        search_shodan(message)
    except Exception as e:
        print(e)
    pass

# Обработчик команд администратора
@bot.message_handler(func=lambda message: message.text in admin_commands and check_admin_access(message.chat.id))
def handle_admin_commands(message):
    command = message.text

    if command == '/block_access':
        # Блокировка доступа к боту
        chat_id = int(message.text.split()[1])  # Ввод ID пользователя в сообщении
        block_user_access(chat_id)
        bot.reply_to(message, "Доступ к боту заблокирован для пользователя")

    elif command == '/view_requests':
        # Просмотреть все запросы человека
        chat_id = int(message.text.split()[1])  # Ввод ID пользователя в сообщении
        user_requests = get_user_requests(chat_id)
        if user_requests:
            requests_text = "\n".join(user_requests)
            bot.reply_to(message, f"Запросы пользователя:\n{requests_text}")
        else:
            bot.reply_to(message, "У пользователя нет запросов")

    elif command == '/view_all_requests':
        # Просмотреть полную базу всех запросов
        all_requests = get_all_requests()
        if all_requests:
            requests_text = "\n".join(all_requests)
            bot.reply_to(message, f"Все запросы:\n{requests_text}")
        else:
            bot.reply_to(message, "Нет доступных запросов")

    elif command == '/view_all_users':
        # Просмотреть всю базу данных пользователей
        all_users = get_all_users()
        if all_users:
            users_text = "\n".join(all_users)
            bot.reply_to(message, f"Все пользователи:\n{users_text}")
        else:
            bot.reply_to(message, "Нет зарегистрированных пользователей")

    elif command == '/set_subscription_limit':
        # Установить ограничение на подписку
        limit = int(message.text.split()[1])  # Ввод ограничения в сообщении
        set_subscription_limit(limit)
        bot.reply_to(message, f"Ограничение на подписку установлено: {limit}")

    elif command == '/give_subscription':
        # Выдать подписку
        chat_id = int(message.text.split()[1])  # Ввод ID пользователя в сообщении
        give_subscription(chat_id)
        bot.reply_to(message, "Подписка выдана пользователю")

    else:
        bot.reply_to(message, "Неизвестная команда")

# Функция блокировки доступа к боту
def block_user_access(chat_id):
    cursor.execute("UPDATE users SET is_subscribed=0 WHERE chat_id=?", (chat_id,))
    conn.commit()

# Функция получения всех запросов пользователя
def get_user_requests(chat_id):
    cursor.execute("SELECT message FROM messages WHERE chat_id=?", (chat_id,))
    requests = cursor.fetchall()
    return [request[0] for request in requests]

# Функция получения всех запросов всех пользователей
def get_all_requests():
    cursor.execute("SELECT users.chat_id, users.username, messages.message FROM users JOIN messages ON users.chat_id = messages.chat_id")
    all_requests = cursor.fetchall()
    return [f"ID: {request[0]}, Username: {request[1]}, Запрос: {request[2]}" for request in all_requests]

# Функция получения всех пользователей
def get_all_users():
    cursor.execute("SELECT * FROM users")
    all_users = cursor.fetchall()
    return [f"ID: {user[0]}, Username: {user[2]}, Номер: {user[3]}, Подписка: {'Да' if user[4] else 'Нет'}" for user in all_users]

# Функция установки ограничения на подписку
def set_subscription_limit(limit):
    cursor.execute("UPDATE users SET is_subscribed=0 WHERE is_subscribed=1 LIMIT ?", (limit,))
    conn.commit()

# Функция выдачи подписки
def give_subscription(chat_id):
    cursor.execute("UPDATE users SET is_subscribed=1 WHERE chat_id=?", (chat_id,))
    conn.commit()



@bot.message_handler(func=lambda message: True)
def handle_message(message):
    save_message(message.chat.id, message.text)  # Сохраняем сообщение в базе данных
    bot.reply_to(message, "Сообщение сохранено")

def save_user(chat_id, phone_number):
    # Проверяем, есть ли пользователь уже в базе данных
    cursor.execute("SELECT * FROM users WHERE chat_id=?", (chat_id,))
    user = cursor.fetchone()
    if user is None:
        # Если пользователь не найден, добавляем его в базу данных
        cursor.execute("INSERT INTO users (chat_id, phone_number) VALUES (?, ?)", (chat_id, phone_number))
    else:
        # Если пользователь уже существует, обновляем его номер телефона
        cursor.execute("UPDATE users SET phone_number=? WHERE chat_id=?", (phone_number, chat_id))
    conn.commit()

def save_message(chat_id, message):
    cursor.execute("INSERT INTO messages (chat_id, message) VALUES (?, ?)", (chat_id, message))
    conn.commit()
    
if __name__ == '__main__':
	# Start polling bot
	print('[+] Bot is starting: @sednt_bot')
	print('[+] Ctrl+C for stop polling')
	
# alert about bot polling for admins
	bot.infinity_polling()

conn.close()
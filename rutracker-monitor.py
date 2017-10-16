import requests
from datetime import datetime
from bs4 import BeautifulSoup
import time

urls = []
urls.append('https://rutracker.net/forum/tracker.php?f=2366') # HD TV Series
urls.append('https://rutracker.net/forum/tracker.php?f=2198') # HD Videos

UPDATE_PERIOD = 30 # secs
SILENT_PERIOD = (23, 9) # from 23:00 to 09:00

payload = {'login_username': 'sergt3',
           'login_password': 'pcuser',
	   'redirect': 'index.php',
           'login': 'вход'}
login_url = 'https://rutracker.net/forum/login.php'

# Telegram
TOKEN = "276848346:AAFhAlZ8JIc1MYW4nSwa1mDkgqmxFzFYyKk"
bot_url = "https://api.telegram.org/bot%s/"%TOKEN

def get_updates_json(request):
    #import pdb; pdb.set_trace()
    print("get_updates");
    response = requests.get(request + 'getUpdates')
    return response.json()


def last_update(data):
    results = data['result']
    total_updates = len(results) - 1
    return results[total_updates]

def get_chat_id(update):
    chat_id = update['message']['chat']['id']
    return chat_id

def send_mess(chat, text):
    print("send_mess");
    params = {'chat_id': chat, 'text': text, 'parse_mode':'HTML'}
    response = requests.post(bot_url + 'sendMessage', data=params)
    return response

def send_image(chat, text):
    print("send_image");
    params = {'chat_id': chat, 'photo': text}
    response = requests.post(bot_url + 'sendPhoto', data=params)
    return response

def get_poster_url(tag):
    topic_href = 'https://rutracker.net/forum/'+tag.attrs['href']
    resp = s.get(topic_href)
    soup = BeautifulSoup(resp.text, 'html.parser')
    try:
        rows = soup.select('.postImg.postImgAligned.img-right')[0].attrs['title']
        return rows
    except IndexError:
        pass

last_check_time = datetime.now().timestamp()

while True:
    try:
        with requests.Session() as s:
            resp = s.post(login_url, data=payload)

            while True:
                time.sleep(UPDATE_PERIOD)
                now = datetime.now()
                print(now)
                if now.hour >= SILENT_PERIOD[0] or now.hour < SILENT_PERIOD[1]:
                    print("Silent period")
                else:
                    for url in urls:
                        print("while post");
                        resp = s.post(url)

                        soup = BeautifulSoup(resp.text, 'html.parser')
                        rows = soup.select('#tor-tbl tr')

                        for row in rows:
                            try:
                                name = row.select('.tLink')[0]
                                # img_url = get_poster_url(name)
                                # chat_id = get_chat_id(last_update(get_updates_json(bot_url)))
                                # send_image(chat_id, img_url)

                                name = str(name).replace('viewtopic', 'https://rutracker.net/forum/viewtopic')
                                timestamp = int(row.select('td')[-1].select('u')[0].contents[0])

                                # chat_id = get_chat_id(last_update(get_updates_json(bot_url)))
                                # send_mess(chat_id, name)

                            except IndexError:
                                pass
                            else:
                                if timestamp > last_check_time:
                                    print(timestamp, name)
                                    try:
                                        chat_id = get_chat_id(last_update(get_updates_json(bot_url)))
                                    except:
                                        print("Get chat_id exception")
                                        pass
                                    else:
                                        send_mess(chat_id, name)
                                # else:
                                #     chat_id = get_chat_id(last_update(get_updates_json(bot_url)))
                                #     send_mess(chat_id, '[inline URL](http://www.example.com/)')

                    last_check_time = datetime.now().timestamp()
    except:
        print("Top exception")



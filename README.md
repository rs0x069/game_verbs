# Бот-помощник онлайн-издательства "Игра слов"
Бот-помощник онлайн-издательства "Игра слов" для VK и Telegram, который отвечает на типичные вопросы пользователей. 
Бот обучаем нейросетью. 
Бот работает на сервисе [Heroku](https://heroku.com/).

## Требования
Python 3.8, 3.9 или 3.10.

### Зависимые модули
* google-cloud-dialogflow==2.14.0
* python-dotenv==0.20.0
* python-telegram-bot==13.12
* requests==2.27.1
* vk-api==11.9.8

## Предварительные требования
1. Для телеграм бота необходимо создать бота в Телеграм и получить токен. Разрешить боту отправлять вам уведомления.
2. Для бота в VK необходимо создать сообщество в VK. В настройках сообщества включить сообщения и создать ключ API. Пользователям нужно разрешить сообществу отправлять им сообщения.
3. На Google Cloud Platform создать проект, создать ключ API и скачать его в виде файла, создать агента в DialoFlow и обучить его.
Для обучения агента можно запустить скрипт `manage_intents.py`, которые обучит его фразами и ответами из файла `questions.json`. 

## Установка
* Склонировать проект
```commandline
https://github.com/rs0x069/game_verbs.git
```
* Перейти в папку `game_verbs`
* Установить пакеты
```commandline
pip install -r requirements.txt
```
* Создать файл `.env` со следующими переменными окружения:
  + TELEGRAM_TOKEN - токен телеграм бота.
  + TELEGRAM_RECIPIENT_CHAT_ID - id чата в Телеграм, в который бот будет отправлять ошибки. 
  + VK_TOKEN - ключ API из VK.
  + GOOGLE_APPLICATION_CREDENTIALS - имя файла с регистрационными данными из Google Cloud Platform. Этот файл должен лежать в папке проекта.
  + GOOGLE_DIALOGFLOW_PROJECT_ID - код проекта в Google Cloud Platform

## Использование
* Для запуска телеграм бота запустить скрипт `bot_tg.py`
```commandline
python bot_tg.py
```
* Для запуска бота VK запустить скрипт `bot_vk.py`
```commandline
python bot_vk.py
```
* Для обучения агента в DialogFlow фразами и ответами из файла `questions.json` запустить скрипт `manage_intents.py` 
```commandline
python manage_intents.py
```
Можно указать путь вручную, для этого нужно воспользоваться аргументом `-f` или `--file_name`:
```commandline
python manage_intents.py -f /path/filename.json
```
Пример файла:
```json
{
  "Устройство на работу": {
    "questions": [
      "Как устроиться к вам на работу?",
      "Как устроиться к вам?",
      "Хочу работать редактором у вас",
    ],
    "answer": "Если вы хотите устроиться к нам, напишите на почту game-of-verbs@gmail.com ..."
  },
  ...
}
```

## Запуск в Докер
* На компьютере должен быть установлен `docker`
* Подготовить файл с переменными окружения `.env` (описание переменных см. в разделе [Установка](#установка))
* Положить файл с регистрационными данными из Google Cloud Platform в папку с проектом и указать имя этого файла в файле `.env` в переменной `GOOGLE_APPLICATION_CREDENTIALS`. Можно так же можно прокинуть этот файл как `volume` в докер-контейнер в директорию `/app/`
* Находясь в папке с проектом выполнить команду `docker compose up -d`. Запустятся боты telegram и vk
* Если в качестве `command` указать `telegram`, то запустится бот telegram, если указать `vk`, то запустится бот vk (см. [пример](#пример-файла-docker-composeyml) файла docker-compose.yml) 

### Пример файла docker-compose.yml
```yaml
version: '3.9'

services:
  bot_telegram:
    build: .
    command: telegram
    env_file:
      - ./.env

  bot_vk:
    build: .
    command: vk
    env_file:
      - ./.env
```

## Примеры
#### Пример результата для Telegram:
![Пример результата для Telegram](https://raw.githubusercontent.com/rs0x069/game_verbs/main/.github/images/demo_tg_bot.gif)

#### Пример результата для ВКонтакте:
![Пример результата для ВКонтакте](https://raw.githubusercontent.com/rs0x069/game_verbs/main/.github/images/demo_vk_bot.gif)


***
Учебный проект для курсов web-разработчиков [dvmn](https://dvmn.org). 

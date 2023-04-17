import requests

from library_service import settings


def send_to_telegram(message: str) -> None:
    api_url = f'https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage'

    response = requests.post(api_url, json={'chat_id': settings.CHAT_ID, 'text': message})
    print(response.text)

import os

from dotenv import load_dotenv
import requests
import argparse

load_dotenv()


def shorten_link(token, url):
    """Create shorten link."""
    payload = {
        'Authorization': f'Bearer {token}',
    }
    long_link = {
        'long_url': url,
    }
    created_link = requests.post(
        url='https://api-ssl.bitly.com/v4/bitlinks',
        json=long_link,
        headers=payload
    )
    created_link.raise_for_status()
    return created_link.json()['id']


def count_clicks(token, url):
    """Count clics."""
    payload = {
        'Authorization': f'Bearer {token}',
    }
    clicks_count = requests.get(
        url=f'https://api-ssl.bitly.com/v4/bitlinks/{url}/clicks/summary',
        headers=payload
    )
    clicks_count.raise_for_status()
    return clicks_count.json()['total_clicks']


def is_bitlink(token, url):
    """Checking is bitlink."""
    payload = {
        'Authorization': f'Bearer {token}',
    }
    bitlink_information = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{url}',
        headers=payload
    )
    return bitlink_information.ok


if __name__ == '__main__':
    bitly_token = os.getenv('BITLY_TOKEN')
    parser = argparse.ArgumentParser()
    parser.add_argument('user_input', help='link')
    args = parser.parse_args()
    user_input = args.user_input
    # user_input = input()
    if is_bitlink(bitly_token, user_input):
        try:
            clicks_count = count_clicks(bitly_token, user_input)
        except requests.exceptions.HTTPError:
            print('Вы ввели неправильную ссылку или неверный токен.')
        else:
            print(clicks_count)
    else:
        try:
            bitlink = shorten_link(bitly_token, user_input)
        except requests.exceptions.HTTPError:
            print('Вы ввели неправильную ссылку или неверный токен.')
        else:
            print('Битлинк', bitlink)

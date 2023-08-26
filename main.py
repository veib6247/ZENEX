import logging

import requests

# init logging
logging.basicConfig(
    format='%(asctime)s-%(levelname)s: %(message)s',
    level=logging.INFO
)

# init domain
subdomain = 'payretosupport'
domain = 'zendesk.com'
url = f'https://{subdomain}.{domain}'


def main():
    try:
        response = requests.get(url)
        match response.status_code:
            case 200:
                logging.info(response.text)

            case _:
                logging.error(f'got http: {response.status_code}')

    except Exception as e:
        logging.error(e)


if __name__ == '__main__':
    main()

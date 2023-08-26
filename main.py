import logging
import os

import requests
from dotenv import load_dotenv

load_dotenv()

# init logging
logging.basicConfig(
    format='%(asctime)s-%(levelname)s: %(message)s',
    level=logging.INFO
)

# init domain
subdomain = 'payretosupport'
domain = 'zendesk.com'
url = f'https://{subdomain}.{domain}'
endpoint_search = '/api/v2/search.json'  # GET
endpoint_tickets = '/api/v2/tickets'  # GET


def main():
    zd_user_email = os.getenv('ZD_EMAIL')
    zd_token = os.getenv('ZD_TOKEN')
    query_params = {'query': 'type:ticket status:pending'}

    try:
        response = requests.get(
            f'{url}{endpoint_tickets}',
            auth=(f'{zd_user_email}/token', zd_token),
            params=query_params
        )

        match response.status_code:
            case 200:
                payload = dict(response.json())
                ticket_list = payload.get('tickets')

                for ticket in ticket_list:
                    logging.info(ticket)

                logging.info(f'Displayed {len(ticket_list)} tickets')

            case _:
                logging.error(f'got http: {response.status_code}')

    except Exception as e:
        logging.error(e)


if __name__ == '__main__':
    main()

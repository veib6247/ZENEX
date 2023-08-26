import logging
import os

import requests
from dotenv import load_dotenv


class Zenex:
    def __init__(self, domain: str, subdomain: str, zd_user_email: str, zd_token: str) -> None:
        self.subdomain = subdomain
        self.domain = domain
        self.zd_user_email = zd_user_email
        self.zd_token = zd_token

        # init logging
        logging.basicConfig(
            format='ZENEX - %(asctime)s - %(levelname)s: %(message)s',
            level=logging.INFO
        )

    def get_url(self):
        return f'https://{self.subdomain}.{self.domain}'

    def search_tickets(self, query_params: str):
        # https://developer.zendesk.com/api-reference/ticketing/ticket-management/search/

        try:
            res = requests.get(
                f'{self.get_url()}/api/v2/search.json',
                auth=(f'{self.zd_user_email}/token', self.zd_token),
                params={
                    'query': query_params,
                    'page': 1
                }
            )

            match res.status_code:
                case 200:
                    payload = dict(res.json())
                    list_of_tickets = payload.get('results')

                    logging.info(
                        f'{len(list_of_tickets)} tickets in the current page from the "results" object'
                    )
                    logging.info(f"count: {payload.get('count')}")
                    logging.info(f"facets: {payload.get('facets')}")
                    logging.info(f"next_page: {payload.get('next_page')}")
                    logging.info(
                        f"previous_page: {payload.get('previous_page')}"
                    )

                    return payload

                case _:
                    logging.error(f'http {res.status_code}')
                    logging.error(res.text)
                    exit()

        except Exception as e:
            logging.exception(e)
            exit()


def main():
    load_dotenv()
    zd_user_email = os.getenv('ZD_EMAIL')
    zd_token = os.getenv('ZD_TOKEN')

    query_params = 'type:ticket status:open'

    zd = Zenex(
        domain='zendesk.com',
        subdomain='payretosupport',
        zd_user_email=zd_user_email,
        zd_token=zd_token
    )

    zd.search_tickets(query_params)


if __name__ == '__main__':
    main()

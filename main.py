import json
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
        self.enable_logging = True

        # init logging
        logging.basicConfig(
            format='ZENEX - %(asctime)s - %(levelname)s: %(message)s',
            level=logging.INFO
        )

    def config(self, enable_logging: bool):
        self.enable_logging = enable_logging

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

            # Zendesk limits the result to only 100 item per request, pagination required to get everything
            match res.status_code:
                case 200:
                    payload = dict(res.json())

                    if self.enable_logging:
                        list_of_tickets = payload.get('results')
                        page_ticket_count = len(list_of_tickets)
                        count = payload.get('count')
                        facets = payload.get('facets')
                        next_page = payload.get('next_page')
                        previous_page = payload.get('previous_page')

                        logging.info(f"count: {count}")
                        logging.info(f"facets: {facets}")
                        logging.info(f"next_page: {next_page}")
                        logging.info(f"previous_page: {previous_page}")
                        logging.info(
                            f'{page_ticket_count} tickets in the current page from the "results" object'
                        )

                    return payload

                case _:
                    if self.enable_logging:
                        logging.error(f'HTTP {res.status_code} - {res.reason}')
                        logging.error(res.text)

                    else:
                        return {'error': res.text}

        except Exception as e:
            logging.exception(e)
            exit()

    def get_exportable_tickets(self, query_params: str):
        # https://developer.zendesk.com/api-reference/ticketing/ticket-management/search/#export-search-results

        try:
            res = requests.get(
                f'{self.get_url()}/api/v2/search/export',
                auth=(f'{self.zd_user_email}/token', self.zd_token),
                params={'query': query_params, 'filter[type]': 'ticket'}
            )

            # still limited to 100 result items
            match res.status_code:
                case 200:
                    payload = dict(res.json())

                    if self.enable_logging:
                        list_of_tickets = payload.get('results')
                        page_ticket_count = len(list_of_tickets)

                        facets = payload.get('facets')
                        meta = payload.get('meta')
                        links = payload.get('links')

                        logging.info(f"facets: {facets}")
                        logging.info(f"meta: {json.dumps(meta,indent=4)}")
                        logging.info(f"links: {json.dumps(links,indent=4)}")
                        logging.info(
                            f'{page_ticket_count} tickets in the current page from the "results" object'
                        )

                    return payload

                case _:
                    if self.enable_logging:
                        logging.error(f'HTTP {res.status_code} - {res.reason}')
                        logging.error(res.text)

                    else:
                        return {'error': res.text}

        except Exception as e:
            logging.exception(e)
            exit()


def main():
    load_dotenv()
    zd_user_email = os.getenv('ZD_EMAIL')
    zd_token = os.getenv('ZD_TOKEN')

    zd = Zenex(
        domain='zendesk.com',
        subdomain='payretosupport',
        zd_user_email=zd_user_email,
        zd_token=zd_token
    )

    searchable = zd.search_tickets('type:ticket status:closed')
    with open('searchable.json', 'w') as file:
        file.write(json.dumps(searchable))

    # exportable = zd.get_exportable_tickets('status:closed')
    # with open('exportable.json', 'w') as file:
    #     file.write(json.dumps(exportable))


if __name__ == '__main__':
    main()

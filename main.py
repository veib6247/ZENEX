import json
import logging
import os
import time

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
        return self

    def get_url(self):
        return f'https://{self.subdomain}.{self.domain}'

    def timer(func):
        """Used as decorator for timing internal methods"""

        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)  # sandwich me!
            end_time = time.time()
            logging.info(
                f'Task finished in {start_time-end_time} seconds'
            )

            return result

        return wrapper

    @timer
    def list_tickets(self):
        """Just list your tickets bruh.."""

        try:
            res = requests.get(
                f'{self.get_url()}/api/v2/tickets',
                auth=(f'{self.zd_user_email}/token', self.zd_token),
                params={
                    'sort_by': 'created_at',
                    'sort_order': 'desc'
                }
            )

            match res.status_code:
                case 200:
                    payload = dict(res.json())

                    if self.enable_logging:
                        logging.info(json.dumps(payload, indent=4))

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

    @timer
    def search_tickets(self, query_params: str):
        """
        Returns the 1st page of the query.

        https://developer.zendesk.com/api-reference/ticketing/ticket-management/search
        """

        try:
            res = requests.get(
                f'{self.get_url()}/api/v2/search.json',
                auth=(f'{self.zd_user_email}/token', self.zd_token),
                params={
                    'query': query_params,
                    'sort_by': 'created_at',
                    'sort_order': 'desc',
                    'page': 1
                }
            )

            match res.status_code:
                case 200:
                    payload = dict(res.json())

                    if self.enable_logging:
                        payload_copy = payload.copy()
                        list_of_tickets = payload_copy.get('results')
                        page_ticket_count = len(list_of_tickets)

                        del payload_copy['results']
                        logging.info(json.dumps(payload_copy, indent=4))

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

    @timer
    def get_exportable_tickets(self, query_params: str):
        """
        Return 1st page of the query using the export endpoint.

        "This endpoint is for search queries that will return more than 1000 results. The result set is ordered only by
        the created_at attribute."

        https://developer.zendesk.com/api-reference/ticketing/ticket-management/search/#export-search-results
        """

        try:
            res = requests.get(
                f'{self.get_url()}/api/v2/search/export',
                auth=(f'{self.zd_user_email}/token', self.zd_token),
                params={
                    'query': query_params,
                    'filter[type]': 'ticket'
                }
            )

            match res.status_code:
                case 200:
                    payload = dict(res.json())

                    if self.enable_logging:
                        payload_copy = payload.copy()

                        list_of_tickets = payload_copy.get('results')
                        page_ticket_count = len(list_of_tickets)

                        # remove the results object when logging to not flood the terminal
                        del payload_copy['results']
                        logging.info(json.dumps(payload_copy, indent=4))

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

    @timer
    def get_id_context(self, resource: str, context_id: str):
        """Take in a resource and the ID. Valid resources are users, ticket_fields, brands, organizations, groups."""

        try:
            res = requests.get(
                f'{self.get_url()}/api/v2/{resource}/{context_id}.json',
                auth=(f'{self.zd_user_email}/token', self.zd_token)
            )

            match res.status_code:
                case 200:
                    payload = dict(res.json())

                    if self.enable_logging:
                        logging.info(json.dumps(payload, indent=4))

                    else:
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

    # instantiate class
    zd = Zenex(
        domain='zendesk.com',
        subdomain='payretosupport',
        zd_user_email=zd_user_email,
        zd_token=zd_token
    )

    searchable = zd.search_tickets('type:ticket status:closed')
    with open('downloads/searchable.json', 'w') as file:
        file.write(json.dumps(searchable))

    # exportable = zd.get_exportable_tickets('status:closed')
    # with open('downloads/exportable.json', 'w') as file:
    #     file.write(json.dumps(exportable))

    # ticket_list = zd.config(enable_logging=False).list_tickets()
    # with open('downloads/list.json', 'w') as file:
    #     file.write(json.dumps(ticket_list))

    # results = zd.config(enable_logging=False).get_id_context(
    #     resource='users', context_id='900120880703')
    # logging.info(results)
    # zd.get_id_context(resource='ticket_fields', context_id='16862464937369')
    # zd.get_id_context(resource='brands', context_id='900000066203')
    # zd.get_id_context(resource='organizations', context_id='900001325246')


if __name__ == '__main__':
    main()

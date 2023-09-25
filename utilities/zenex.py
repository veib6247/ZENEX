import json
import logging
import time

import requests


# decorator for your methods
def timer(func):
    """Used as decorator for timing internal methods"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)  # sandwich me!
        end_time = time.time()
        logging.info(
            f'Task finished in {end_time - start_time} seconds'
        )

        return result

    return wrapper


# ze main class
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

    @timer
    def list_tickets(self):
        """Just list your tickets bruh"""

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
    def search_tickets(self, query_params: str, next_page: str):
        """
        Returns the 1st page of the query.

        https://developer.zendesk.com/api-reference/ticketing/ticket-management/search
        """

        try:
            if not next_page:
                res = requests.get(
                    f'{self.get_url()}/api/v2/search.json',
                    auth=(f'{self.zd_user_email}/token', self.zd_token),
                    params={
                        'query': query_params
                    }
                )

            else:
                logging.info('Querying the next page...')
                res = requests.get(
                    next_page,
                    auth=(f'{self.zd_user_email}/token', self.zd_token)
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
    def get_exportable_tickets(self, query_params: str, next_page: str):
        """
        Return 1st page of the query using the export endpoint.

        "This endpoint is for search queries that will return more than 1000 results. The result set is ordered only by
        the created_at attribute."

        https://developer.zendesk.com/api-reference/ticketing/ticket-management/search/#export-search-results
        """

        try:
            if not next_page:
                res = requests.get(
                    f'{self.get_url()}/api/v2/search/export',
                    auth=(f'{self.zd_user_email}/token', self.zd_token),
                    params={
                        'query': query_params,
                        'filter[type]': 'ticket'
                    }
                )

            else:
                logging.info('Querying next page...')
                res = requests.get(
                    next_page,
                    auth=(f'{self.zd_user_email}/token', self.zd_token),
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

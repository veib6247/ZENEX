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
                    'sort_by': 'created_at',
                    'sort_order': 'desc',
                    'page': 1
                }
            )

            # Zendesk limits the result to only 100 item per request, pagination required to get everything
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

    def get_exportable_tickets(self, query_params: str):
        # https://developer.zendesk.com/api-reference/ticketing/ticket-management/search/#export-search-results
        # "This endpoint is for search queries that will return more than 1000 results. The result set is ordered only by the created_at attribute."

        try:
            res = requests.get(
                f'{self.get_url()}/api/v2/search/export',
                auth=(f'{self.zd_user_email}/token', self.zd_token),
                params={
                    'query': query_params,
                    'filter[type]': 'ticket'
                }
            )

            # still limited to 100 result items
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

    def show_user(self, user_id: str):
        # https://developer.zendesk.com/api-reference/ticketing/users/users/#show-user

        try:
            res = requests.get(
                f'{self.get_url()}/api/v2/users/{user_id}.json',
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

    def show_field(self, ticket_field_id: str):
        # https://developer.zendesk.com/api-reference/ticketing/tickets/ticket_fields/#show-ticket-field

        try:
            res = requests.get(
                f'{self.get_url()}/api/v2/ticket_fields/{ticket_field_id}.json',
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

    def show_brand(self, brand_id: str):
        # https://developer.zendesk.com/api-reference/ticketing/account-configuration/brands/#show-a-brand

        try:
            res = requests.get(
                f'{self.get_url()}/api/v2/brands/{brand_id}.json',
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

    def show_organization(self, organization_id):
        # https://developer.zendesk.com/api-reference/ticketing/organizations/organizations/#show-organization

        try:
            res = requests.get(
                f'{self.get_url()}/api/v2/organizations/{organization_id}.json',
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

    def show_group(self, group_id):
        # https://developer.zendesk.com/api-reference/ticketing/groups/groups/#show-group

        try:
            res = requests.get(
                f'{self.get_url()}/api/v2/groups/{group_id}.json',
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

    zd = Zenex(
        domain='zendesk.com',
        subdomain='payretosupport',
        zd_user_email=zd_user_email,
        zd_token=zd_token
    )

    # searchable = zd.search_tickets('type:ticket status:closed')
    # with open('data/searchable.json', 'w') as file:
    #     file.write(json.dumps(searchable))

    # exportable = zd.get_exportable_tickets('status:closed')
    # with open('data/exportable.json', 'w') as file:
    #     file.write(json.dumps(exportable))

    # zd.show_user('901178672543')
    # zd.show_field('16862464937369')
    # zd.show_brand('900000066203')
    # zd.show_organization('900001325246')
    zd.show_group('900000372563')


if __name__ == '__main__':
    main()

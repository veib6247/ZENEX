import logging
import os

import pandas as pd
from dotenv import load_dotenv

from utilities.zenex import Zenex

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

columns = [
    'CREATED_AT',
    'ID',
    'SOURCE_NAME',
    'CLIENT_NAME',
    'CONNECTOR',
    'SUBJECT',
    'DESCRIPTION',
    'LEVEL',
    'STATUS'
]

df = pd.DataFrame(columns=columns)


def main():

    generate_data(new_next_page='')

    # searchable = zd.search_tickets(
    #     query_params='type:ticket created>2023-09-01',
    #     next_page=''
    # )

    # with open('downloads/searchable.json', 'w') as file:
    #     file.write(json.dumps(searchable))

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


def generate_data(new_next_page: str):
    try:
        exportable = zd.config(enable_logging=False).search_tickets(
            query_params='type:ticket created>2023-08-31',
            next_page=new_next_page
        )

        if 'results' in exportable:
            tickets_list = list(exportable['results'])

            for ticket in tickets_list:

                via_source = ticket['via']['source']
                source_from = dict(via_source['from'])
                created_date_only = ticket['created_at'].split('T')
                ticket_fields = ticket['fields']

                row = {
                    'CREATED_AT': created_date_only[0],
                    'ID': ticket['id'],
                    'SOURCE_NAME': source_from.get('name'),
                    'CLIENT_NAME': ticket_fields[2].get('value'),
                    'CONNECTOR': ticket_fields[3].get('value'),
                    'SUBJECT': ticket['subject'],
                    'DESCRIPTION': ticket['description'],
                    'LEVEL': ticket_fields[0].get('value'),
                    'STATUS': ticket['status']
                }

                df.loc[len(df)] = row

            if not exportable['next_page']:
                logging.info('ALL PAGES COMPLETED')
                print(df)

                df.to_csv(
                    'downloads\export.csv',
                    mode='a',
                    index=False,
                    encoding='utf-8',
                    header=True
                )

            else:
                print(f'Previous page: {exportable["previous_page"]}')
                print(f'Next page: {exportable["next_page"]}')

                generate_data(
                    new_next_page=exportable["next_page"]
                )

        else:
            print(df)
            print(exportable)

    except KeyboardInterrupt:
        logging.info('Program manually terminated')

    except Exception as e:
        logging.exception(e)
        exit()


if __name__ == '__main__':
    main()

# Zenex

A smol python wrapper class for the Zendesk API.

## How to use:

1. Initialize your instance:
   ```
    zd = Zenex(
        domain='your_domain.com',
        subdomain='your_subdomain',
        zd_user_email='your_api_user_email',
        zd_token='your_api_token'
    )
   ```
2. Use the methods:
   ```
   zd.get_id_context(context_id='organizations', resource='123456789')
   ```


# Example for accessing Github APIs with OAuth 2.0

## Prerequisites

Before running these examples, you will need the following:

* A Github  Account, you can sign up for one at https://github.com/.
* A Github Developer App with an OAuth 2.0 Client ID, configured for a Web application. This is done from the Github settings Console and you can find instructions [here]([https://developers.google.com/identity/protocols/oauth2](https://docs.github.com/en/developers/apps/building-oauth-apps/creating-an-oauth-app)). 



Now you need to gather the following information from the Github settings Console that belongs to your front-end application:
- **Client ID and Client Secret**  - The client ID and secret of the Web application that you created earlier. This identifies the application that tokens will be minted for.

Copy the [`client_config.py.dist`](client_config.py.dist) to `client_config.py` and fill in the information you gathered as well as edit the other fields to suit your deployment scenario

```python

github_client_id = 'xxxx'
github_client_secret ='xxxx'

authorize_url = 'https://github.com/login/oauth/authorize'

token_url = 'https://github.com/login/oauth/access_token'

api_url_base = 'https://api.github.com/'

base_url = 'http://localhost:5000/'

```

run the sample by typing:

``` bash
python3 github_client.py
```
Access the application by going to : http://localhost:5000/

#Example for accessing Google APIs with OAuth 2.0

## Prerequisites

Before running these examples, you will need the following:

* A Google Developer Account, you can sign up for one at https://developer.google.com/.
* A Google Developer project with an OAuth 2.0 Client ID, configured for a Web application. This is done from the Google Developer Console and you can find instructions [here](https://developers.google.com/identity/protocols/oauth2). 



Now you need to gather the following information from the Google Developer Console that belongs to your front-end application:
- **Client ID and Client Secret**  - The client ID and secret of the Web application that you created earlier. This can be found on the  right hand side of the screen when you are in the " Client ID for Web application " view . This identifies the application that tokens will be minted for.
- **Client Secret** - This is the URL of the authorization server that will perform authentication.  All Developer Accounts have a "default" authorization server.  The issuer is a combination of your Org URL (found in the upper right of the console home page) and `/oauth2/default`. For example, `https://dev-1234.oktapreview.com/oauth2/default`.

Copy the [`client_config.py.dist`](client_config.py.dist) to `client_config.py` and fill in the information you gathered as well as edit the other fields to suit your deployment scenario

```python
google_client_id = 'xxx-xxx.apps.googleusercontent.com'
google_client_secret ='xxx'

authorize_url = 'https://accounts.google.com/o/oauth2/v2/auth'

token_url = 'https://www.googleapis.com/oauth2/v4/token'


base_url = 'http://localhost:5000/'

user_info_url = 'https://www.googleapis.com/oauth2/v3/userinfo' 
```

run the sample by typing:

``` bash
python3 google_client.py
```
Access the application by going to : http://localhost:5000/

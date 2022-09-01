vulcan2calendar
===============
script used to port exams from vulcan gradebook to a google calendar.
# Requirements
used packages:
```python
vulcan api library:
    vulcan-api
    (https://github.com/kapi2289/vulcan-api)

google api libraries:
    google-api-python-client
    google-auth-httplib2 
    google-auth-oauthlib
```
# Set up
### Vulcan
[vulcan-api setup guide](https://vulcan-api.readthedocs.io/en/latest/getting-started.html)  
### tl;dr
### create keystore
```python
from vulcan import Keystore

keystore = Keystore.create()

keystore = Keystore.create(device_model="Vulcan API")
with open("keystore.json", "w") as f:
    f.write(keystore.as_json)
```

### register account/device
```python
from vulcan import Account

# keystore read from cachefile, token symbol and pin avaliable on vulcan portal
account = Account.register(keystore, token, symbol, pin)
with open("account.json", "w") as f:
    f.write(account.as_json)
```

### Google
[google's guide](https://developers.google.com/calendar/api/quickstart/python)
### tl;dr
### install packages
```bash
  pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

  #or

  pip3 install -r requirements.txt
```
### set up credentials and service account
[google guide](https://developers.google.com/workspace/guides/create-credentials)  
save credentials json file as ``credentials.json``


# How to run?
docker:
```bash
docker build -t vulcan2calendar --build-arg pin={vulcan pin} --build-arg token={vulcan token} --build-arg symbol={vulcan symbol}  . 

docker run -d -v  /etc/vulcan2calendar/credentials.json:/app/ vulcan2calendar
```
 or if you have already registered device on vulcan page, and you don't want to do it again
```bash
docker build -t vulcan2calendar . 
docker run -d -v  /etc/vulcan2calendar/credentials.json:/app/ -v  /etc/vulcan2calendar/account.json:/app/ -v  /etc/vulcan2calendar/keystore.json:/app/ vulcan2calendar
```
/ in /etc/vulcan2calendar/ I downloaded json files /

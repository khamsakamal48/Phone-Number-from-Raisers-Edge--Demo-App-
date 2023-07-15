# Phone Number from Raisers Edge (Demo App)
This is a fun demo app developed to demonstrate/test pulling phone numbers from Raisers Edge to a python web app using Blackbaud's SKY API.

## 1. Install pre-requisites
- Get a Ubuntu (Linux) machine
- Install below packages
```shell
sudo apt install python3-pip #Install Python (if not installed already)
```

```shell
pip install requests
pip install streamlit
pip install python-dotenv
pip install pandas
pip install pyarrow
pip install fastparquet
pip install chardet
```

## 2. Create a .env file with below parameters
- Create a .env file
```shell
vim .env
```

- Replace ```# ...``` with appropriate values
```shell
AUTH_CODE= # Raiser's Edge NXT Auth Code (encode Client)
REDIRECT_URL= # Redirect URL of application in Raiser's Edge NXT
CLIENT_ID= # Client ID of application in Raiser's Edge NXT
RE_API_KEY= # Raiser's Edge NXT Developer API Key
MAIL_USERN= # Email Username
MAIL_PASSWORD= # Email password
IMAP_URL= # IMAP web address
IMAP_PORT= # IMAP Port
SMTP_URL= # SMTP web address
SMTP_PORT= # SMTP Port
SEND_TO= # Email ID of user who needs to receive error emails (if any)
```

## 3. Installation steps
- Clone the repo
- Save the data from Raisers Edge to the Database folder with .parquet extension and filename as 'RE Data.parquet'
- Request Raisers Edge Access Token by running below command and following the on-screen instructions.
```shell
python3 'Request Access Token.py'
```
- Now, get a Refresh Token
```shell
python3 'Get Refresh Token.py'
```
- Set below cron jobs
```shell
@hourly cd Phone-Number-from-Raisers-Edge--Demo-App- && python3 'Get Refresh Token.py'> /dev/null 2>&1
```
- To run the web app
```shell
streamlit run App.py
```
- The app will be then accessible over `http://IP-Address-of-your-machine:8503/phone/`

## Note:
- This app is a mockup designed to retrieve phone numbers from Raisers Edge NXT based on Name, Degree, Department, and Batch.
- It also tests the latency/speed of Blackbaud’s API response within the IITB Campus.
- Phone numbers are retrieved using a GET request without maintaining a local cache/database.
- The only local database used is in .parquet format with Name, Batch, and Employment details.
- This app doesn't include:
  - Restricted Login access (username & password)
  - Restriction to copy the API response i.e. Phone numbers
  - Timeout to hide phone numbers
  - Logging of API requests
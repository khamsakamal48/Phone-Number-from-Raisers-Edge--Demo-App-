import streamlit as st
import pandas as pd
import json
import os
import requests
import time

from dotenv import load_dotenv
from urllib3 import Retry
from requests.adapters import HTTPAdapter

st.set_page_config(
    page_title='Get Phone Number',
    page_icon=':calling:',
    layout="wide")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Add a title and intro text
st.title('📲 Phone Number Retriever')
st.write('##')

# Define Functions
# Load the Parquet file into a Pandas dataframe
@st.cache_data() # Reset cache every 1 Hour
def get_data():
    data = pd.read_parquet('Database/RE Data.parquet')
    return data

data = get_data()

def get_env_variables():
    global RE_API_KEY, MAIL_USERN, MAIL_PASSWORD, IMAP_URL, IMAP_PORT, SMTP_URL, SMTP_PORT, SEND_TO, FORM_URL

    load_dotenv()

    RE_API_KEY = os.getenv('RE_API_KEY')
    MAIL_USERN = os.getenv('MAIL_USERN')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    IMAP_URL = os.getenv('IMAP_URL')
    IMAP_PORT = os.getenv('IMAP_PORT')
    SMTP_URL = os.getenv('SMTP_URL')
    SMTP_PORT = os.getenv('SMTP_PORT')
    SEND_TO = os.getenv('SEND_TO')
    FORM_URL = os.getenv('FORM_URL')

def retrieve_token():
    with open('access_token_output.json') as access_token_output:
        data = json.load(access_token_output)
        access_token = data['access_token']
        return access_token

def set_api_request_strategy():
    global http

    retry_strategy = Retry(
        total=3,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=['HEAD', 'GET', 'OPTIONS'],
        backoff_factor=10
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount('https://', adapter)
    http.mount('http://', adapter)

def get_request_re(url, params):
    # Retrieve access_token from file
    access_token = retrieve_token()

    # Request headers
    headers = {
        'Bb-Api-Subscription-Key': RE_API_KEY,
        'Authorization': 'Bearer ' + access_token,
    }

    re_api_response = http.get(url, params=params, headers=headers).json()
    return re_api_response


def api_to_df(response):
    # Load from JSON to pandas
    try:
        api_response = pd.json_normalize(response['value'])
    except:
        try:
            api_response = pd.json_normalize(response)
        except:
            api_response = pd.json_normalize(response, 'value')

    # Load to a dataframe
    df = pd.DataFrame(data=api_response)

    return df

# Load Environment variables
get_env_variables()

# Set API Request Strategy
set_api_request_strategy()

# Filters
# Year
st.write('#### Select the range for Graduation Year')
year_filter = st.select_slider(
    'Select the range for Graduation Year:',
    options=data['Class of'].drop_duplicates().sort_values(),
    value=(1990, 2010),
    label_visibility='hidden'
)

col1, col2 = st.columns(2)

with col1:
    st.write('#### Select the Department')
    dept_filter = st.multiselect(
        'Select the Department',
        options=data[data['Class of'].isin(year_filter)]['Department'].drop_duplicates().sort_values(),
        label_visibility='hidden'
    )

with col2:
    st.write('#### Select the Degree')
    degree_filter = st.multiselect(
        'Select the Degree',
        options=data[data['Class of'].isin(year_filter)]['Degree'].drop_duplicates().sort_values(),
        label_visibility='hidden'
    )

st.divider()

col3, col4 = st.columns(2)

with col3:
    st.write('#### Choose the Alum Name')
    name = st.selectbox(
        label='Choose the Alum Name',
        options=data[
            (data['Class of'].isin(year_filter)) &
            (data['Department'].isin(dept_filter)) &
            (data['Degree'].isin(degree_filter))
        ]['Name'].sort_values(),
        label_visibility='hidden'
    )
    if name:
        get_phone = st.button(
            label='Get Phone numbers'
        )

with col4:
    st.write('#### Phone Details:')
    if name:
        if get_phone:
            re_id = data[
                (data['Name'] == name) &
                (data['Class of'].isin(year_filter)) &
                (data['Department'].isin(dept_filter)) &
                (data['Degree'].isin(degree_filter))
                ]['CnBio_System_ID'].values[0]

            if re_id:
                url = f'https://api.sky.blackbaud.com/constituent/v1/constituents/{re_id}/phones'
                params = {}
                api_response = get_request_re(url, params)
                data = api_to_df(api_response).copy()
                data = data.sort_values('primary', ascending=False).copy()
                data = data[['number']].rename(columns={'number': 'Phone'}).drop_duplicates().copy()
                dataframe = st.dataframe(data, hide_index=True, use_container_width=True)

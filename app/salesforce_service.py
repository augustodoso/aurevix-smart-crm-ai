import os
import requests


SF_LOGIN_URL = os.getenv("SF_LOGIN_URL", "https://login.salesforce.com")
SF_CLIENT_ID = os.getenv("SF_CLIENT_ID")
SF_CLIENT_SECRET = os.getenv("SF_CLIENT_SECRET")
SF_USERNAME = os.getenv("SF_USERNAME")
SF_PASSWORD = os.getenv("SF_PASSWORD")
SF_SECURITY_TOKEN = os.getenv("SF_SECURITY_TOKEN")
SF_API_VERSION = os.getenv("SF_API_VERSION", "v60.0")


class SalesforceAuthError(Exception):
    pass


class SalesforceRequestError(Exception):
    pass


def get_access_token() -> dict:
    url = f"{SF_LOGIN_URL}/services/oauth2/token"

    payload = {
        "grant_type": "password",
        "client_id": SF_CLIENT_ID,
        "client_secret": SF_CLIENT_SECRET,
        "username": SF_USERNAME,
        "password": f"{SF_PASSWORD}{SF_SECURITY_TOKEN}",
    }

    response = requests.post(url, data=payload, timeout=30)

    if response.status_code != 200:
        raise SalesforceAuthError(
            f"Falha na autenticação Salesforce: {response.status_code} - {response.text}"
        )

    return response.json()


def create_lead(
    description: str,
    name: str,
    email: str,
    company: str
) -> dict:
    auth_data = get_access_token()
    access_token = auth_data["access_token"]
    instance_url = auth_data["instance_url"]

    url = f"{instance_url}/services/data/{SF_API_VERSION}/sobjects/Lead/"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    last_name = name.strip() if name.strip() else "Lead IA"

    payload = {
        "LastName": last_name,
        "Company": company.strip() if company.strip() else "Não informado",
        "Email": email.strip(),
        "Description": description,
        "Status": "Open - Not Contacted"
    }

    response = requests.post(url, json=payload, headers=headers, timeout=30)

    if response.status_code not in (200, 201):
        raise SalesforceRequestError(
            f"Falha ao criar Lead: {response.status_code} - {response.text}"
        )

    return response.json()
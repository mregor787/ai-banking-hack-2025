import requests

DB_URL = "http://db_service:8001"

def save_mail(customer_id: str, mail_text: str):
    url = f"{DB_URL}/api/customers/{customer_id}/mail"
    response = requests.post(url, json={"mailText": mail_text})
    response.raise_for_status()
    return response.json()

def save_answer(mail_id: str, answer_text: str, is_important=False, is_urgently=False):
    url = f"{DB_URL}/api/mails/{mail_id}/answer"
    response = requests.post(
        url,
        json={
            "answerText": answer_text,
            "isImportant": is_important,
            "isUrgently": is_urgently
        }
    )
    response.raise_for_status()
    return response.json()

def get_all_mails():
    resp = requests.get(f"{DB_URL}/api/mails")
    resp.raise_for_status()
    return resp.json()

def get_mail(mail_id):
    resp = requests.get(f"{DB_URL}/api/mails/{mail_id}")
    resp.raise_for_status()
    return resp.json()

def get_customers():
    url = f"{DB_URL}/api/customers"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

def create_customer(name: str, person_type: str):
    url = f"{DB_URL}/api/customers"
    payload = {"name": name, "personType": person_type}
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()

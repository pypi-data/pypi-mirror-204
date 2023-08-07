import requests
import openpyxl as px


def get_translation(text, auth_key, target_lang="JA"):
    url = "https://api-free.deepl.com/v2/translate"
    header = {
        "Host": "api-free.deepl.com",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "auth_key": auth_key,
        "text": text,
        "target_lang": target_lang,
    }
    response = requests.post(url=url, data=data, headers=header)
    json_data = response.json()
    return json_data["translations"][0]["text"]


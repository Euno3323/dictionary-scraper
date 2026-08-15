from re import sub
from bs4 import SoupStrainer, BeautifulSoup
import requests as req

user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136."
               ]

def fetch_html(url, **kwargs):
    """Sends a GET request to the given url"""
    try:
        response = req.get(url, **kwargs)
        print(f"Status-code: {response.status_code}")
        response.raise_for_status()
    except req.exceptions.Timeout as e:
        print(f"Request failed with the error: {e}")
        return None
    except req.exceptions.ConnectTimeout as e:
        print(f"Request failed with the error: {e}")
        return None
    except req.exceptions.RequestException as e:
        print(f"Request failed with the error: {e}")
        return None
    except req.exceptions.ConnectionError as e:
        print(f"Request failed with the error: {e}")
        return None
    
    print("Success!")
    return response.text

def extract_defintion(html_content):
    """Extracts defintion from the given html-content"""
    strainer = SoupStrainer("div")
    soup = BeautifulSoup(html_content, "lxml", parse_only=strainer)

    data = soup.find("div", class_="def ddef_d db")
    return data.get_text()

    print(data[:200])
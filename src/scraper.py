import re
import requests as req
import bs4 as bs


# # Reading each line and extracting the word
# with open(r"./data/input/words2.csv") as input_obj, open(r"./data/output/output.csv", "x") as output_obj:
#     for line in input_obj.readlines():
#         print(repr(line))
#         print(re.sub(" .+", "", repr(line)))


user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136."
               ]

def get_html(url, **kwargs):
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


data = get_html("https://dictionary.cambridge.org")
def extract_defintion(html_content):
    strainer = bs.SoupStrainer("div")
    soup = bs.BeautifulSoup(html_content, "lxml", parse_only=strainer)

    data = soup.find("div", class_="def ddef_d db")
    return data.get_text()

if (data):
    print(data[:200])
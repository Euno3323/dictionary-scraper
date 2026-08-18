from re import sub
from bs4 import SoupStrainer, BeautifulSoup
import requests as req
import time 

user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136."
               ]

def create_url(word):
    return f"https://dictionary.cambridge.org/dictionary/english/{word}"

def fetch_html(url, **kwargs):
    """Sends a GET request to the given url"""
    try:
        response = req.get(url, **kwargs)
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

    print(f"Successfully extracted content from: {url}")
    return response.text

def extract_defintion(html_content):
    """Extracts defintion from the given html-content"""
    strainer = SoupStrainer("div")
    soup = BeautifulSoup(html_content, "lxml", parse_only=strainer)

    data = soup.find("div", class_="def ddef_d db")
    definition = data.get_text()
    definition = definition.replace(":", "").strip()
    return definition

def read_input(filepath, start=None, end=None):
    """Generates a dictionary of the words from the given file"""
    with open(filepath) as file:
        for row_index, line in enumerate(file):
            if start is not None and row_index < start:
                continue
            if end is not None and end <= row_index:
                break

            line = line.strip().lower()
            yield {
                "original-word" : sub(",.*", "", line),
                "formatted-word" : sub(" .*", "", line)
            }

def write_output(path, word, definition):
    """Writes the given word and defintion to a file"""
    with open(path, "a") as file:
        file.write(word + "," + definition + "\n")

def main():
    word_gen = read_input("data/input/words.csv", 0, 5)
    output_name = time.strftime("%Y%m%d_%H%M%S")

    for dic in word_gen:
        url = create_url(dic.get("formatted-word"))
        definition = extract_defintion(fetch_html(url, headers={"User-Agent":user_agents[0]}))
        write_output(f"data/output/{output_name}.csv", dic.get("original-word"), definition)

if __name__ == "__main__":
    main()



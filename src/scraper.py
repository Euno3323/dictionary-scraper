import re
import requests as req
import bs4 as bs
import json


# # Reading each line and extracting the word
# with open(r"./data/input/words2.csv") as input_obj, open(r"./data/output/output.csv", "x") as output_obj:
#     for line in input_obj.readlines():
#         print(repr(line))
#         print(re.sub(" .+", "", repr(line)))


def get_html(url : str, timeout : int=2) -> str | None:
    try:
        url = "https://www.youtube.com/"
        response = req.get(url, timeout=timeout)
        print(f"Status-code: {response.status_code}")
        response.raise_for_status()

    except req.exceptions.Timeout as e:
        print(f"Request failed: {e}")
        return None

    except req.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

    else:
        print("Success!")
        return response.text

data = get_html("https://dictionary.cambridge.org/dictionary/english/house")

if (data):
    print(data[:200])
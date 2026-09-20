import requests as req
from agents import user_agents
from random import choice
from re import sub
from bs4 import SoupStrainer, BeautifulSoup
from time import strftime
from pathlib import Path

USAGE = "Usage: [OPTIONS] <FILEPATH> [START-ROW] [END-ROW]\n" \
        "\n" \
        "Arguments:\n" \
        "\tFILEPATH:\tPath to input file.\n" \
        "\tSTART-ROW:\tFirst row to read in file.\n" \
        "\tEND-ROW:\tLast row to read in file,\n" \
        "\n" \
        "Options:\n" \
        "\t-h, -help, --help\t Show help message"


def fetch_html(url, **kwargs):
    """Sends a GET request to the given url."""
    try:
        response = req.get(url, **kwargs)
        response.raise_for_status()
        return response.text
    except req.exceptions.Timeout as e:
        print(f"Request failed for {url}: {e}")
        return None
    except req.exceptions.RequestException as e:
        print(f"Request failed for {url}: {e}")
        return None

def extract_defintion(html_content):
    """Extracts defintion from the given html-content"""
    strainer = SoupStrainer("div")
    soup = BeautifulSoup(html_content, "lxml", parse_only=strainer)

    data = soup.find("div", class_="def ddef_d db")
    definition = data.get_text()
    definition = definition.replace(":", "").strip()
    return definition


def create_url(word):
    return f"https://dictionary.cambridge.org/dictionary/english/{word}"

def read_lines(filepath, start_row=None, end_row=None):
    """Read words from a file and return a list of tuples (original word, formatted word, row-index)."""

    words = []

    with open(filepath, encoding="utf-8") as file:
        for row_index, line in enumerate(file):
            if start_row is not None and row_index < start_row:
                continue
            if end_row is not None and row_index >= end_row:
                break

            line = line.strip().lower()

            if line:
                words.append((line, sub("[ (].*", "", line), row_index))

    return words

def main():
    word_gen = read_input("data/input/words.csv", 0, 5)
def write_output(filepath, word, definition):
    """Writes the given word and definition to a file."""
    with open(filepath, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([word, definition])

def parse_arguments(args):
    """Parses arguments and validates them."""

    operands = {}

    if not args or len(args) > 3:
        raise SystemExit("Incorrect number of arguments.")
    
    if args[0] in ("-h", "-help", "--help"):
        raise SystemExit(USAGE)

    if not Path(args[0]).is_file():
        raise SystemExit("Path is invalid, inaccessible, missing, or does not point to a file.")

    if not args[0].lower().endswith(".csv"):
        raise SystemExit("File is not of the type .csv.")

    operands["filepath"] = args[0]

    try:
        start_row = int(args[1]) if len(args) > 1 else None
        end_row = int(args[2]) if len(args) > 2 else None
    except ValueError:
        raise SystemExit("Optional arguments are not of type integer.")

    if start_row is not None and start_row < 0:
        raise SystemExit("Integers must be positive.")

    if end_row is not None and end_row < 0:
        raise SystemExit("Integers must be positive.")

    if start_row is not None and end_row is not None and start_row > end_row:
        raise SystemExit("START-ROW must be smaller or equal to END-ROW.")

    operands["start_row"] = start_row
    operands["end_row"] = end_row

    return operands
    
    output_name = strftime("%Y%m%d_%H%M%S")

    for dic in word_gen:
        url = create_url(dic.get("formatted-word"))
        html = fetch_html(url, headers={"User-Agent" : choice(user_agents)})
        definition = extract_defintion(html)
        write_output(f"data/output/{output_name}.csv", dic.get("original-word"), definition)

if __name__ == "__main__":
    main()



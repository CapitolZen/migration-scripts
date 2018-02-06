import click
from html.parser import HTMLParser
import json


class MyHTMLParser(HTMLParser):

    results = None

    is_client_title = False
    current_client = ""

    def __init__(self):
        super().__init__()
        self.results = {}

    def handle_starttag(self, tag, attrs):
        if tag == "h3":
            self.is_client_title = True
        else:
            print(tag)

    def handle_endtag(self, tag):
        if tag == "h3":
            self.is_client_title = False
        else:
            print(tag)

    def handle_data(self, data):
        if self.is_client_title and data not in self.results:
            self.results[data] = []
            self.current_client = data
        else:
            data = data.strip()
            if "SB" in data or "HB" in data or "SR" in data:
                self.results[self.current_client].append(data)

    def get_data(self):
        return self.results


@click.command()
@click.argument('file', type=click.File(mode='r', encoding='utf-16'))
def parse(file):
    content = file.read()
    parser = MyHTMLParser()
    parser.feed(content)
    print(json.dumps(parser.get_data()))


if __name__ == '__main__':
    parse()
from bs4 import BeautifulSoup
from requests import get

from argparse import ArgumentParser
from pathlib import Path
from json import dumps


arg_parser = ArgumentParser(description='Utility program to immediately generate a list from the docs')

arg_parser.add_argument('url', help='URL of the documentation')
arg_parser.add_argument('-o', '--output', type=Path, help='Output file name')

args = arg_parser.parse_args()


req = get(args.url)
soup = BeautifulSoup(req.text, 'html.parser')

out = []
for link in soup.find_all('tr'):
    if link.get('class') is None:
        continue
    
    if link.get('class')[0].startswith('memitem:'):
        if link.find_all('td')[1].find('b') is None:
            continue
        
        out.append(link.find_all('td')[1].find('b').string)


if args.output is not None:
    args.output.write_text(dumps(out, indent=4))

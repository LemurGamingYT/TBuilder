from bs4 import BeautifulSoup
from requests import get

from argparse import ArgumentParser
from pathlib import Path
from json import dumps


arg_parser = ArgumentParser(description='Utility program to immediately generate a list from the docs')

arg_parser.add_argument('url', help='URL of the documentation')
arg_parser.add_argument('-o', '--output', type=Path, help='Output file name')

arg_parser.add_argument('-n', '--name', help='Set the name of the Enum (if -e is used)')

arg_parser.add_argument('-e', '--enum', help='Generates an enum instead of list', action='store_true')

args = arg_parser.parse_args()


name = args.name if args.name is not None else 'TDocEnum'


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
    if args.enum:
        text = 'from enum import Enum, auto\n\nclass {}(Enum):\n\t'.format(name)
        for element in out:
            text += element.upper() + ' = auto()\n\t'
        
        args.output.write_text(text)
    else:
        args.output.write_text(dumps(out, indent=4))

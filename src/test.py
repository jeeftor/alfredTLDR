import sys
import glob, os
from collections import Counter


def filter_commands(filter, exact_match_only=True):

    os.chdir("../tldr-pages/pages/common")

    # The order matters here
    directories = ['sunos', 'linux','common','osx',]


    starts_with = {}
    filter_match = {}
    match = {}

    for d in directories:

        os.chdir("../" + d)
        for f in glob.glob("*.md"):
            cmd = f[:-3]
            loc = d + "/" + f

            if filter == cmd and exact_match_only:
                match[cmd] = loc
            elif cmd.startswith(filter):
                starts_with[cmd] = loc
            elif filter in cmd:
                filter_match[cmd] = loc


    if bool(match):
        print match
    else:
        print starts_with, match




def parse_tldr_page(location):

    overall_description = ""


    with open(location) as f:
        for line in f:

            if line.startswith('>'):
                overall_description += line[1:]
                pass
            elif line.startswith('-'):
                subtitle = line[1:-2]
                title = None
                pass
            elif line.startswith('`'):
                title = line[1:-2]
                print title,"\n",subtitle
                subtitle = None
                title = None
                pass

            #print line.strip()


filter_commands('w', exact_match_only=False)
parse_tldr_page('../osx/wacaw.md')
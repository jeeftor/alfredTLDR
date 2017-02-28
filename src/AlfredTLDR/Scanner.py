import os
import glob

class Scanner():
    """TLDR Directory scanner class - handles the TLDR pages"""

    def __init__(self, wf, directory=None):
        if directory:
            self.base_directory = directory
        else:
            self.base_directory = os.getcwd() + "/tldr-pages/pages"

        self.wf = wf

    def filter_commands(self, filter, exact_match_only=True):
        """Scans the base_directory list for stuff"""
        self.wf.logger.debug('Searching for string [{}]'.format(filter))
        os.chdir(self.base_directory + "/common")

        # The order matters here - if there are dupes only the "last" one will be found
        directories = ['sunos', 'linux', 'common', 'osx', ]

        starts_with = {}
        generic_match = {}
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
                    generic_match[cmd] = loc

        self.wf.logger.debug('Found {} Exact Matches'.format(len(match)))
        self.wf.logger.debug('Found {} Starts With Matches'.format(len(starts_with)))
        self.wf.logger.debug('Found {} generic matches'.format(len(generic_match)))
        if bool(match):
            #print match
            self.parse_tldr_page(match.values()[0])
        else:

            sorted_starts_with = sorted(starts_with.keys(), key=lambda x: x.lower())
            sorted_generic_match = sorted(generic_match.keys(), key=lambda x: x.lower())

            self.wf.add_item('Searching for: ' + filter, 'Found ' + str(len(sorted_generic_match) + len(sorted_starts_with)) + ' entries')

            for item in sorted_starts_with:
                self.wf.add_item(item, starts_with[item])

            for item in sorted_generic_match:
                self.wf.add_item(item, generic_match[item])


    def parse_tldr_page(self, tldr_file):
        """Opens a TLDR.md file and formats it for alfred magic"""
        overall_description = ""

        file_path = self.base_directory + '/' + tldr_file

        with open(file_path) as f:
            for line in f:

                if line.startswith('>'):
                    overall_description += line[1:]
                elif line.startswith('-'):
                    subtitle = line[1:-2]
                    title = None
                    pass
                elif line.startswith('`'):
                    title = line[1:-2]
                    self.wf.add_item(subtitle,title, valid=False, quicklookurl=file_path)
                    subtitle = None
                    title = None
                    pass


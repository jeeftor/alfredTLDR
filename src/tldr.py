from workflow import Workflow3
import sys
from AlfredTLDR import Scanner


def main(wf):
    query = str(wf.args[0]).lower()

    scanner = Scanner.Scanner(wf)
    scanner.filter_commands(query,exact_match_only=True)
    #scanner.parse_tldr_page('osx/xed.md')
    wf.send_feedback()
pass



if __name__ == u"__main__":
    wf = Workflow3()
    sys.exit(wf.run(main))


"""
Git Notion

Usage:
  git_notion.py [options]

Options:
    -h --help                       Show this screen.
    -s --page-structure=<value>     The structure of the pages in Notion. (nested|flat) [default: nested]
    -d --dir-name=<value>           The name of the directory to save the documents to.
    -f --use-file-name              Use the file name as the page title, instead of the first h1 in the file.
"""

import sys
from docopt import docopt
import git_notion_pretty as git_notion

def main():
    """Console script for git_notion"""
    args = docopt(__doc__)

    # convert all the arguments to the correct type
    if args["--dir-name"] == "None":
        args["--dir-name"] = None

    git_notion.sync_to_notion(args["--dir-name"], args["--use-file-name"], page_structure=args["--page-structure"])
    return 0

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

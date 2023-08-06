"""Main module."""
import hashlib
import os
import glob
from configparser import ConfigParser
import re

from notion.block import PageBlock
from notion.block import TextBlock
from notion.block import CalloutBlock
from notion.client import NotionClient
from md2notion.upload import upload


TOKEN = os.getenv("NOTION_TOKEN_V2", "")
_client = None


def get_client():
    global _client
    if not _client:
        _client = NotionClient(token_v2=TOKEN)
    return _client


def get_or_create_page(base_page, title):
    page = None
    for child in base_page.children.filter(PageBlock):
        if child.title == title:
            page = child

    if not page:
        page = base_page.children.add_new(PageBlock, title=title)
        page.children.add_new(CalloutBlock, title=f"This page was automatically generated.", icon="🤖")
    return page


def upload_file(base_page, filename: str, use_file_name=False, page_structure="nested"):
    """Upload a file to Notion."""
    # Get the page title
    page_title = os.path.basename(filename)
    if use_file_name is False:
        # find the first h1 in the file and use that as the page title
        with open(filename, "r", encoding="utf-8") as mdFile:
            # only read the first line
            for line in mdFile.readlines(1):
                if line.startswith("# "):
                    page_title = line[2:].strip()
                    print(f"Found title {page_title}")
                    strip_first_line = True # strip the first line when uploading to make it pretty
                    break
        if page_title is None:
            page_title = os.path.basename(filename)
            print(f"Could not find a title for {filename}. Using the file name instead.")

    if page_structure == "flat":
        print(f"Uploading {page_title} to {base_page.title}")
        page = get_or_create_page(base_page, page_title)
    elif page_structure == "nested":
        # Create a page for each directory in the path
        path = os.path.dirname(filename)
        if path == "": # no path
            page = get_or_create_page(base_page, page_title)
        else: # path exists
            page = base_page
            print(f"Page is {page}")
            for dir in path.split(os.sep):
                print(f"Uploading {page_title} to {base_page.title}")
                page = get_or_create_page(page, dir)
            # Create a page for the file
            print(f"Uploading {page_title} to {base_page.title}")
            page = get_or_create_page(page, page_title)
    else:
        raise ValueError(f"Invalid page structure: {page_structure}")

    # Check if the file has changed since the last upload
    hasher = hashlib.md5()
    with open(filename, "rb") as mdFile:
        buf = mdFile.read()
        hasher.update(buf)
    if page.children and hasher.hexdigest() in str(page.children[0]):
        return page

    # Remove all the existing children and add the new hash
    for child in page.children:
        child.remove()
    page.children.add_new(TextBlock, title=f"MD5: {hasher.hexdigest()}")
    page.children.add_new(CalloutBlock, title=f"This page was automatically generated.", icon="🤖")

    # Upload the file
    with open(filename, "r", encoding="utf-8") as mdFile:
        upload(mdFile, page)
    return page


def sync_to_notion(dir_name, use_file_name=True, page_structure='nested'): # takes in the arguments from the docopt
    # Get the name of the current working directory, to be used as the container page name
    if dir_name is None:
        dir_name = os.path.basename(os.getcwd())

    # Get the configurations from the config file
    config = ConfigParser() # create a config parser object
    config_path = os.getenv("NOTION_CONFIG_PATH") or "./"
    config.read(os.path.join(config_path, "setup.cfg")) # read the config file

    # Pull the configurations from the config file or environment variables
    root_page_url = os.getenv("NOTION_ROOT_PAGE") or config.get('git-notion-pretty', 'notion_root_page')
    include_regex = os.getenv("NOTION_INCLUDE_REGEX") or config.get('git-notion-pretty', 'include_regex', fallback=None)
    ignore_regex = os.getenv("NOTION_EXCLUDE_REGEX") or config.get('git-notion-pretty', 'ignore_regex', fallback=None)

    # Get the root page. This is the parent page for all container pages.
    # Typically this should be something like "Knowledge Base" or "GitHub Docs"
    root_page = get_client().get_block(root_page_url)
    # Get or create the container page for the current working directory. This page will contain all the files
    # Typically this should be something like "backend" or "frontend" - the name of the repository
    container_page = get_or_create_page(root_page, dir_name)

    # Iterate through the files in the directory and upload them to Notion
    for file in glob.glob("**/*.md", recursive=True):
        if (
            (include_regex is None or re.match(include_regex, file)) # if the file matches the include regex
            and (ignore_regex is None or not re.match(ignore_regex, file)) # and the file does not match the ignore regex
        ):
            print(f"\n{file}")
            upload_file(
                container_page,
                file,
                use_file_name,
                page_structure,
            )
        else:
            continue # skip the file if it matches the ignore regex
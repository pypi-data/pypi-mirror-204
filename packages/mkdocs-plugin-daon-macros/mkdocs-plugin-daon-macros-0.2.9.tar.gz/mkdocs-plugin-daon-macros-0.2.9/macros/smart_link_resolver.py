import os
import logging
from functools import lru_cache

log = logging.getLogger('mkdocs')


def smart_link(self, config, page):
    # Wrap the config and page variables in a closure so that they can be
    # referenced by the function within the Jinja environment.

    def smart_link_wrapped(smart_id=None, alt_text=None):
        docs_dir = config.data['docs_dir']
        file_path = find_smart_id(docs_dir, smart_id)
        if file_path is None:
            log.warn(f"Smart link with ID: " + smart_id + " NOT found")
            return alt_text
        file_path = file_path.replace('/index/#', '/#')
        rel_url = os.path.relpath(file_path, config.data['docs_dir'] + "/" + page.url)
        tag = f'<a class="sl_ref" href="{rel_url}" > ' + alt_text + '</a>'
        return tag

    return smart_link_wrapped


@lru_cache(maxsize=1024)
def find_smart_id(docs_dir, smart_id):
    for root, dirs, files in os.walk(docs_dir, onerror=None):
        for filename in files:  # iterate over the files in the current dir
            file_path = os.path.join(root, filename)  # build the file path
            if filename.endswith(".md"):
                try:
                    with open(file_path, "rb") as f:  # open the file for reading
                        # read the file line by line
                        for line in f:  # use: for i, line in enumerate(f) if you need line numbers
                            try:
                                line = line.decode("utf-8")  # try to decode the contents to utf-8
                            except ValueError:  # decoding failed, skip the line
                                continue
                            if 'id="' + smart_id in line:  # if the keyword exists on the current line...
                                log.info(f"Smart link with ID: {smart_id} found on: {file_path}")
                                file_path = (os.path.splitext(file_path)[0])
                                return file_path + '/#' + smart_id  # no need to iterate over the rest of the file
                except (IOError, OSError):  # ignore read and permission errors
                    pass

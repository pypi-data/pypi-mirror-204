import glob
import os
import logging
import re
from functools import lru_cache


log = logging.getLogger('mkdocs')


def smart_image(self, config, page):
    # Wrap the config and page variables in a closure so that they can be
    # referenced by the function within the Jinja environment.

    def smart_image_wrapped(name=None, alt_text=None):
        log.info(f"Processing smart image name: {name} at: {page}")

        path = resolve_image(
            config.data['docs_dir'], os.path.dirname(page.file.abs_src_path), name)
        if path:
            # Need to take the path of the page into account
            # when calculating the relative URL for the image.
            rel_url = os.path.relpath(path, config.data['docs_dir'] + "/" + page.url)
            log.info(f"Found image: '{name}' at: '{rel_url}'")
            self.monitor[config.data['docs_dir'] + "/" + name] = True
            # identityx-logo.png -> identityx-logo-png for id attrib
            image_id = "si-id-" + re.sub(r"[_\./]", '-', page.url + name)
            css_class = "si-class-" + re.sub(r"[_\./]", '-', name)
            alt = image_id
            if alt_text is not None:
                alt = alt_text
            tag = f'<img alt="{alt}" id="{image_id}" class="{css_class}" src="{rel_url}" ></img>'
            log.info(f"Using tag: '{tag}'")

            return tag
        else:
            log.error(f"Could not find image: '{name}' referenced by: '{page.file.abs_src_path}'")

    return smart_image_wrapped


@lru_cache(maxsize=1024)
def resolve_image(base_dir, curr_dir, image):
    log.debug(f"Searching: {curr_dir} for: {image}")
    found = glob.glob(f"{curr_dir}/images/{image}")
    if found:
        log.debug(f"Resolved image at: {found}")
        return found[0]
    else:
        if curr_dir == base_dir:
            # We've hit the base directory.
            return None
        else:
            # Try the parent directory.
            curr_dir = os.path.dirname(curr_dir)
            return resolve_image(base_dir, curr_dir, image)



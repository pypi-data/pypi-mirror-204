# --------------------------------------------
# Main part of the plugin
# Defines the VariablesPlugin class
#
# Laurent Franceschetti (c) 2018
# MIT License
# --------------------------------------------

from mkdocs.plugins import BasePlugin
from jinja2 import Template
import os
import logging
from . import module_reader
from . import smart_image_resolver
from . import smart_link_resolver

log = logging.getLogger('mkdocs')

# The subset of the YAML file that will be used for the variables:
YAML_SUBSET = 'extra'

# the list of variables (including functions) to be injected
variables = {}


class MacrosPlugin(BasePlugin):
    """
    Inject config 'extra' variables into the markdown
    plus macros / variables defined in external module.

    The python code is located in 'main.py' or in a 'main' package
    in the root directory of the website
    (unless you want to redefine that name in the 'python_module' value
    in the mkdocs.yml file)
    """
    monitor = {}

    @property
    def variables(self):
        "The list of variables"
        try:
            return self._variables
        except AttributeError:
            return None

    def on_config(self, config):
        docs_dir = config.data['docs_dir']
        for root, dirs, files in os.walk(docs_dir):
            for file in files:
                if file.endswith((".png", '.jpg', 'jpeg', 'gif')):
                    self.monitor.update({str(root + '/' + file): False})
        "Fetch the variables and functions"
        # print("Here is the config:", config)
        # fetch variables from YAML file:
        self._variables = config.get(YAML_SUBSET)

        # add variables and functions from the module:
        module_reader.load_variables(self._variables, config)

        print("Variables:", self.variables)

    def on_page_markdown(self, markdown, page, config,
                         site_navigation=None, **kwargs):
        "Provide a hook for defining functions from an external module"

        # the site_navigation argument has been made optional
        # (deleted in post 1.0 mkdocs, but maintained here
        # for backward compatibility)

        # Create templae and get the variables
        md_template = Template(markdown)

        # Execute the jinja2 template and return
        return md_template.render({'smart_image': smart_image_resolver.smart_image(self, config, page),
                                   'smart_link': smart_link_resolver.smart_link(self, config, page)},
                                  **self.variables)

    def on_post_build(self, config):

        unused_images_identifier = True if 'unused_images_identifier' not in config.data else config.data[
            'unused_images_identifier']
        if unused_images_identifier:
            for k, v in self.monitor.items():
                if v:
                    # log.info('Image ' + k + ' is used in documentation pages')
                    print('Image ' + k + ' is used in documentation pages')
                else:
                    # log.warning('Image ' + k + ' is NOT used in documentation pages')
                    print('Image ' + k + ' is NOT used in documentation pages')

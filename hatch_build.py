"""Custom build script for hatch backend"""

import os
import sys
from urllib.request import urlopen

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

notebook_css_version = "5.4.0"
notebook_css_url = f"https://cdn.jupyter.org/notebook/{notebook_css_version}/style/style.min.css"


jupyterlab_css_version = "3.1.11"
jupyterlab_css_url = f"https://unpkg.com/@jupyterlab/nbconvert-css@{jupyterlab_css_version}/style/index.css"


jupyterlab_theme_light_version = "3.1.11"
jupyterlab_theme_light_url = f"https://unpkg.com/@jupyterlab/theme-light-extension@{jupyterlab_theme_light_version}/style/variables.css"


jupyterlab_theme_dark_version = "3.1.11"
jupyterlab_theme_dark_url = f"https://unpkg.com/@jupyterlab/theme-dark-extension@{jupyterlab_theme_dark_version}/style/variables.css"


template_css_urls = {
    "lab": [
        (jupyterlab_css_url, "index.css"),
        (jupyterlab_theme_light_url, "theme-light.css"),
        (jupyterlab_theme_dark_url, "theme-dark.css"),
    ],
    "classic": [(notebook_css_url, "style.css")],
}

osp = os.path
here = osp.abspath(osp.dirname(__file__))
templates_dir = osp.join(here, "share", "templates")


def _get_css_file(template_name, url, filename):
    """Get a css file and download it to the templates dir"""
    directory = osp.join(templates_dir, template_name, "static")
    dest = osp.join(directory, filename)
    if not osp.exists(directory):
        os.makedirs(directory)
    print(f"Downloading CSS: {url}")
    try:
        css = urlopen(url).read()
    except Exception as e:
        msg = f"Failed to download css from {url}: {e}"
        print(msg, file=sys.stderr)
        if osp.exists(dest):
            print(f"Already have CSS: {dest}, moving on.")
        else:
            raise OSError("Need CSS to proceed.")
        return

    with open(dest, "wb") as f:
        f.write(css)
    print(f"Downloaded Notebook CSS to {dest}")


def _get_css_files():
    """Get all of the css files if necessary"""
    if in_checkout := osp.exists(osp.abspath(osp.join(here, "..", ".git"))):
        print("Not running from git, nothing to do")
        return

    for template_name, resources in template_css_urls.items():
        for url, filename in resources:
            _get_css_file(template_name, url, filename)


class CustomHook(BuildHookInterface):
    def initialize(self, version, build_data):
        if self.target_name not in ["wheel", "sdist"]:
            return
        _get_css_files()

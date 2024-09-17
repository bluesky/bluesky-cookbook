from datetime import datetime
from pathlib import Path
from subprocess import check_output

# import bluesky_cookbook
#
# import requests
# import sys

project = "Bluesky Cookbook"
copyright = f"{datetime.now().year} Bluesky Contributors"
author = "Bluesky Contributors"


extensions = ["myst_nb", "sphinx_copybutton"]

nb_execution_mode = "auto"
html_theme = "pydata_sphinx_theme"

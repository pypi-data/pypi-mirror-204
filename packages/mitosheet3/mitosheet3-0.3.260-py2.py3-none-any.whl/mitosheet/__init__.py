#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Saga Inc.
# Distributed under the terms of the GPL License.
"""
The Mito package, which contains functions for creating a Mito sheet. 

To generate a new sheet, simply run:

import mitosheet
mitosheet.sheet()

If running mitosheet.sheet() just prints text that looks like `MitoWidget(...`, then you need to 
install the JupyterLab extension manager by running:

jupyter labextension install @jupyter-widgets/jupyterlab-manager@2;

Run this command in the terminal where you installed Mito. It should take 5-10 minutes to complete.

Then, restart your JupyterLab instance, and refresh your browser. Mito should now render.

NOTE: if you have any issues with installation, please email jake@sagacollab.com
"""

import os
import pandas as pd

# Public interface we want users to rely on
from mitosheet.mito_backend import sheet
from mitosheet._version import __version__

# NOTE: We always export v1 sheet functions and types as unqualified exports, as we did
# this when we started Mito. This allows us to not break existing user analyses. We should
# never add to these -- see mitosheet/public/README.md for more info
from mitosheet.public.v1 import register_analysis
from mitosheet.public.v1.sheet_functions import *
from mitosheet.public.v1.sheet_functions.types import *
from mitosheet.public.v1.utils import flatten_column_header

# We export depricated utilities, so that users can still use them if they used to
from mitosheet.api.get_column_summary_graph import (
    filter_df_to_safe_size_external as filter_df_to_safe_size,
)
from mitosheet.step_performers.bulk_old_rename.deprecated_utils import (
    make_valid_header_external as make_valid_header,
)

# Make sure the user is initalized
from mitosheet.user import initialize_user
initialize_user()

# This function is only necessary for mitosheet3, as it is used
# in jlab3 to find the extension. It is not used in jlab2
def _jupyter_labextension_paths():
    """Called by jupyterlab to load the extension"""
    return [{"src": "labextension", "dest": "mitosheet"}]


def _jupyter_nbextension_paths():
    """Called by Jupyter Notebook Server to detect if it is a valid nbextension and
    to install the widget

    Returns
    =======
    section: The section of the Jupyter Notebook Server to change.
        Must be 'notebook' for widget extensions
    src: Source directory name to copy files from. Webpack outputs generated files
        into this directory and Jupyter Notebook copies from this directory during
        widget installation
    dest: Destination directory name to install widget files to. Jupyter Notebook copies
        from `src` directory into <jupyter path>/nbextensions/<dest> directory
        during widget installation
    require: Path to importable AMD Javascript module inside the
        <jupyter path>/nbextensions/<dest> directory
    """
    return [{
        'section': 'notebook',
        'src': 'nbextension',
        'dest': 'mitosheet',
        'require': 'mitosheet/extension'
    }]
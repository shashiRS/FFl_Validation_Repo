#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Helpers for unit testing."""
import logging
import os
import shutil
import tempfile
from pathlib import Path

import pytest

__author__ = "ADAS-Test-Scripting-Foundation"
__copyright__ = "Copyright 2021, Continental AMS ADAS RD ADS V&V TES LND"
__version__ = "0.1"
__status__ = "Development"

_log = logging.getLogger(__name__)


@pytest.fixture()
def temp_dir() -> Path:
    temp_dir = tempfile.mkdtemp(prefix="tsf_")
    if os.path.exists(temp_dir):
        try:
            shutil.rmtree(temp_dir)
            os.makedirs(temp_dir)
        except Exception as ex:
            _log.info(f"Failed to delete tempdir: {ex}")

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
        _log.debug(f"Created temporary directory: '{temp_dir}'")

    yield Path(temp_dir)

    _log.debug("Deleting temporary directory...")
    try:
        shutil.rmtree(temp_dir)
    except Exception as ex:
        _log.info(f"Failed to delete temp dir... [{ex}]")
    pass

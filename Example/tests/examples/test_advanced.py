#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quickstart example."""
import logging
from pathlib import Path

from advanced.confusion_matrix import example as cm

__author__ = "BA ADAS ENP SIMU KPI"
__copyright__ = "2020-2012, Continental AG"
__version__ = "0.16.1"
__status__ = "Production"


_log = logging.getLogger(__name__)


pytest_plugins = ("examples.tests.test_support",)


def test_confusion_matrix_main(temp_dir: Path):
    """Unit test quickstart.

    .. note:: Can be safely ignored as reader of the examples.
    """
    cm.main(temp_dir, False)

    assert (temp_dir / "out" / "run_spec.json").exists()
    assert (temp_dir / "out" / "report" / "html" / "index.html").exists()

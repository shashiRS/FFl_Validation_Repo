#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quickstart example."""
import logging
from pathlib import Path

from examples.quickstart import main as qs

__author__ = "BA ADAS ENP SIMU KPI"
__copyright__ = "2020-2012, Continental AG"
__version__ = "0.16.1"
__status__ = "Production"


_log = logging.getLogger(__name__)


pytest_plugins = ("examples.tests.test_support",)


def test_quickstart_main(temp_dir: Path):
    """Unit test quickstart.

    .. note:: Can be safely ignored as reader of the examples.
    """
    qs.main(temp_dir, False)

    assert (temp_dir / "run_spec.json").exists()
    assert (temp_dir / "report" / "html" / "index.html").exists()

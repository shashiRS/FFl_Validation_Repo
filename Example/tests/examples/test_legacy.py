#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quickstart example."""
import logging
from pathlib import Path

from legacy.basic import (
    custom_readers,
    empty_expected_result_example,
    label_db,
    minimal_example,
    preprocessor_example,
    reading_with_wildcards_example,
    reference_reading_example,
    side_load_example,
    statistics_example,
)

__author__ = "BA ADAS ENP SIMU KPI"
__copyright__ = "2020-2012, Continental AG"
__version__ = "0.16.1"
__status__ = "Production"


_log = logging.getLogger(__name__)


pytest_plugins = ("examples.tests.test_support",)


def test_custom_readers(temp_dir: Path):
    """Unit test quickstart.

    .. note:: Can be safely ignored as reader of the examples.
    """
    custom_readers.main(temp_dir, False)

    assert (temp_dir / "run_spec.json").exists()
    assert (temp_dir / "report" / "html" / "index.html").exists()


def test_empty_expected_result_example(temp_dir: Path):
    """Unit test quickstart.

    .. note:: Can be safely ignored as reader of the examples.
    """
    empty_expected_result_example.main(temp_dir, False)

    assert (temp_dir / "run_spec.json").exists()
    assert (temp_dir / "report" / "html" / "index.html").exists()


def test_label_db(temp_dir: Path):
    """Unit test quickstart.

    .. note:: Can be safely ignored as reader of the examples.
    """
    label_db.main(temp_dir, False)

    assert (temp_dir / "run_spec.json").exists()
    assert (temp_dir / "report" / "html" / "index.html").exists()


def test_minimal_example(temp_dir: Path):
    """Unit test quickstart.

    .. note:: Can be safely ignored as reader of the examples.
    """
    minimal_example.main(temp_dir, False)

    assert (temp_dir / "run_spec.json").exists()
    assert (temp_dir / "report" / "html" / "index.html").exists()


def test_preprocessor_example(temp_dir: Path):
    """Unit test quickstart.

    .. note:: Can be safely ignored as reader of the examples.
    """
    preprocessor_example.main(temp_dir, False)

    assert (temp_dir / "run_spec.json").exists()
    assert (temp_dir / "report" / "html" / "index.html").exists()


def test_reading_with_wildcards_example(temp_dir: Path):
    """Unit test quickstart.

    .. note:: Can be safely ignored as reader of the examples.
    """
    reading_with_wildcards_example.main(temp_dir, False)

    assert (temp_dir / "run_spec.json").exists()
    assert (temp_dir / "report" / "html" / "index.html").exists()


def test_reference_reading_example(temp_dir: Path):
    """Unit test quickstart.

    .. note:: Can be safely ignored as reader of the examples.
    """
    reference_reading_example.main(temp_dir, False)

    assert (temp_dir / "run_spec.json").exists()
    assert (temp_dir / "report" / "html" / "index.html").exists()


def test_side_load_example(temp_dir: Path):
    """Unit test quickstart.

    .. note:: Can be safely ignored as reader of the examples.
    """
    side_load_example.main(temp_dir, False)

    assert (temp_dir / "run_spec.json").exists()
    assert (temp_dir / "report" / "html" / "index.html").exists()


def test_statistics_example(temp_dir: Path):
    """Unit test quickstart.

    .. note:: Can be safely ignored as reader of the examples.
    """
    statistics_example.main(temp_dir, False)

    assert (temp_dir / "run_spec.json").exists()
    assert (temp_dir / "report" / "html" / "index.html").exists()

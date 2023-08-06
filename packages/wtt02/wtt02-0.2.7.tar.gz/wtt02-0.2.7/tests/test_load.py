"""Test the extension can be loaded and used."""

import pathlib

import pytest

import wtt02.main as main

HERE = pathlib.Path(__file__).parent


def test_load(monkeypatch):
    """Test the extension can be loaded."""
    monkeypatch.setenv("WTT_02_LICENSE", "test")

    con = main.get_connection()

    results = con.execute("SELECT calc_exact_mw('c1ccccc1');").fetchall()
    assert len(results) == 1


def test_load_missing_env_var():
    """Test the extension can be loaded."""
    with pytest.raises(main.WTT02ConfigurationException):
        main.get_connection()

"""Basic tests for the kinwangji package."""

import pytest
from kinwangji import wanji_four_gua, jq, gangzhi, jiazi


def test_jiazi_length():
    """The sexagenary cycle should contain exactly 60 entries."""
    assert len(jiazi()) == 60


def test_jiazi_first_last():
    """First entry is 甲子, last is 癸亥."""
    cycle = jiazi()
    assert cycle[0] == "甲子"
    assert cycle[-1] == "癸亥"


def test_gangzhi_returns_five_elements():
    """gangzhi should return a list of 5 elements (year, month, day, hour, minute)."""
    result = gangzhi(2025, 6, 15, 10, 30)
    assert isinstance(result, list)
    assert len(result) == 5


def test_jq_returns_string():
    """jq should return the name of a solar term as a string."""
    result = jq(2025, 6, 15, 10, 30)
    assert isinstance(result, str)
    assert len(result) == 2  # Chinese solar term names are 2 characters


def test_wanji_four_gua_keys():
    """wanji_four_gua should return a dict with expected keys."""
    result = wanji_four_gua(2025, 6, 15, 10, 30)
    assert isinstance(result, dict)
    expected_keys = {"日期", "干支", "會", "運", "世", "運卦動爻", "世卦動爻", "旬卦動爻",
                     "正卦", "運卦", "世卦", "旬卦", "年卦", "月卦", "日卦", "時卦", "分卦"}
    assert set(result.keys()) == expected_keys

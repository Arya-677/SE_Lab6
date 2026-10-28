"""
Lab 6 - Code (line) coverage tests for visa_application.py
Name: Arya Devang        SRN: PES1UG24AM054

Run:
    coverage run -m pytest CodeCoverageTest_visa_application.py
    coverage report -m
"""
import pytest
from visa_application import visa_fee, documents_complete, application_status


# ---------------------------------------------------------------- visa_fee
def test_within_included_entries():
    assert visa_fee("tourist", 1, "normal", "B") == 0


def test_unknown_visa_type_raises():
    with pytest.raises(ValueError, match="unknown visa type"):
        visa_fee("diplomatic", 1, "normal", "B")


def test_negative_entries_raises():
    with pytest.raises(ValueError, match="invalid entries"):
        visa_fee("tourist", -1, "normal", "B")


def test_group_a_gets_bonus_entry_normal_speed():
    # tourist: 1 included + 1 bonus (group A) = 2; 3 entries -> 1 extra * 40
    assert visa_fee("tourist", 3, "normal", "A") == 40


def test_express_large_extra_surcharge():
    # tourist: 1 included; 8 entries -> 7 extra * (100 + 20 + 10)
    assert visa_fee("tourist", 8, "express", "B") == 910


# ------------------------------------------------------- documents_complete
def test_documents_complete():
    assert documents_complete(3, 2, False) is True


def test_documents_renewal_with_form():
    assert documents_complete(1, 0, True) is True


def test_documents_too_few_photos():
    assert documents_complete(3, 1, False) is False


def test_status_express_closing():
    assert application_status(5, True, False) == "closing"


def test_status_closed():
    assert application_status(0, False, False) == "closed"


def test_status_peak_season_raises_cutoff():
    # normal + peak -> cutoff 45, so 40 days is only "closing"
    assert application_status(40, False, True) == "closing"

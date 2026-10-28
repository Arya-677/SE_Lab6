"""
Lab 6 - Branch coverage tests for visa_application.py
Name: Arya Devang        SRN: PES1UG24AM054

Run:
    coverage run --branch -m pytest BranchCoverageTest_visa_application.py
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


def test_express_small_extra():
    # tourist, group B: 1 included; 3 entries -> 2 extra * 100
    assert visa_fee("tourist", 3, "express", "B") == 200


def test_normal_large_extra_surcharge():
    # business: 3 included; 9 entries -> 6 extra * (40 + 20)
    assert visa_fee("business", 9, "normal", "B") == 360


def test_express_large_extra_surcharge():
    # tourist: 1 included; 8 entries -> 7 extra * (100 + 20 + 10)
    assert visa_fee("tourist", 8, "express", "B") == 910


def test_student_group_a_gets_no_bonus_entry():
    # student, group A: condition `visa_type != "student"` is False -> 2 included
    assert visa_fee("student", 3, "normal", "B") == 40
    assert visa_fee("student", 3, "normal", "A") == 40


def test_group_a_business_express_exact_boundary():
    # business + A: 4 included; 4 entries -> extra == 0 -> free
    assert visa_fee("business", 4, "express", "A") == 0


def test_extra_exactly_five_has_no_surcharge():
    # tourist: 1 included; 6 entries -> extra == 5 (not > 5) -> 5 * 40
    assert visa_fee("tourist", 6, "normal", "B") == 200


# ------------------------------------------------------- documents_complete
def test_documents_complete():
    assert documents_complete(3, 2, False) is True


def test_documents_renewal_with_form():
    assert documents_complete(1, 0, True) is True


def test_documents_too_few_photos():
    assert documents_complete(3, 1, False) is False


def test_documents_too_few_forms():
    assert documents_complete(2, 2, False) is False


def test_renewal_without_forms():
    assert documents_complete(0, 5, True) is False


def test_documents_enough_forms_but_boundary_photos():
    assert documents_complete(3, 2, False) is True
    assert documents_complete(5, 0, False) is False


# ------------------------------------------------------ application_status
def test_status_normal_open():
    assert application_status(40, False, False) == "open"


def test_status_express_closing():
    assert application_status(5, True, False) == "closing"


def test_status_closed():
    assert application_status(0, False, False) == "closed"


def test_status_peak_season_raises_cutoff():
    # normal + peak -> cutoff 45, so 40 days is only "closing"
    assert application_status(40, False, True) == "closing"


def test_status_express_open_at_cutoff():
    assert application_status(10, True, False) == "open"


def test_status_express_peak_boundaries():
    # express + peak -> cutoff 25; closing window is 10..24
    assert application_status(25, True, True) == "open"
    assert application_status(10, True, True) == "closing"
    assert application_status(9, True, True) == "closed"


def test_status_normal_closing_lower_boundary():
    assert application_status(15, False, False) == "closing"
    assert application_status(14, False, False) == "closed"

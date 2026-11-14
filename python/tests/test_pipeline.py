
import pandas as pd

from python.src.validator import (
    validate_columns,
    validate_reference,
    validate_refund_origin,
    validation_results
)


# ==================================================
# 1. REQUIRED COLUMN TESTS
# ==================================================

def test_required_columns_pass():

    df = pd.DataFrame({
        "order_id": ["A1", "A2"],
        "customer_id": ["C1", "C2"]
    })

    assert validate_columns(
        "test_orders",
        df,
        ["order_id", "customer_id"]
    ) is True


def test_required_columns_fail():

    df = pd.DataFrame({
        "order_id": ["A1", "A2"]
    })

    assert validate_columns(
        "test_orders",
        df,
        ["order_id", "customer_id"]
    ) is False


# ==================================================
# 2. DUPLICATE TESTS
# ==================================================

def test_duplicate_records():

    df = pd.DataFrame({
        "order_id": ["A1", "A1", "A2"]
    })

    assert df.duplicated(
        subset=["order_id"]
    ).sum() == 1


def test_no_duplicate_records():

    df = pd.DataFrame({
        "order_id": ["A1", "A2", "A3"]
    })

    assert df.duplicated(
        subset=["order_id"]
    ).sum() == 0


# ==================================================
# 3. REFERENTIAL INTEGRITY TESTS
# ==================================================

def test_valid_order_reference():

    validation_results.clear()

    orders = pd.DataFrame({
        "order_id": ["O1", "O2", "O3"]
    })

    payments = pd.DataFrame({
        "order_id": ["O1", "O2"]
    })

    validate_reference(
        "payments",
        payments,
        "order_id",
        "orders",
        orders,
        "order_id"
    )

    assert validation_results[-1]["status"] == "PASSED"


def test_invalid_order_reference():

    validation_results.clear()

    orders = pd.DataFrame({
        "order_id": ["O1", "O2"]
    })

    payments = pd.DataFrame({
        "order_id": ["O1", "O3"]
    })

    validate_reference(
        "payments",
        payments,
        "order_id",
        "orders",
        orders,
        "order_id"
    )

    assert validation_results[-1]["status"] == "FAILED"
    assert validation_results[-1]["count"] == 1


# ==================================================
# 4. SYNTHETIC REFUND TESTS
# ==================================================

def test_synthetic_refund_origin():

    validation_results.clear()

    refunds = pd.DataFrame({
        "data_origin": [
            "SYNTHETIC",
            "SYNTHETIC"
        ]
    })

    validate_refund_origin(refunds)

    assert validation_results[-1]["status"] == "PASSED"


def test_invalid_refund_origin():

    validation_results.clear()

    refunds = pd.DataFrame({
        "data_origin": [
            "SYNTHETIC",
            "ACTUAL"
        ]
    })

    validate_refund_origin(refunds)

    assert validation_results[-1]["status"] == "FAILED"
    assert validation_results[-1]["count"] == 1


from pathlib import Path

# ==================================================
# RTRW PROJECT PATHS
# ==================================================

# Project root: RTRW/
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Dataset directories
RAW_DATA_DIR = PROJECT_ROOT / "datasets" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "datasets" / "processed"

# Python output directories
REPORT_DIR = PROJECT_ROOT / "python" / "reports"
LOG_DIR = PROJECT_ROOT / "python" / "logs"


# ==================================================
# CREATE REQUIRED DIRECTORIES
# ==================================================

for directory in [
    PROCESSED_DATA_DIR,
    REPORT_DIR,
    LOG_DIR
]:
    directory.mkdir(
        parents=True,
        exist_ok=True
    )


# ==================================================
# DATASET VALIDATION CONFIGURATION
# ==================================================

DATASET_CONFIG = {

    # ------------------------------------------------
    # 1. ORDERS
    # ------------------------------------------------

    "orders": {
        "file": "olist_orders_dataset.csv",

        "required_columns": [
            "order_id",
            "customer_id",
            "order_status",
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date"
        ],

        "unique_key": [
            "order_id"
        ],

        "date_columns": [
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date"
        ],

        "numeric_columns": [],

        "amount_columns": [],

        "required_non_null": [
            "order_id",
            "customer_id",
            "order_status",
            "order_purchase_timestamp"
        ]
    },


    # ------------------------------------------------
    # 2. PAYMENTS
    # ------------------------------------------------

    "payments": {
        "file": "olist_order_payments_dataset.csv",

        "required_columns": [
            "order_id",
            "payment_sequential",
            "payment_type",
            "payment_installments",
            "payment_value"
        ],

        "unique_key": [
            "order_id",
            "payment_sequential"
        ],

        "date_columns": [],

        "numeric_columns": [
            "payment_sequential",
            "payment_installments",
            "payment_value"
        ],

        "amount_columns": [
            "payment_value"
        ],

        "required_non_null": [
            "order_id",
            "payment_sequential",
            "payment_type",
            "payment_value"
        ]
    },


    # ------------------------------------------------
    # 3. ORDER ITEMS
    # ------------------------------------------------

    "order_items": {
        "file": "olist_order_items_dataset.csv",

        "required_columns": [
            "order_id",
            "order_item_id",
            "product_id",
            "seller_id",
            "shipping_limit_date",
            "price",
            "freight_value"
        ],

        "unique_key": [
            "order_id",
            "order_item_id"
        ],

        "date_columns": [
            "shipping_limit_date"
        ],

        "numeric_columns": [
            "order_item_id",
            "price",
            "freight_value"
        ],

        "amount_columns": [
            "price",
            "freight_value"
        ],

        "required_non_null": [
            "order_id",
            "order_item_id",
            "product_id",
            "seller_id",
            "price",
            "freight_value"
        ]
    },


    # ------------------------------------------------
    # 4. CUSTOMERS
    # ------------------------------------------------

    "customers": {
        "file": "olist_customers_dataset.csv",

        "required_columns": [
            "customer_id",
            "customer_unique_id",
            "customer_zip_code_prefix",
            "customer_city",
            "customer_state"
        ],

        "unique_key": [
            "customer_id"
        ],

        "date_columns": [],

        "numeric_columns": [],

        "amount_columns": [],

        "required_non_null": [
            "customer_id",
            "customer_unique_id"
        ]
    },


    # ------------------------------------------------
    # 5. SELLERS
    # ------------------------------------------------

    "sellers": {
        "file": "olist_sellers_dataset.csv",

        "required_columns": [
            "seller_id",
            "seller_zip_code_prefix",
            "seller_city",
            "seller_state"
        ],

        "unique_key": [
            "seller_id"
        ],

        "date_columns": [],

        "numeric_columns": [],

        "amount_columns": [],

        "required_non_null": [
            "seller_id"
        ]
    },


    # ------------------------------------------------
    # 6. PRODUCTS
    # ------------------------------------------------

    "products": {
        "file": "olist_products_dataset.csv",

        "required_columns": [
            "product_id",
            "product_category_name",
            "product_name_lenght",
            "product_description_lenght",
            "product_photos_qty",
            "product_weight_g",
            "product_length_cm",
            "product_height_cm",
            "product_width_cm"
        ],

        "unique_key": [
            "product_id"
        ],

        "date_columns": [],

        "numeric_columns": [
            "product_name_lenght",
            "product_description_lenght",
            "product_photos_qty",
            "product_weight_g",
            "product_length_cm",
            "product_height_cm",
            "product_width_cm"
        ],

        "amount_columns": [],

        "required_non_null": [
            "product_id"
        ]
    },


    # ------------------------------------------------
    # 7. SYNTHETIC REFUNDS
    # ------------------------------------------------

    "refunds": {
        "file": "refunds_dataset.csv",

        "required_columns": [
            "refund_id",
            "order_id",
            "customer_id",
            "refund_date",
            "refund_amount",
            "restocking_fee",
            "tax_refunded",
            "refund_status",
            "refund_type",
            "currency",
            "data_origin"
        ],

        "unique_key": [
            "refund_id"
        ],

        "date_columns": [
            "refund_date"
        ],

        "numeric_columns": [
            "refund_amount",
            "restocking_fee",
            "tax_refunded"
        ],

        "amount_columns": [
            "refund_amount",
            "restocking_fee",
            "tax_refunded"
        ],

        "required_non_null": [
            "refund_id",
            "order_id",
            "customer_id",
            "refund_date",
            "refund_amount",
            "data_origin"
        ]
    }

}


# ==================================================
# POSTAL CODE COLUMNS
# Keep these as strings to preserve leading zeros.
# ==================================================

STRING_COLUMNS = [
    "customer_zip_code_prefix",
    "seller_zip_code_prefix"
]

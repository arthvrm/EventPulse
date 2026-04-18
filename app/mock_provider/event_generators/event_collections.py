STRIPE_EVENT_STATUS_MAP = {
    "payment_intent.succeeded": "COMPLETED",
    "payment_intent.payment_failed": "FAILED",
    "payment_intent.canceled": "CANCELED",
    "charge.succeeded": "COMPLETED",
    "charge.failed": "FAILED",
    "charge.refunded": "REFUNDED",
    "invoice.payment_succeeded": "COMPLETED",
    "invoice.payment_failed": "FAILED",
    "checkout.session.completed": "COMPLETED"
}

STRIPE_FAILURE_REASON_MAP = {
    "payment_intent.payment_failed": [
        "card_declined",
        "insufficient_funds",
        "expired_card"
    ],
    "charge.failed": [
        "do_not_honor",
        "processing_error"
    ]
}

PAYPAL_EVENT_STATUS_MAP = {
    "CHECKOUT.ORDER.APPROVED": "APPROVED",
    "CHECKOUT.ORDER.COMPLETED": "COMPLETED",

    "PAYMENT.AUTHORIZATION.CREATED": "AUTHORIZED",
    "PAYMENT.AUTHORIZATION.VOIDED": "VOIDED",

    "PAYMENT.CAPTURE.COMPLETED": "COMPLETED",
    "PAYMENT.CAPTURE.DENIED": "DENIED",
    "PAYMENT.CAPTURE.FAILED": "FAILED",
    "PAYMENT.CAPTURE.PENDING": "PENDING",
    "PAYMENT.CAPTURE.REFUNDED": "REFUNDED",
    "PAYMENT.CAPTURE.REVERSED": "REVERSED"
}

PAYPAL_FAILURE_REASON_MAP = {
    "PAYMENT.CAPTURE.DENIED": [
        "INSUFFICIENT_FUNDS",
        "CARD_DECLINED",
        "EXPIRED_CARD"
    ],
    "PAYMENT.CAPTURE.FAILED": [
        "TECHNICAL_ERROR",
        "PROCESSING_ERROR",
        "NETWORK_FAILURE"
    ],
    "PAYMENT.CAPTURE.REVERSED": [
        "CHARGEBACK",
        "DISPUTE_LOST"
    ],
    "PAYMENT.AUTHORIZATION.VOIDED": [
        "USER_CANCELED",
        "FRAUD_SUSPECTED"
    ]
}

PAYPAL_RESOURCE_TYPE_MAP = {
    "CHECKOUT.ORDER": "checkout-order",
    "PAYMENT.CAPTURE": "capture",
    "PAYMENT.AUTHORIZATION": "authorization"
}

NAMES = [
    "Artem Kovalenko",
    "Ivan Shevchenko",
    "Olena Melnyk",
    "Maksym Bondarenko",
    "Sofiia Tkachenko",
    "Danylo Koval",
    "Anastasiia Boyko",
    "Andrii Kravets",
    "Yulia Marchenko",
    "Taras Hrytsenko"
]

PRODUCTS = [
    ("Lo-fi Beats Subscription", "DIGITAL_GOODS", 9.99),
    ("Streetwear Oversized Hoodie", "PHYSICAL_GOODS", 49.99),
    ("AI Avatar Generator Credits", "DIGITAL_GOODS", 9.99),
    ("Gaming Mouse RGB", "PHYSICAL_GOODS", 29.99),
    ("Indie Game Bundle", "DIGITAL_GOODS", 14.99),
    ("Crypto Trading Course", "DIGITAL_GOODS", 59.99),
    ("Wireless Earbuds", "PHYSICAL_GOODS", 79.99),
    ("Anime Figurine", "PHYSICAL_GOODS", 34.99),
    ("Spotify Premium Gift", "DIGITAL_GOODS", 19.99),
    ("Online Fitness Program", "DIGITAL_GOODS", 24.99)
]

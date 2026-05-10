from paypal import PayPalNormalizer
from stripe import StripeNormalizer

NORMALIZERS = {
    "stripe": StripeNormalizer(),
    "paypal": PayPalNormalizer(),
}
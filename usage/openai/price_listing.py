from usage.base.price_listing import PRICE_LISTINGS, PriceListing
from usage.openai.types import SERVICE_NAME

PRICE_LISTINGS[f"{SERVICE_NAME}-gpt-4-0125-preview"] = PriceListing(
    input_token_price=0.0001,
    output_token_price=0.0003,
)
PRICE_LISTINGS[f"{SERVICE_NAME}-gpt-4-1106-preview"] = PriceListing(
    input_token_price=0.0001,
    output_token_price=0.0003,
)
PRICE_LISTINGS[f"{SERVICE_NAME}-gpt-3.5-turbo-0125"] = PriceListing(
    input_token_price=0.0000005,
    output_token_price=0.0000015,
)

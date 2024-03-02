from abc import ABC

from pydantic import BaseModel, Field


class PriceListing(BaseModel):
    input_token_price: float = Field()
    output_token_price: float = Field()


PRICE_LISTINGS: dict[str, PriceListing] = {}

from __future__ import annotations
from . import (
    i80f48,
)
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class Serum3InfoJSON(typing.TypedDict):
    reserved_base: i80f48.I80F48JSON
    reserved_quote: i80f48.I80F48JSON
    base_index: int
    quote_index: int
    market_index: int
    has_zero_funds: bool


@dataclass
class Serum3Info:
    layout: typing.ClassVar = borsh.CStruct(
        "reserved_base" / i80f48.I80F48.layout,
        "reserved_quote" / i80f48.I80F48.layout,
        "base_index" / borsh.U64,
        "quote_index" / borsh.U64,
        "market_index" / borsh.U16,
        "has_zero_funds" / borsh.Bool,
    )
    reserved_base: i80f48.I80F48
    reserved_quote: i80f48.I80F48
    base_index: int
    quote_index: int
    market_index: int
    has_zero_funds: bool

    @classmethod
    def from_decoded(cls, obj: Container) -> "Serum3Info":
        return cls(
            reserved_base=i80f48.I80F48.from_decoded(obj.reserved_base),
            reserved_quote=i80f48.I80F48.from_decoded(obj.reserved_quote),
            base_index=obj.base_index,
            quote_index=obj.quote_index,
            market_index=obj.market_index,
            has_zero_funds=obj.has_zero_funds,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "reserved_base": self.reserved_base.to_encodable(),
            "reserved_quote": self.reserved_quote.to_encodable(),
            "base_index": self.base_index,
            "quote_index": self.quote_index,
            "market_index": self.market_index,
            "has_zero_funds": self.has_zero_funds,
        }

    def to_json(self) -> Serum3InfoJSON:
        return {
            "reserved_base": self.reserved_base.to_json(),
            "reserved_quote": self.reserved_quote.to_json(),
            "base_index": self.base_index,
            "quote_index": self.quote_index,
            "market_index": self.market_index,
            "has_zero_funds": self.has_zero_funds,
        }

    @classmethod
    def from_json(cls, obj: Serum3InfoJSON) -> "Serum3Info":
        return cls(
            reserved_base=i80f48.I80F48.from_json(obj["reserved_base"]),
            reserved_quote=i80f48.I80F48.from_json(obj["reserved_quote"]),
            base_index=obj["base_index"],
            quote_index=obj["quote_index"],
            market_index=obj["market_index"],
            has_zero_funds=obj["has_zero_funds"],
        )

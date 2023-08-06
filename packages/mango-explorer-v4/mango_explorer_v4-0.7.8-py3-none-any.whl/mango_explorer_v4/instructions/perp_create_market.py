from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.system_program import SYS_PROGRAM_ID
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class PerpCreateMarketArgs(typing.TypedDict):
    perp_market_index: int
    name: str
    oracle_config: types.oracle_config_params.OracleConfigParams
    base_decimals: int
    quote_lot_size: int
    base_lot_size: int
    maint_base_asset_weight: float
    init_base_asset_weight: float
    maint_base_liab_weight: float
    init_base_liab_weight: float
    maint_overall_asset_weight: float
    init_overall_asset_weight: float
    base_liquidation_fee: float
    maker_fee: float
    taker_fee: float
    min_funding: float
    max_funding: float
    impact_quantity: int
    group_insurance_fund: bool
    fee_penalty: float
    settle_fee_flat: float
    settle_fee_amount_threshold: float
    settle_fee_fraction_low_health: float
    settle_token_index: int
    settle_pnl_limit_factor: float
    settle_pnl_limit_window_size_ts: int
    positive_pnl_liquidation_fee: float


layout = borsh.CStruct(
    "perp_market_index" / borsh.U16,
    "name" / borsh.String,
    "oracle_config" / types.oracle_config_params.OracleConfigParams.layout,
    "base_decimals" / borsh.U8,
    "quote_lot_size" / borsh.I64,
    "base_lot_size" / borsh.I64,
    "maint_base_asset_weight" / borsh.F32,
    "init_base_asset_weight" / borsh.F32,
    "maint_base_liab_weight" / borsh.F32,
    "init_base_liab_weight" / borsh.F32,
    "maint_overall_asset_weight" / borsh.F32,
    "init_overall_asset_weight" / borsh.F32,
    "base_liquidation_fee" / borsh.F32,
    "maker_fee" / borsh.F32,
    "taker_fee" / borsh.F32,
    "min_funding" / borsh.F32,
    "max_funding" / borsh.F32,
    "impact_quantity" / borsh.I64,
    "group_insurance_fund" / borsh.Bool,
    "fee_penalty" / borsh.F32,
    "settle_fee_flat" / borsh.F32,
    "settle_fee_amount_threshold" / borsh.F32,
    "settle_fee_fraction_low_health" / borsh.F32,
    "settle_token_index" / borsh.U16,
    "settle_pnl_limit_factor" / borsh.F32,
    "settle_pnl_limit_window_size_ts" / borsh.U64,
    "positive_pnl_liquidation_fee" / borsh.F32,
)


class PerpCreateMarketAccounts(typing.TypedDict):
    group: PublicKey
    admin: PublicKey
    oracle: PublicKey
    perp_market: PublicKey
    bids: PublicKey
    asks: PublicKey
    event_queue: PublicKey
    payer: PublicKey


def perp_create_market(
    args: PerpCreateMarketArgs,
    accounts: PerpCreateMarketAccounts,
    program_id: PublicKey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["group"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["oracle"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["perp_market"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["bids"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["asks"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["event_queue"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["payer"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b']/-\xc3>\xfc "'
    encoded_args = layout.build(
        {
            "perp_market_index": args["perp_market_index"],
            "name": args["name"],
            "oracle_config": args["oracle_config"].to_encodable(),
            "base_decimals": args["base_decimals"],
            "quote_lot_size": args["quote_lot_size"],
            "base_lot_size": args["base_lot_size"],
            "maint_base_asset_weight": args["maint_base_asset_weight"],
            "init_base_asset_weight": args["init_base_asset_weight"],
            "maint_base_liab_weight": args["maint_base_liab_weight"],
            "init_base_liab_weight": args["init_base_liab_weight"],
            "maint_overall_asset_weight": args["maint_overall_asset_weight"],
            "init_overall_asset_weight": args["init_overall_asset_weight"],
            "base_liquidation_fee": args["base_liquidation_fee"],
            "maker_fee": args["maker_fee"],
            "taker_fee": args["taker_fee"],
            "min_funding": args["min_funding"],
            "max_funding": args["max_funding"],
            "impact_quantity": args["impact_quantity"],
            "group_insurance_fund": args["group_insurance_fund"],
            "fee_penalty": args["fee_penalty"],
            "settle_fee_flat": args["settle_fee_flat"],
            "settle_fee_amount_threshold": args["settle_fee_amount_threshold"],
            "settle_fee_fraction_low_health": args["settle_fee_fraction_low_health"],
            "settle_token_index": args["settle_token_index"],
            "settle_pnl_limit_factor": args["settle_pnl_limit_factor"],
            "settle_pnl_limit_window_size_ts": args["settle_pnl_limit_window_size_ts"],
            "positive_pnl_liquidation_fee": args["positive_pnl_liquidation_fee"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, program_id, data)

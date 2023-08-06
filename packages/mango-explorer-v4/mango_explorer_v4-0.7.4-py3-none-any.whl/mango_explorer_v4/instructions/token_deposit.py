from __future__ import annotations
import typing
from solana.publickey import PublicKey
from spl.token.constants import TOKEN_PROGRAM_ID
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class TokenDepositArgs(typing.TypedDict):
    amount: int
    reduce_only: bool


layout = borsh.CStruct("amount" / borsh.U64, "reduce_only" / borsh.Bool)


class TokenDepositAccounts(typing.TypedDict):
    group: PublicKey
    account: PublicKey
    owner: PublicKey
    bank: PublicKey
    vault: PublicKey
    oracle: PublicKey
    token_account: PublicKey
    token_authority: PublicKey


def token_deposit(
    args: TokenDepositArgs,
    accounts: TokenDepositAccounts,
    program_id: PublicKey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["group"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["account"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["owner"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["bank"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["vault"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["oracle"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["token_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["token_authority"], is_signer=True, is_writable=False
        ),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"u\xff\x9aG\xf5:_Y"
    encoded_args = layout.build(
        {
            "amount": args["amount"],
            "reduce_only": args["reduce_only"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, program_id, data)

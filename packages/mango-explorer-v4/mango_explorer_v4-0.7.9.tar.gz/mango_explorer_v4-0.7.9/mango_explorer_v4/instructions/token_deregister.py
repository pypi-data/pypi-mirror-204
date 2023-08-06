from __future__ import annotations
import typing
from solana.publickey import PublicKey
from spl.token.constants import TOKEN_PROGRAM_ID
from solana.transaction import TransactionInstruction, AccountMeta
from ..program_id import PROGRAM_ID


class TokenDeregisterAccounts(typing.TypedDict):
    group: PublicKey
    admin: PublicKey
    mint_info: PublicKey
    dust_vault: PublicKey
    sol_destination: PublicKey


def token_deregister(
    accounts: TokenDeregisterAccounts,
    program_id: PublicKey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["group"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["mint_info"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["dust_vault"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["sol_destination"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"Rf&C\x87\xc7\x84."
    encoded_args = b""
    data = identifier + encoded_args
    return TransactionInstruction(keys, program_id, data)

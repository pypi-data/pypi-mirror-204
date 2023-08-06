import argparse
import asyncio

from ..mango_client import MangoClient


async def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--mango-account',
        help='Mango account primary key.',
        required=True
    )

    args = parser.parse_args()

    mango_client = await MangoClient.connect()

    mango_account = await mango_client.get_mango_account(args.mango_account)

    print(await mango_client.positions(mango_account))

    # Example output:
    # {
    #   'BTC-PERP': {
    #       'size': -0.0492,
    #       'notional': -1344.6361230369,
    #       'entry_price': 28370.277029292287,
    #       'oracle_price': 27330.00250075,
    #       'unsettled_pnl': 33.75017664508752,
    #       'pnl': 185.00809608116452
    #   }
    #   ...
    # }


if __name__ == '__main__':
    asyncio.run(main())

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

    print(await mango_client.balances(mango_account))

    # Example output:
    # {
    # 'MSOL': {'balance': 0.0, 'in_orders': 0.0, 'unsettled': 0.0},
    # 'SOL': {'balance': 0.08695266961087615, 'in_orders': 0.0, 'unsettled': 0.0},
    # 'USDC': {'balance': 3.406757116516584, 'in_orders': 0.4, 'unsettled': 1e-05}
    # }


if __name__ == '__main__':
    asyncio.run(main())

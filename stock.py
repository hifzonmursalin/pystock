import sys
import requests as rq

fh_token = "TODO: Your token here"

args = sys.argv


def args_check():
    if len(args) == 2 or len(args) > 2:
        return True
    else:
        return False


def fetch(company: str):
    price_url = f'https://finnhub.io/api/v1/quote?symbol={company}&token={fh_token}'
    price = rq.get(price_url).json()
    return price


def process(cmp_args):
    company = cmp_args.upper()
    price = fetch(company)
    comp_name = rq.get(f'https://finnhub.io/api/v1/search?q={company}&token={fh_token}').json()
    try:
        comp_name = comp_name['result'][0]['description']
    except IndexError:
        print("Sorry, but the stocks you're trying to look for is unavailable.")
        exit(1)
    phrase = f"Stock for {company} ({comp_name}) is {price['c']}, while its last price is {price['pc']}"

    if phrase == f"Stock for {company} ({comp_name}) is 0, while its last price is 0":
        print("Sorry, but the stocks you're trying to look for is unavailable.")
        exit(1)

    print(f"===========\n{phrase}\n===========")
    if price['c'] > price['pc']:
        increase = price['c'] - price['pc']
        original_number = price['c']
        print(f"+{round(increase / original_number * 100, 2)}%")
    if price['c'] < price['pc']:
        decrease = price['pc'] - price['c']
        original_number = price['c']
        print(f"-{round(decrease / original_number * 100, 2)}%")


if __name__ == '__main__':
    if args_check():
        process(args[1])

    else:
        print("You don't pass any argument, please input stock symbol.")
        inp = input("pystock: ")
        process(inp)

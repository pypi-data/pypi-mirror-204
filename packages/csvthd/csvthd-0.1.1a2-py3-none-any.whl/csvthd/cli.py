# built in
from datetime import datetime

# site
import click

# package
from .filters import details_include_filter, amount_is_filter
from .commandline import print_transaction
from .transactions import get_transactions
from .config import load_config

# TODO: consider looking into (odx?) other formats because someone mentioned apparently there
# ... are some other commons ones that are standardized.

# TODO: add option to get calculate total sum of filtered out transactions


@click.command()
@click.option(
    "-i",
    "--include",
    multiple=True,
    help="Only show transactions that contain the given substring in their details.",
)
@click.option(
    "-a",
    "--amount",
    multiple=True,
    nargs=2,
    help="Only show transactions with amounts under/over/equal to value.",
)
@click.option(
    "-s",
    "--sort-by",
    type=click.Choice(["date", "amount"]),
    default="date",
    help="Sort transactions by given property.",
)
@click.option(
    "-r", "--reverse-sort", is_flag=True, help="Reverse sorting order."
)
def cli(include, amount, sort_by, reverse_sort):
    filters = []

    # create an include filter for each include arg and append each to filter array
    filters.append(details_include_filter(include))

    # create amount is filters
    [filters.append(amount_is_filter(_amt[0], _amt[1])) for _amt in amount]

    config = load_config()
    transactions = get_transactions(config["files"])

    # sort transactions
    if sort_by == "date":
        transactions.sort(
            key=lambda t: datetime.strptime(t["date"], "%d/%m/%Y").timestamp(),
            reverse=reverse_sort,
        )
    elif sort_by == "amount":
        transactions.sort(key=lambda t: t["amount"], reverse=reverse_sort)
    else:
        raise ValueError("Invalid 'sort_by' type")

    # apply all filters
    for _filter in filters:
        transactions = filter(_filter, transactions)

    print("---[ TRANSACTIONS ]---")
    for transaction in transactions:
        print_transaction(transaction)

    if len(filters) == 0:
        print("\nHint: Use `--help` to learn how to filter transactions.")

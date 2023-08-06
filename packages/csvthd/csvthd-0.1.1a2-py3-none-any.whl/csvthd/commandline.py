RED_BACK = "\033[41m"
GREEN_BACK = "\033[42m"
ANSI_RESET = "\033[0m"


def print_transaction(transaction):
    _amount = transaction["amount"]

    AMOUNT_COLOUR = RED_BACK if _amount < 0 else GREEN_BACK

    print(
        # TODO: find the longest account name string and use it change string formatting padding size
        f"[{transaction['account_name']:^25}] "
        + transaction["date"]
        + " | AMT: "
        + f"{AMOUNT_COLOUR}{_amount:>8.2f}{ANSI_RESET} | "
        + transaction["details"]
    )

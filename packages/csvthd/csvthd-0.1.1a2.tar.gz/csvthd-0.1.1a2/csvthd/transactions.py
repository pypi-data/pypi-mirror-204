# built in
import csv


def get_transactions(files):
    transactions = []
    for _file in files:
        with open(_file["filepath"], "r", newline="", encoding="utf-8") as f:
            rowreader = csv.reader(f)
            for idx, row in enumerate(rowreader):
                # print(row)

                # skip header row if it has one
                if _file["hasHeaderRow"] is True and idx == 0:
                    continue

                transactions.append(
                    {
                        "date": row[_file["dateIdx"]],
                        "amount": float(row[_file["amountIdx"]]),
                        "details": row[_file["detailsIdx"]],
                        "balance_at_time_of_transaction": row[
                            _file["balanceIdx"]
                        ],
                        "account_name": _file["accountName"],
                    }
                )
    return transactions

def details_include_filter(substrings):
    """Filter out transactions that don't match all substrings (case insensitive)."""
    # lowercase all substrings
    substrings = [ss.lower() for ss in substrings]

    def _func(transaction):
        # get lowercase version of transaction details
        _details = transaction["details"].lower()

        # for each substring
        for substring in substrings:
            # if the substring isn't contained in details
            if not substring in _details:
                return False
        # if not substrings haven't matched transaction details
        return True

    return _func


def amount_is_filter(operator, value):
    """Filter out transactions based on amounts.

    Operator is `under`, `over` or `equal`.
    Value is a float.
    """

    value = float(value)

    def _func(transaction):
        # convert amount to float
        _amount = float(transaction["amount"])

        if operator == "under":
            # if amount under zero, flip sign for comparison
            _amount = abs(_amount)
            return _amount < value
        elif operator == "over":
            # if amount under zero, flip sign for comparison
            _amount = abs(_amount)
            return _amount > value
        elif operator == "equal":
            return _amount == value
        else:
            raise ValueError("Operator must by `above`, `below` or `equal`")

    return _func

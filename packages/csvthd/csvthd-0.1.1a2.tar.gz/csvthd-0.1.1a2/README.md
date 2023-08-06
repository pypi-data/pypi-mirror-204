# CSV Transaction History Detective

## Getting started

1. [Install](https://gitlab.com/DrTexx/csv-transaction-history-detective/#installation) `csvthd`
2. Create your `config.json` file (see [`config.json.example.md`](https://gitlab.com/DrTexx/csv-transaction-history-detective/-/blob/main/config.json.example.md) for a template)
3. See [usage](https://gitlab.com/DrTexx/csv-transaction-history-detective/#usage)

## Installation

```bash
pip install csvthd
```

## Usage

### Show help

```bash
csvthd --help
```

### Filter

#### Transaction details

`-i/--include`

Only show transactions that include **all** of the specified strings in their details

- Case insensitive
- Multiple strings supported (each transaction's details must include **all** of the strings specified)

```bash
# only show transactions with details including the word "paypal"
csvthd -i paypal

# only show transactions with details including "paypal" and "steam"
csvthd -i paypal -i steam
```

#### Amount

`-a/--amount`

Only show transactions with amounts under/over/equal to a given value

- Multiple numbers supported (each transaction amount must satisfy **all** conditions specified)

```bash
# only show transactions over $20.00
csvthd -a over 20

# only show transactions under $10.00
csvthd -a under 10

# only show transactions between $20.00 to $30.00
csvthd -a over 20 -a under 30

# only show transactions of exactly $25.00
csvthd -a equal 25
```

### Sorting

#### Sort by

`-s/--sort-by`

```bash
# sort by date (default)
csvthd -s date

# sort by amount
csvthd -s amount 
```

#### Reverse sorting order

`-r/--reverse-sort`

```bash
csvthd -r # reverse sort order
```

## Development

### Build

```bash
./development-scripts/build.sh
```

## Links

<!-- TODO: add website link -->
- 📖 &nbsp;[Documentation](https://gitlab.com/DrTexx/csv-transaction-history-detective)
- 🐍 &nbsp;[Latest Release](https://pypi.org/project/csvthd)
- 🧰 &nbsp;[Source Code](https://gitlab.com/DrTexx/csv-transaction-history-detective)
- 🐞 &nbsp;[Issue Tracker](https://gitlab.com/DrTexx/csv-transaction-history-detective/-/issues)
- `🐦 Twitter` &nbsp;[@DrTexx](https://twitter.com/DrTexx)
- `📨 Email` &nbsp;[denver.opensource@tutanota.com](mailto:denver.opensource@tutanota.com)

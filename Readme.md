
# Tool for OFX files
* converts to onscreen tabular text format
* *convert to csv* (not yet implemented)
* *build a gui where data can be ordered by field etc...* (not yet implemented)

# Usage
This is a very rough start... I needed to get something quick, and will hopefully be able to clean it up soon.
`pyvenv3 .
pip install -r Requirements.txt
yofx/yofx.py -f filename totext
`

# Example
```
account number: 1062739485
account routing_number: 00202899
start_date: 1937-04-01 06:00:00
end_date: 2024-03-31 17:59:59
balance: 1.00

           ID             |         DATE         |  AMOUNT   |           PAYEE           |                           MEMO                            | CHECKNUM | SIC  | MCC |  TYPE  |
c4f606d775c7f99d172548df4 | 2016-01-31 08:00:00  |      0.99 | DEPOSIT INTEREST          |                                                           |          | None |     |    int |
0ae540a5e5fd3cb5cb299097b | 2016-01-31 08:00:00  |    -10.00 | SERVICE CHARGE            |                                                           |          | None |     |    fee |
f62e5bcda4fae4f82370da0c6 | 2016-01-31 08:00:00  |    -22.00 | WOODGROVE-TELEBANKING FEE |                                                           |          | None |     |  debit |
e0177968e866407e29db40b4a | 2016-01-30 08:00:00  |   -200.00 | BILL PMT - INTERNET       | SOUTH SHORE LINE              Confirmation # 000009739812 |          | None |     |  debit |
8c42a99f2faf0570422e0e440 | 2016-01-21 08:00:00  |   1260.00 | CHEQUE DEPOSIT            | W/ THANKS HANNON FULLER                                   |          | None |     |  debit |
83ac309ea37fd05775b107d09 | 2035-01-18 08:00:00  | -98765.43 | BILL PMT - INTERNET       | LUNAR INDUSTRIES  RESCUE MISS Confirmation # 000000378319 |          | None |     |  debit |
8c42a99f2faf0570422e0e440 | 2011-03-11 07:40:00  |   5272.00 | CHEQUE DEPOSIT            | ARMY SALARY COLTER STEVENS
```

h1. TODO / ideas
* pick/add license
* gui (tk?)
* Use xml.etree and eliminate dependencies?


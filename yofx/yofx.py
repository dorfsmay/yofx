#!/usr/bin/env python3

import argparse
from ofxparse import OfxParser
from collections import OrderedDict
import logging

logging.basicConfig(format='==> %(module)s, %(funcName)s %(message)s', level=logging.ERROR)

def calculate_fields_sizes(ofx):
    fields_sizes = dict()
    for t in ofx.account.statement.transactions:
        for f in [ f for f in dir(t) if not f.startswith('_') ]:
            logging.debug("field: {}".format(f))
            this = getattr(t, f)
            if type(this) is str:
                length = len(this)
            else:
                length = len(str(this))
            logging.debug("new length: {}".format(length))
            if (f not in fields_sizes) or (length > fields_sizes[f]):
                logging.debug("updating {} with {}".format(f, length))
                fields_sizes[f] = length
    return fields_sizes

def pick_longest(name, length):
    name_length = len(name)
    if length == 0 or name_length > length:
        length = name_length
        logging.debug("===> {}, {}".format(name, length))
    return length

def totext(ofx):
    fields_sizes = calculate_fields_sizes(ofx)
    # At this point we assume that a few of the fields are always present.
    # 'amount', 'checknum', 'date', 'id', 'mcc', 'memo', 'payee', 'sic', 'type'
    # TODO: Verify this assumption

    fields = list()
    # establish order
    d = dict()
    d['name'] = 'id'
    d['length'] = pick_longest(d['name'], fields_sizes.pop(d['name']))
    d['format'] = "{{:<{}s}} |".format(d['length'])
    d['convert'] = False
    fields.append(d)

    d = dict()
    d['name'] = 'date'
    d['length'] = 20  # lenght converted to str
    _ = fields_sizes.pop('date')
    d['format'] = " {{:^{}s}} |".format(d['length'])
    d['convert'] = True
    fields.append(d)

    d = dict()
    d['name'] = 'amount'
    # we adjust the length for the additional coma for the thousands
    l = fields_sizes.pop(d['name'])
    l = l + int((l - 3)/3)
    d['length'] = pick_longest(d['name'], l)
    d['format'] = " {{:> {},f}} |".format(d['length'])
    d['convert'] = False
    fields.append(d)

    d = dict()
    d['name'] = 'payee'
    d['length'] = pick_longest(d['name'], fields_sizes.pop(d['name']))
    d['format'] = " {{:<{}s}} |".format(d['length'])
    d['convert'] = False
    fields.append(d)

    d = dict()
    d['name'] = 'memo'
    d['length'] = pick_longest(d['name'], fields_sizes.pop(d['name']))
    d['format'] = " {{:<{}s}} |".format(d['length'])
    d['convert'] = False
    fields.append(d)

    # Field I don't use or that I don't know about
    for f, l in fields_sizes.items():
        d = dict()
        d['name'] = f
        d['length'] = pick_longest(f, l)
        d['format'] = " {{:>{}s}} |".format(d['length'])
        d['convert'] = True
        fields.append(d)

    del fields_sizes

    # print account information
    print()
    for item in ('number', 'routing_number',):
        try:
            print("account {}: {}".format(item, getattr(ofx.account, item)))
        except AttributeError:
            pass
    for item in ('start_date', 'end_date', 'balance', 'available_balance'):
        try:
            print("{}: {}".format(item, getattr(ofx.account.statement, item)))
        except AttributeError:
            pass
    print()
    # print headers
    counter = 0
    for f in fields:
        s = "" if counter == 0 else " "
        counter += 1
        prepared = "{}{{:^{}s}} |".format(s, f['length'])
        print(prepared.format(f['name'].upper()), end='')
    print()

    # print data
    for t in ofx.account.statement.transactions:
        for f in fields:
            val = getattr(t, f['name'])
            if f['convert']:
                val = str(val)
            print(f['format'].format(val), end='')
        print()



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--debug", "-d",
        action='store_true',
        help="Debug mode (very verbose)",
        )
    parser.add_argument("-f",
        dest="ofx_file",
        help="the ofx file",
        type=argparse.FileType('rb'),
        )
    parser.add_argument("action",
        choices=['totext', 'gui', 'tocsv',]
        )

    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logging.debug('DEBUG MODE')
    ofx = OfxParser.parse(args.ofx_file)
    # print a few lines to clear the air (https://github.com/jseutter/ofxparse/issues/86)
    print("\n\n\n\n")
    locals()[args.action](ofx)


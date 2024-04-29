import argparse

from beancount import loader
from beancount.parser import parser, printer
from beancount.core import display_context
from modules.imports.alipay import Alipay
from modules.imports.wechat import WeChat
from modules.imports.abc_debit import ABCDebit
from decimal import Decimal

parser = argparse.ArgumentParser("import")
parser.add_argument("--path", help="CSV Path")
parser.add_argument(
    "--entry", help="Entry bean path (default = main.bean)", default='main.bean')
parser.add_argument("--out", help="Output bean path", default='out.bean')
args = parser.parse_args()

entries, errors, option_map = loader.load_file(args.entry)

importers = [Alipay, WeChat, ABCDebit]
instance = None
for importer in importers:
    try:
        with open(args.path, 'rb') as f:
            file_bytes = f.read()
            instance = importer(args.path, file_bytes, entries, option_map)
        break
    except Exception as e:
        print(e)
        pass

if instance == None:
    print("No suitable importer!")
    exit(1)

new_entries = instance.parse()

with open(args.out, 'w', encoding='utf-8') as f:
    dcontext = display_context.DisplayContext()
    dcontext.update(Decimal('0.01'))
    printer.print_entries(new_entries, dcontext=dcontext, file=f)

print('Outputed to ' + args.out)
exit(0)

import argparse

from beancount import loader
from beancount.parser import parser, printer
from beancount.core import display_context, data
from decimal import Decimal
import codecs
import sys

def print_entries(entries, dcontext=None, render_weights=False, file=None, prefix=None):
    """A convenience function that prints a list of entries to a file.

    Args:
      entries: A list of directives.
      dcontext: An instance of DisplayContext used to format the numbers.
      render_weights: A boolean, true to render the weights for debugging.
      file: An optional file object to write the entries to.
    """
    assert isinstance(entries, list), "Entries is not a list: {}".format(entries)
    output = file or (codecs.getwriter("utf-8")(sys.stdout.buffer)
                      if hasattr(sys.stdout, 'buffer') else
                      sys.stdout)

    if prefix:
        output.write(prefix)
    previous_type = type(entries[0]) if entries else None
    eprinter = printer.EntryPrinter(dcontext, render_weights, None, '    ')
    for entry in entries:
        # Insert a newline between transactions and between blocks of directives
        # of the same type.
        entry_type = type(entry)
        if (entry_type in (data.Transaction, data.Commodity) or
            entry_type is not previous_type):
            output.write('\n')
            previous_type = entry_type

        string = eprinter(entry)
        output.write(string)

parser = argparse.ArgumentParser("sorter")
parser.add_argument(
    "--entry", help="Entry bean path (default = main.bean)", default='main.bean')
parser.add_argument("--out", help="Output bean path", default='out.bean')
args = parser.parse_args()

entries, errors, option_map = loader.load_file(args.entry)

new_entries = entries

with open(args.out, 'w', encoding='utf-8') as f:
    dcontext = display_context.DisplayContext()
    dcontext.update(Decimal('0.01'))
    print_entries(new_entries, dcontext=dcontext, file=f)

print('Outputed to ' + args.out)
exit(0)


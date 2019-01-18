"""
Usage:
  prox <command> [<args>...]

Run 'prox COMMAND --help' for more information on a command.
"""

from inspect import getmembers, isclass
from docopt import docopt, DocoptExit
from prox import __version__ as VERSION


def main():
    """Main CLI entrypoint."""
    import prox.clis
    options = docopt(__doc__, version=VERSION, options_first=True)
    command_name = ""
    args = ""
    command_class =""

    command_name = options.pop('<command>')
    args = options.pop('<args>')

    if args is None:
        args = {}

    try:
        module = getattr(prox.clis, command_name)
    
        prox.clis = getmembers(module, isclass)
        command_class = [command[1] for command in prox.clis
                   if command[0] != 'Base'][0]
    except AttributeError as e:
        print(e)
        raise DocoptExit()

    command = command_class(options, args)
    command.execute()


if __name__ == '__main__':
    main()

import argparse


def prnt():
    print('Ololo')
def main():
    parser = argparse.ArgumentParser(prog='PROG')
    parser.add_argument('--foo', action='store_true', help='foo help')
    subparsers = parser.add_subparsers(help='sub-command help')

    parser_a = subparsers.add_parser('a', help='a help')
    parser_a.add_argument('bar', type=int, help='bar help')


if __name__ == '__main__':
    main()
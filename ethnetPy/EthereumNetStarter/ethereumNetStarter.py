# eth nodes configurator

# from web3.auto import w3
#from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider
import web3
import argparse
import glob
import subprocess


def printcol(str):
    print('\x1b[6;30;42m' + str + '\x1b[0m')


genesis = '''
{
    "nonce": "0x0000000000000042",
    "timestamp": "0x0",
    "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "extraData": "0x00",
    "gasLimit": "0x8000000",
    "difficulty": "0x400",
    "mixhash": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "coinbase": "0x3333333333333333333333333333333333333333",
    "alloc": {
    },
    "config": { }
}
'''

config = '''
{
  "nodes": [
    {
      "id": 1,
      "port": 8584,
      "peersIDs": [1,2,3]
    },
    {
      "id": 2,
      "port": 8585,
      "peersIDs": [1]
    },
    {
      "id": 3,
      "port": 8586,
      "peersIDs": [1]
    }
  ],
  "genesis": {
    "difficulty": "0x400",
    "gasLimit": "0x8000000"
  }
}
'''


def start(args):
    """Эта функция будет вызвана для старта ноды """
    printcol("Starting node {}".format(args.name))
    printcol("Starting Done")


def stop(args):
    """Эта функция будет вызвана для остановки ноды """
    printcol("Stopping node {}".format(args.arg))
    printcol("Stopping Done")


def parse_args():
    parser = argparse.ArgumentParser(description=
                                     "eth nodes configurator"
                                     "use web3 stable"
                                     )
    subparsers = parser.add_subparsers()

    # parser.add_argument("bundle", action='store', help="app bundle id")
    # parser.add_argument("source", action="store", help="app files source path")
    # parser.add_argument("config", action="store", help="uploadin files config path")
    # parser.add_argument("-v", "--verbose", action="store_true", help="increase output verbosity")

    parser_start = subparsers.add_parser('start', help='Start eth node')
    parser_start.add_argument('-n', '--name', action='store', default='ethNode0', help='Node name')
    parser_start.add_argument('-d', '--diff', default='0x400', help='Difficulty of mining')
    parser_start.add_argument('-g', '--gasLimit', default='0x8000000', help='GasLimit')
    parser_start.add_argument('-p', '--port', default='8545', help='Node port')
    parser_start.add_argument('-c', '--passcode', default='123', help='Miner account passcode')
    parser_start.set_defaults(func=start)
    # parser_start.set_defaults(func=start, name='ethNode0', diff='0x400', gasLimit='0x8000000', port='8545', passcode='123')

    parser_stop = subparsers.add_parser('stop', help='Stop eth node')
    parser_stop.add_argument('-a', '--arg', default='defArgValue', help='Stop arg value')
    parser_stop.set_defaults(func=stop)

    args = parser.parse_args()
    return args


# configs = [line.rstrip('\n') for line in open(args.config)]
# configs = [x for x in configs if not x.startswith('#')]

printcol("Configs:")


# [print(config) for config in configs]

def main():
    """Это все, что нам потребуется для обработки всех ветвей аргументов"""
    args = parse_args()
    try:
        print("args:", args)
        args.func(args)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()






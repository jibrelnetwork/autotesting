# eth nodes configurator

# from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider
import argparse
import subprocess
import os
import json
import shutil
import socket
import time

localhost = "127.0.0.1"

config = '''
{
  "nodes": [
    {
      "id": 1
    },
    {
      "id": 2
    },
    {
      "id": 3
    }
  ],
  "genesis": 
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
}
'''

def printcol(str):
    print('\x1b[6;30;42m' + str + '\x1b[0m')

def cmd(cmd_str):
    return subprocess.Popen(cmd_str.split(' '), stdout=subprocess.PIPE).communicate()[0]

def isOpen(ip,port):
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
      s.connect((ip, int(port)))
      s.shutdown(2)
      return True
   except:
      return False

def unopened_ports_scan(ip, starting_port, count):
    unopened_ports = []
    while len(unopened_ports) < count:
        if not isOpen(ip, starting_port):
            unopened_ports.append(starting_port)
        starting_port += 1
    return unopened_ports

def getpid(process_name):
    return [item.split()[1] for item in os.popen('ps -ef | grep geth').read().splitlines()[1:] if process_name in item.split()]


def start(args):
    config = json.loads(args.config)
    nodes_data = config['nodes']

    for i in range(len(nodes_data)):

        printcol("Init node {}".format(i))
        print(json.dumps(args.config))

        node_port = unopened_ports_scan(localhost, 30301, 1)[0]
        rpc_ip = localhost
        rpc_port = unopened_ports_scan(localhost, 8545, 1)[0]

        nodes_data[i]["rpc_ip"] = rpc_ip
        nodes_data[i]["rpc_port"] = rpc_port
        nodes_data[i]["node_port"] = node_port

        node_id = rpc_port
        node_name = "node_{}".format(node_id)

        node_path = "nodes/{}/".format(node_name)
        if os.path.exists(node_path):
            shutil.rmtree(node_path, ignore_errors=True)
        os.makedirs(node_path)

        genesis_path = "{}{}".format(node_path, "genesis.json")

        file = open(genesis_path, 'w')
        file.write(json.dumps(config['genesis']))
        file.close()

        cmd("geth --datadir {} init {}".format(node_path, genesis_path))

        printcol("Starting eth node {}".format(i))
        start_cmd = "geth --datadir {} --port {} --rpc --rpcport {} --rpcaddr {} --rpcapi=\'db,eth,net,web3,personal\'".format(node_path, node_port, rpc_port, rpc_ip)
        geth_process = subprocess.Popen(start_cmd.split(' ')) #, stdout=subprocess.PIPE)

        nodes_data[i]["node_pid"] = geth_process.pid
        time.sleep(5)

        printcol("Starting eth node {} done".format(i))
        print("Use: web3 = Web3(Web3.HTTPProvider(\"http://{}:{}\"))".format(rpc_ip, rpc_port))

    printcol("Started {} eth nodes".format(len(nodes_data)))
    print(json.dumps(nodes_data).replace("\"","\\\""))
    return nodes_data


def stop(args):
    printcol("Stopping nodes")
    nodes = json.loads(args.nodes)
    for node in nodes:
        cmd("kill {}".format(node["node_pid"]))
    printcol("Stopping nodes Done")

def stop_all(args):
    printcol("Stopping all geth nodes")
    pids = getpid("geth")
    for pid in pids:
        cmd("kill {}".format(pid))
    printcol("Stopping nodes Done")


def parse_args():
    parser = argparse.ArgumentParser(description=
                                     "eth nodes configurator"
                                     "use web3 stable"
                                     )
    subparsers = parser.add_subparsers()
    parser_start = subparsers.add_parser('start', help='Start eth node')
    parser_start.add_argument('-c', '--config', action='store', default=config, help='Node configuration json string')
    parser_start.add_argument('-p', '--port', default='30301', help='Node port')
    parser_start.add_argument('-i', '--rpc_ip', default='127.0.0.1', help='Node rpc ip address')
    parser_start.add_argument('-r', '--rpc_port', default='8545', help='RPC node port')
    # parser_start.add_argument('-c', '--passcode', default='123', help='Miner account passcode')
    parser_start.set_defaults(func=start)

    parser_stop = subparsers.add_parser('stop', help='Stop eth node')
    parser_stop.add_argument('-n', '--nodes', default='[{}]', help='Nodes to stop json string')
    parser_stop.set_defaults(func=stop)

    parser_stop_all = subparsers.add_parser('stopall', help='Stop all eth node')
    parser_stop_all.set_defaults(func=stop_all)

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    try:
        # print("args:", args)
        args.func(args)



    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()

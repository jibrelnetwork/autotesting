# eth nodes starter
# starts geth nodes by configuration

import argparse
import subprocess
import os
import json
import shutil
import socket
import time

def printcol(str):
    print('\x1b[6;30;42m' + str + '\x1b[0m')

def printerr(str):
    print('\x1b[6;30;31m' + str + '\x1b[0m')

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
    return [item.split()[0] for item in os.popen('ps -A | grep geth').read().splitlines()[0:] if process_name in item.split()]


def start(args):

    config = None
    if args.config:
        printcol("Using --config")
        config = json.loads(args.config)
    else:
        if args.config_path:
            printcol("Using --config_path {}".format(args.config_path))
            config_path = args.config_path
            if os.path.exists(config_path):
                with open(config_path, 'r') as file:
                    data = file.read().replace('\n', ' ')
                    file.close()
                config = json.loads(data)
            else:
                printerr("Wrong config_path:{}".format(config_path))
                exit(1)
        else:
            printerr("Need provide at least one of params: --config, --config_path")
            exit(2)

    nodes_data = config['nodes']

    for i in range(len(nodes_data)):

        printcol("Init node {}".format(i))
        print(json.dumps(args.config))

        rpc_ip = args.rpc_ip
        node_port = unopened_ports_scan(rpc_ip, args.port, 1)[0]
        rpc_port = unopened_ports_scan(rpc_ip, args.rpc_port, 1)[0]
        rpc_api = nodes_data[i]["rpc_api"]

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
        start_cmd = "geth --datadir {} --port {} --rpc --rpcport {} --rpcaddr {} --rpcapi=\'{}\'".format(node_path, node_port, rpc_port, rpc_ip, rpc_api)
        geth_process = subprocess.Popen(start_cmd.split(' '))

        nodes_data[i]["node_pid"] = geth_process.pid
        time.sleep(5)

        printcol("Starting eth node {} done".format(i))
        print("Use: web3 = Web3(Web3.HTTPProvider(\"http://{}:{}\"))".format(rpc_ip, rpc_port))

    printcol("Geth nodes addresses:")
    print(json.dumps(nodes_data).replace("\"", "\\\""))

    printcol("Started {} geth nodes DONE".format(len(nodes_data)))

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

def help(args):
    printerr("Use -h")


def parse_args():
    parser = argparse.ArgumentParser(description=
                                     "eth nodes configurator"
                                     "use web3 stable"
                                     )
    subparsers = parser.add_subparsers()
    parser_start = subparsers.add_parser('start', help='Start eth node')
    parser_start.add_argument('-c', '--config', action='store', help='Node configuration json string')
    parser_start.add_argument('-f', '--config_path', default='./genesis.json', action='store', help='Node configuration json file path')
    parser_start.add_argument('-p', '--port', default=30301, help='Node port')
    parser_start.add_argument('-i', '--rpc_ip', default='127.0.0.1', help='Node rpc ip address')
    parser_start.add_argument('-r', '--rpc_port', default=8545, help='RPC node port')
    parser_start.set_defaults(func=start)

    parser_stop = subparsers.add_parser('stop', help='Stop eth nodes')
    parser_stop.add_argument('-n', '--nodes', default='[{}]', help='Nodes to stop json string')
    parser_stop.set_defaults(func=stop)

    parser_stop_all = subparsers.add_parser('stopall', help='Stop all eth nodes')
    parser_stop_all.set_defaults(func=stop_all)

    parser.set_defaults(func=help)

    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    try:
        args.func(args)

    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
import sys
sys.path.append('/usr/local/lib/python3.6/site-packages')

from multiprocessing import Process, Manager
from collections import namedtuple
from flask import Flask
from flask import request
from flask import Response
import ethnetstarter
import subprocess
import json
import time

app = Flask(__name__)

manager = Manager()
tasks = manager.dict()

def cmd(cmd_str):
    return subprocess.Popen(cmd_str.split(' '), stdout=subprocess.PIPE).communicate()[0]

def stating_eth_net_task(task_id, l):
    print("started:{}".format(task_id))
    task = tasks[task_id]
    task["status"] = "in progress"
    tasks[task_id] = task

    # res = ethnetstarter.main(["start"])
    config = task["config"]
    params = ["start", "-c", "{}".format(json.dumps(config))]
    args = ethnetstarter.parse_args(params)
    res = None
    try:
        res = args.func(args)
    except Exception as e:
        print(e)

    task = tasks[task_id]
    task["res"] = res
    task["status"] = "done"
    tasks[task_id] = task
    print("done:{}".format(task_id))

def stop_eth_net_task(nodes, l):
    print("Nodes to stop:{}".format(nodes))
    args = ["stop", "-n", "{}".format(json.dumps(nodes))]
    args = ethnetstarter.parse_args(args)
    try:
        args.func(args)
    except Exception as e:
        print(e)
    print("done")

def stop_all(a, b):
    ethnetstarter.stop_all({})

@app.route('/')
def index():
    return "Ethereum net starter"


@app.route('/start', methods=['POST'])
def post_start():
    task_id = str(time.time()).replace('.', '')
    content = request.get_json()
    content["task_id"] = task_id
    tasks[task_id] = {"status": "posted", "config": content}
    p = Process(target=stating_eth_net_task, args=(task_id, ""))
    p.start()
    ret = json.dumps({"task_id":task_id})
    resp = Response(response=ret,
                    status=200,
                    mimetype="application/json")
    return resp

@app.route('/status', methods=['GET'])
def get_status():
    task_id = request.args.get("task_id")
    task = tasks.get(task_id)
    ret = json.dumps(task)
    resp = Response(response=ret,
                    status=200,
                    mimetype="application/json")
    return resp

@app.route('/stop', methods=['POST'])
def post_stop():
    content = request.get_json()
    p = Process(target=stop_eth_net_task, args=(content, ""))
    p.start()
    ret = json.dumps({"stopping nodes":content})
    resp = Response(response=ret,
                    status=200,
                    mimetype="application/json")
    return resp

@app.route('/stopall', methods=['GET'])
def get_stop_all():
    p = Process(target=stop_all, args=("", ""))
    p.start()
    return 'Start stopping all nodes'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

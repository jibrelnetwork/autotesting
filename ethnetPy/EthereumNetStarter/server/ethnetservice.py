import sys
sys.path.append('/usr/local/lib/python3.6/site-packages')

from multiprocessing import Process, Manager
from collections import namedtuple
from flask import Flask
from flask import request
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

    Args = namedtuple("Args", "config nodes")

    args = Args(config=json.dumps(task["config"]), nodes={})
    res = ethnetstarter.main(["start"]) #ethnetstarter.main("start") # start(args)

    task = tasks[task_id]
    task["res"] = res
    task["status"] = "done"
    tasks[task_id] = task
    print("done:{}".format(task_id))

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
    return json.dumps({"task_id":task_id})

@app.route('/status', methods=['GET'])
def get_status():
    task_id = request.args.get("task_id")
    task = tasks.get(task_id)
    return json.dumps(task)

@app.route('/stopall', methods=['GET'])
def get_stop_all():
    p = Process(target=stop_all, args=("", ""))
    p.start()
    return 'Start stopping all nodes'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

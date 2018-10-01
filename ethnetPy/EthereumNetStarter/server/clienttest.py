import requests
import time
import unittest
import os

config_data = {
  'nodes': [
    {
      'id': 1,
      'rpc_api':'db,eth,net,web3,personal'
    },
    {
      'id': 2,
      'rpc_api':'db,eth,net,web3,personal'
    },
    {
      'id': 3,
      'rpc_api':'db,eth,net,web3,personal'
    }
  ],
  'genesis':
    {
        'nonce': '0x0000000000000042',
        'timestamp': '0x0',
        'parentHash': '0x0000000000000000000000000000000000000000000000000000000000000000',
        'extraData': '0x00',
        'gasLimit': '0x8000000',
        'difficulty': '0x400',
        'mixhash': '0x0000000000000000000000000000000000000000000000000000000000000000',
        'coinbase': '0x3333333333333333333333333333333333333333',
        'alloc': {
        },
        'config': {}
    }
}

def getpid(process_name):
    return [item.split()[0] for item in os.popen('ps -A | grep {}'.format(process_name)).read().splitlines()[0:] if process_name in item.split()]

class TestStringMethods(unittest.TestCase):

    def test_start(self):
        r = requests.post("http://127.0.0.1:5000/start", json=config_data)

        self.assertEqual(r.status_code, 200)

        task_id = r.json().get('task_id')

        self.assertTrue(task_id)
        print("Task_id:{}".format(task_id))

        print("Task started ...")
        res = None
        times = 0
        while (not res) and (times < 20):
            r = requests.get("http://127.0.0.1:5000/status?task_id={}".format(task_id))
            res_json = r.json()
            res = res_json.get("res")
            print("Task status: {}".format(res_json.get("status")))
            time.sleep(2)
            times += 1

        print("Done")
        print("Res:{}".format(res))

        nodes_count = len(config_data['nodes'])

        self.assertIsNotNone(res)
        self.assertEqual(len(res), nodes_count)
        self.assertTrue(res[0].get('id'))
        self.assertTrue(res[0].get('rpc_api'))
        self.assertTrue(res[0].get('rpc_ip'))
        self.assertTrue(res[0].get('rpc_port'))
        self.assertTrue(res[0].get('node_port'))

        geth_pids = getpid("geth")

        for node in res:
            self.assertTrue(geth_pids.__contains__(str(node.get('node_pid'))))

        started_nodes = res

        r = requests.post("http://127.0.0.1:5000/stop", json=started_nodes)

        self.assertEqual(r.status_code, 200)

        geth_pids = getpid("geth")

        for node in started_nodes:
            self.assertFalse(geth_pids.__contains__(str(node.get('node_pid'))))

        time.sleep(1)

if __name__ == '__main__':
    unittest.main()
import requests
import time
import unittest

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

class TestStringMethods(unittest.TestCase):

    def test_start(self):
        r = requests.post("http://127.0.0.1:5000/start", json=config_data)

        self.assertEqual(r.status_code, 200)

        task_id = r.json().get('task_id')

        self.assertTrue(task_id)
        print("Task_id:{}".format(task_id))

        print("Loading...")
        res = None
        while not res:
            r = requests.get("http://127.0.0.1:5000/status?task_id={}".format(task_id))
            res_json = r.json()
            res = res_json.get("res")
            time.sleep(2)

        print("Done")
        print("Res:{}".format(res))

        nodes_count = len(config_data['nodes'])

        self.assertEqual(len(res), nodes_count)
        self.assertTrue(res[0].get('id'))
        self.assertTrue(res[0].get('rpc_ip'))
        self.assertTrue(res[0].get('rpc_port'))
        self.assertTrue(res[0].get('node_port'))

if __name__ == '__main__':
    unittest.main()
import requests

if __name__ == '__main__':
    r = requests.get('http://localhost:8080/start')
    print("res:{}".format(r))

    payload = {'key1': 'value1', 'key2': 'value2'}
    r = requests.post("http://localhost:8080/", data=payload)
    print("res:{}".format(r))

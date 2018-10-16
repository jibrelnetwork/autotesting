Using  pipenv


Add to ~/.profile

```
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
```

Install geth

```
brew install geth
```


Run server

```
pipenv run python ethnetservice.py
```

Run client tests

```
pipenv run python clienttest.py
```

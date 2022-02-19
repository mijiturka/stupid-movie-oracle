# stupid-movie-oracle
One that gives wise and authoritative decisions on which stupid movie we should watch tonight

## Deployment

Either copy a database in or create a new one:
```
$ mkdir server-side/users
$ sqlite3 server-side/users/users.db
```
The newly created database can be empty:
```
$ sqlite3 server-side/users/users.db "VACUUM;"
```

Place authentication info in `server-side/deploy/terraform.tfvars`:
```
api_token="..."
ssh_user="..."
root_user_pwd="..."
```

Provision a Linode:
```
$ cd deploy
$ terraform plan
$ terraform apply
```

Terraform will output the IP for the Linode it's just spun up. Place the IP in `inventory.ini`

Configure the Linode:
```
$ ansible-playbook debian.yaml
```

## Running tests

From within the `server-side` directory:

* `pytest`
Or to run particular tests:
* `pytest tests/test_server.py`
* `pytest tests/test_options.py::TestMain`
* `pytest tests/test_options.py::TestMain::test_dieable_ok_exact`

<!-- Or without pytest:
* `python -m unittest discover`
Or to run particular tests:
* `python -m unittest tests.test_server`
* `python -m unittest tests.test_options.TestMain`
* `python -m unittest tests.test_options.TestMain.test_dieable_ok_less_than` -->

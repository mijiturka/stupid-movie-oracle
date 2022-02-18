# stupid-movie-oracle
One that gives wise and authoritative decisions on which stupid movie we should watch tonight

## Deployment

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

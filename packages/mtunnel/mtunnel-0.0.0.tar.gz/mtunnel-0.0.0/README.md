# mtunnel

Creates multiple background SSH tunnels for services within a project and stage.

## installation

Install the package from `PyPI`:
```
pip3 install mtunnel
```

## usage

For example:

With this config in `mtunnel.yml`:

```
jumpbox:
  ssh_address: bastion.example.com
  dont_sudo: true

region: us-east-1

projects:
  project1:
    profile: default
    stages:
      staging:
        mysql:
          bind_port: 3306
          host_address: staging-rds-0.us-east-1.rds.amazonaws.com
          host_port: 3306
        es:
          bind_port: 9200
          host_address: vpc-staging-abcdefghijkl.us-east-1.es.amazonaws.com
          host_port: 443
```

when you run this command:
```
mtunnel project1 staging
```

the following SSH tunnels will be setup via `bastion.example.com`:
```
mysql: localhost:3306 -> staging-rds-0.us-east-1.rds.amazonaws.com:3306
es: localhost:9200 -> vpc-staging-rds-abcdefghijkl.us-east-1.es.amazonaws.com:443
```

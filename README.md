# Social network app

## Additional information

To create database

```
create role network with password 'network';
alter user network with superuser;
alter role 'network' with login;
create database "network" owner "network";
```

To run project

```
git clone https://github.com/pavlenk0/social-network.git
cd social-network
make install
make run
```

To test project

```
make test
```

To check the code for flake8 and isort

```
make flake
make isort
```

Project uses [hunter API](https://hunter.io/api/v2/docs) to verify emails

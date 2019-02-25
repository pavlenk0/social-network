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

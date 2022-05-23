# PyResticD

### About

PyResticD is a collection of Python scripts to run [restic](https://restic.github.io/) in a Daemon like 
fashion on servers while keeping the backup password in volatile memory only.

### Requirements

- python3
- pip3
- restic

### Installation

- Install Python requirements:

```
pip3 install schedule python-dateutil pytz
```

- Copy the configuration files:

```
cp pyresticd.cfg.exmaple pyresticd.cfg
cp excludes.txt.example excludes.txt
```

- Edit the `pyresticd.cfg` file.


### Usage

Edit the configuration file and start it in tmux or screen:

```
python3 pyresticd.py
```

### Forget & Prune

To forget and prune snapshots the `forget-and-prune.py` script can be used.

### Monitoring

The script can create a "infofile" in a web-server accessible location. Later the `./monitor/monitor.py` script can be used to check if the backups on various servers ran successfully.

### Authors

- Mebus, https://github.com/Mebus/

### License

- MIT

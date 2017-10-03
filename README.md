# PyResticD

### About

PyResticD is a inofficial collection of Python scripts to run [restic](https://restic.github.io/) in a Daemon like fashion on servers while keeping the backup password in volatile memory only.

### Requirements

python3, pip3

### Installation

Install Python requirements:

```
pip3 install schedule python-dateutil pytz
```

Copy config file:

```
cp pyresticd.conf.exmaple pyresticd.conf
cp excludes.txt.example excludes.txt
```
### Usage

Edit the configuration file and start it in tmux or screen!

### Author

Mebus, 
https://github.com/Mebus/

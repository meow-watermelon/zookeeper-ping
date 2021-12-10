# Zookeeper Ping

## Intro

This is a small utility to test Zookeeper service by using `ruok` command and issuing a series of CRUD operations to show the running latency metrics.

## Python Module Dependencies

Following Python modules are needed to run this utility:

```
argparse
kazoo
random
signal
string
sys
time
```

## Usage

```
$ ./zkping.py -h
usage: zkping.py [-h] --quorum QUORUM [--timeout TIMEOUT] [--count COUNT] [--znoderoot ZNODEROOT]

Zookeeper Ping

optional arguments:
  -h, --help            show this help message and exit
  --quorum QUORUM       Zookeeper quorum string (example: zkp1:2181,zkp2:2181,zkp3:2181)
  --timeout TIMEOUT     Zookeeper client timeout value (default: 30 seconds)
  --count COUNT         Stop after sending count requests
  --znoderoot ZNODEROOT
                        Parent of testing znode (default: /)
```

## Example

```
$ ./zkping.py --quorum '127.0.0.1:2181' --count 5 --znoderoot '/abc'
RUOK PING - sequence_id: 1 - error: NaN - ruok_time: 3.18 ms
CRUD PING - sequence_id: 1 - znode_name: /abc/zkping-05RA8PSO95GI9MVB - create_error: NaN - create_time: 3.28 ms - read_error: NaN - read_time: 1.67 ms - update_error: NaN - update_time: 1.88 ms - delete_error: NaN - delete_time: 1.50 ms
RUOK PING - sequence_id: 2 - error: NaN - ruok_time: 6.05 ms
CRUD PING - sequence_id: 2 - znode_name: /abc/zkping-Z6DYLSVF8EMH9CWF - create_error: NaN - create_time: 10.90 ms - read_error: NaN - read_time: 5.75 ms - update_error: NaN - update_time: 7.90 ms - delete_error: NaN - delete_time: 6.16 ms
RUOK PING - sequence_id: 3 - error: NaN - ruok_time: 6.14 ms
CRUD PING - sequence_id: 3 - znode_name: /abc/zkping-4X8G8IF0RH8VLC05 - create_error: NaN - create_time: 10.69 ms - read_error: NaN - read_time: 5.86 ms - update_error: NaN - update_time: 6.56 ms - delete_error: NaN - delete_time: 6.23 ms
RUOK PING - sequence_id: 4 - error: NaN - ruok_time: 6.18 ms
CRUD PING - sequence_id: 4 - znode_name: /abc/zkping-LVLGPCB4JCYNAXC8 - create_error: NaN - create_time: 10.86 ms - read_error: NaN - read_time: 5.83 ms - update_error: NaN - update_time: 6.49 ms - delete_error: NaN - delete_time: 5.98 ms
RUOK PING - sequence_id: 5 - error: NaN - ruok_time: 6.02 ms
CRUD PING - sequence_id: 5 - znode_name: /abc/zkping-MR5QHM12HLN2R2FC - create_error: NaN - create_time: 10.41 ms - read_error: NaN - read_time: 5.33 ms - update_error: NaN - update_time: 6.59 ms - delete_error: NaN - delete_time: 6.35 ms
```

## Known Issues

1. [kazoo](https://kazoo.readthedocs.io/en/latest/index.html) module has internal retry mechanism if the Zookeeper client encounters exceptions. As a service ping-pong utility, there's no need to issue retry calls. I will remove retry calls from the Zookeeper client to make sure the utility fails quickly.

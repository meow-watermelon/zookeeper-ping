#!/usr/bin/env python3

import argparse
from kazoo.client import KazooClient
import random
import signal
import socket
import string
import sys
import time

def signal_handler(signal_number, frame):
    sys.exit(0)

def zk_4w_ruok(client):
    # (command_result_flag, information)
    # command_result_flag = True or False or None
    # information = command running time or error message
    output = (None, None)

    # start time timestamp
    start_time = time.time()

    # start zookeeper client
    try:
        client.start()
    except Exception as e:
        output = (False, e)
    else:
        # send ruok 4w command
        try:
            zk_4w_result = client.command(b'ruok')
        except Exception as e:
            output = (None, e)
        else:
            if zk_4w_result == 'imok':
                output = (True, time.time() - start_time)
            else:
                output = (False, time.time() - start_time)

            # stop zookeeper client
            client.stop()

    return output

def zk_crud(client, *, znode_root='/'):
    random_znode_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))

    if znode_root == '/':
        znode_name = znode_root + 'zkping-' + random_znode_string
    else:
        znode_name = znode_root + '/zkping-' + random_znode_string

    output = {}
    output['znode_name'] = znode_name

    # create
    start_time = time.time()

    try:
        client.start()
    except Exception as e:
        output['create_flag'] = False
        output['create_info'] = e
    else:
        try:
            client.ensure_path(znode_name)
        except Exception as e:
            output['create_flag'] = False
            output['create_info'] = e
        else:
            output['create_flag'] = True
            output['create_info'] = time.time() - start_time

        client.stop()
        
    # read
    start_time = time.time()

    try:
        client.start()
    except Exception as e:
        output['read_flag'] = False
        output['read_info'] = e
    else:
        try:
            client.get(znode_name)
        except Exception as e:
            output['read_flag'] = False
            output['read_info'] = e
        else:
            output['read_flag'] = True
            output['read_info'] = time.time() - start_time

        client.stop()

    # update
    start_time = time.time()

    try:
        client.start()
    except Exception as e:
        output['update_flag'] = False
        output['update_info'] = e
    else:
        try:
            client.set(znode_name, b'0123456789')
        except Exception as e:
            output['update_flag'] = False
            output['update_info'] = e
        else:
            output['update_flag'] = True
            output['update_info'] = time.time() - start_time

        client.stop()

    # delete
    start_time = time.time()

    try:
        client.start()
    except Exception as e:
        output['delete_flag'] = False
        output['delete_info'] = e
    else:
        try:
            client.delete(znode_name)
        except Exception as e:
            output['delete_flag'] = False
            output['delete_info'] = e
        else:
            output['delete_flag'] = True
            output['delete_info'] = time.time() - start_time

        client.stop()

    return output

if __name__ == '__main__':
    # set up command arguments
    parser = argparse.ArgumentParser(description='Zookeeper Ping')
    parser.add_argument('--quorum', type=str, required=True, help='Zookeeper quorum string (example: zkp1:2181,zkp2:2181,zkp3:2181)')
    parser.add_argument('--timeout', type=int, required=False, default=30, help='Zookeeper client timeout value (default: 30 seconds)')
    parser.add_argument('--count', type=int, required=False, help='Stop after sending count requests')
    parser.add_argument('--znoderoot', type=str, required=False, default='/', help='Stop after sending count requests (default: /)')
    args = parser.parse_args()

    # register the signal handler
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # initiate zookeeper client
    try:
        zk_client = KazooClient(hosts=args.quorum, timeout=args.timeout, connection_retry=None, command_retry=None)
    except Exception as e:
        print('ERROR: Failed to initialize Zookeeper client: %s' %(e))
        sys.exit(2)
    else:
        seq_count = 0
        counter = 0

        while True:
            if args.count:
                counter += 1

                if counter > args.count:
                    break

            results = {}
            seq_count += 1

            # process 4w result
            zk_4w_result = zk_4w_ruok(zk_client)

            if zk_4w_result[0] == True:
                results['zk_4w_time'] = zk_4w_result[1]
                results['zk_4w_error'] = 'NaN'

            if zk_4w_result[0] == None:
                results['zk_4w_time'] = zk_4w_result[1]
                results['zk_4w_error'] = 'NO_IMOK_RESPONSE'

            if zk_4w_result[0] == False:
                results['zk_4w_time'] = 0.0
                results['zk_4w_error'] = zk_4w_result[1]

            # process crud result
            zk_curd_result = zk_crud(zk_client, znode_root=args.znoderoot)

            if zk_curd_result['create_flag']:
                results['zk_create_time'] = zk_curd_result['create_info']
                results['zk_create_error'] = 'NaN'
            else:
                results['zk_create_time'] = 0.0
                results['zk_create_error'] = zk_curd_result['create_info']

            if zk_curd_result['read_flag']:
                results['zk_read_time'] = zk_curd_result['read_info']
                results['zk_read_error'] = 'NaN'
            else:
                results['zk_read_time'] = 0.0
                results['zk_read_error'] = zk_curd_result['read_info']

            if zk_curd_result['update_flag']:
                results['zk_update_time'] = zk_curd_result['update_info']
                results['zk_update_error'] = 'NaN'
            else:
                results['zk_update_time'] = 0.0
                results['zk_update_error'] = zk_curd_result['update_info']

            if zk_curd_result['delete_flag']:
                results['zk_delete_time'] = zk_curd_result['delete_info']
                results['zk_delete_error'] = 'NaN'
            else:
                results['zk_delete_time'] = 0.0
                results['zk_delete_error'] = zk_curd_result['delete_info']

            # final output
            print('RUOK PING - sequence_id: %d - error: %s - ruok_time: %.2f ms' %(seq_count, results['zk_4w_error'], results['zk_4w_time'] * 1000))
            print('CRUD PING - sequence_id: %d - znode_name: %s - create_error: %s - create_time: %.2f ms - read_error: %s - read_time: %.2f ms - update_error: %s - update_time: %.2f ms - delete_error: %s - delete_time: %.2f ms' %(seq_count, zk_curd_result['znode_name'], results['zk_create_error'], results['zk_create_time'] * 1000, results['zk_read_error'], results['zk_read_time'] * 1000, results['zk_update_error'], results['zk_update_time'] * 1000, results['zk_delete_error'], results['zk_delete_time'] * 1000))

            # sleep 1 second for each loop
            time.sleep(1)

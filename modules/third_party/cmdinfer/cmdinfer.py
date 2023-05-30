#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import glob

import zmq
from zmq import EAGAIN, ETERM

def fetch_stats(line: str)->dict:
    line = line.strip()
    try:
        stats = json.loads(line)
        return stats
    except json.decoder.JSONDecodeError:
        return None


def request_estimated_bandwidth(line: str)->bool:
    line = line.strip()
    if RequestBandwidthCommand == line:
        return True
    return False


# get the estimator class
# Currently searches local dir only
def find_estimator_class():
    import BandwidthEstimator
    return BandwidthEstimator.Estimator

def main():

    # load estimator
    estimator_class = find_estimator_class()
    estimator = estimator_class()

    # establish zmq context
    context = zmq.Context()

    # establish socket
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    ## loop to keep running
    while True:

        # try to connect to a socket
        # if it works, return socket
        # if not, gracefully close


        try:
            # send a request to the socket
            print("\nPreparing to send request\n")
            socket.send(b"Hello") # TMP flag for "send more data"
            print("Request sent\n")
            line = socket.recv(flags=zmq.NOBLOCK)
        # TODO: review built-in zmq exception handler
        except(Exception) as e:
            print("No message available") # TEMP
            # No response; close socket/clean buffer and repeat
        else:
            print("message returned")
            print(line)

        print("After the socket run")

    #    # if isinstance(line, bytes):
    #    #     line = line.decode("utf-8")
    #    # stats = fetch_stats(line)
    #    # if stats:
    #    #     estimator.report_states(stats)
    #    #     continue
    #    # request = request_estimated_bandwidth(line)
    #    # if request:
    #    #     bandwidth = estimator.get_estimated_bandwidth()
    #    #     ofd.write("{}\n".format(int(bandwidth)).encode("utf-8"))
    #    #     ofd.flush()
    #    #     continue
    #    # sys.stdout.write(line)
    #    # sys.stdout.flush()


if __name__ == '__main__':
    main()

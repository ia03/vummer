#!/usr/bin/env python
import lxc
import sys
from threading import Timer

CONTAINER_NAME = 'apicontainer'
OUTPUT_FILE = 'user_code.out'
ERROR_FILE = 'user_code.error'

def sandbox_python(code):
    def user_code():
        exec(code)

    # Setup the container object
    c = lxc.Container(CONTAINER_NAME)
    if not c.defined:
        prepare_lxc()
        c = lxc.Container(CONTAINER_NAME)

    # Query some information
    print("Container state: %s" % c.state)
    print("Container PID: %s" % c.init_pid)
    c.set_config_item('lxc.prlimit.cpu', '1')

    timer = Timer(1, stop_and_destroy)
    timer.start()

    with open(OUTPUT_FILE, 'w') as output_file, open(ERROR_FILE, 'w') as error_file:
        c.attach_wait(user_code, stdout=output_file, stderr=error_file)

    stop_and_destroy()

    with open(OUTPUT_FILE, 'r') as output_file, open(ERROR_FILE, 'r') as error_file:
        results = {'output': output_file.read(), 'errors': error_file.read()}
    return results

def prepare_lxc():
    stop_and_destroy()

    c = lxc.Container(CONTAINER_NAME)

    # Create the container rootfs
    if not c.create("download", lxc.LXC_CREATE_QUIET, {"dist": "alpine",
                                                       "release": "3.10",
                                                       "arch": "amd64"}):
        print("Failed to create the container rootfs", file=sys.stderr)
        return

    # Start the container
    if not c.start():
        print("Failed to start the container", file=sys.stderr)
        return
    c.set_config_item('lxc.ephemeral', '1')
    c.set_config_item('lxc.prlimit.as', '128000000')

def stop_and_destroy():
    c = lxc.Container(CONTAINER_NAME)
    if c.defined:
        # Stop the container
        if not c.stop():
            print("Failed to kill the container", file=sys.stderr)
            return

        # Destroy the container
        if not c.destroy():
            print("Failed to destroy the container.", file=sys.stderr)
            return

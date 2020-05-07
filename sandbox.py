#!/usr/bin/env python
import lxc
import sys

CONTAINER_NAME = 'apicontainer'
OUTPUT_FILE = 'user_code.out'
ERROR_FILE = 'user_code.error'

def sandbox_python(code):
    def user_code():
        exec(code)

    # Setup the container object
    c = lxc.Container(CONTAINER_NAME)
    if not c.defined:
        if not c.create("download", lxc.LXC_CREATE_QUIET, {"dist": "ubuntu",
                                                           "release": "trusty",
                                                           "arch": "amd64"}):
            print("Failed to create the container rootfs", file=sys.stderr)
            return
        # Start the container
        if not c.start():
            print("Failed to start the container", file=sys.stderr)
            return

    # Query some information
    print("Container state: %s" % c.state)
    print("Container PID: %s" % c.init_pid)
    with open(OUTPUT_FILE, 'w') as output_file, open(ERROR_FILE, 'w') as error_file:
        c.attach_wait(user_code, stdout=output_file, stderr=error_file)

    # Stop the container
    if not c.stop():
        print("Failed to kill the container", file=sys.stderr)
        return

    # Destroy the container
    if not c.destroy():
        print("Failed to destroy the container.", file=sys.stderr)
        return


    with open(OUTPUT_FILE, 'r') as output_file, open(ERROR_FILE, 'r') as error_file:
        results = {'output': output_file.read(), 'errors': error_file.read()}
    return results

def prepare_lxc():
    # Create a new container
    c = lxc.Container(CONTAINER_NAME)

    # Create the container rootfs
    if not c.create("download", lxc.LXC_CREATE_QUIET, {"dist": "ubuntu",
                                                       "release": "trusty",
                                                       "arch": "amd64"}):
        print("Failed to create the container rootfs", file=sys.stderr)
        return

    # Start the container
    if not c.start():
        print("Failed to start the container", file=sys.stderr)
        return

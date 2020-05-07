#!/usr/bin/env python
import lxc
import sys

CONTAINER_NAME = 'apicontainer'
OUTPUT_FILE = 'user_code.out'

def sandbox_python(code):
    def user_code():
        exec(code)

    # Setup the container object
    c = lxc.Container(CONTAINER_NAME)
    if c.defined:
        print("Container already exists", file=sys.stderr)
        if not c.stop():
            print("Failed to kill the container", file=sys.stderr)
        if not c.destroy():
            print("Failed to destroy the container.", file=sys.stderr)
        c = lxc.Container(CONTAINER_NAME)

    # Create the container rootfs
    if not c.create("download", lxc.LXC_CREATE_QUIET, {"dist": "ubuntu",
                                                       "release": "trusty",
                                                       "arch": "amd64"}):
        print("Failed to create the container rootfs", file=sys.stderr)
        return 'Internal error'

    # Start the container
    if not c.start():
        print("Failed to start the container", file=sys.stderr)
        return 'Internal error'

    # Query some information
    print("Container state: %s" % c.state)
    print("Container PID: %s" % c.init_pid)
    with open(OUTPUT_FILE, 'w') as output_file:
        c.attach_wait(user_code, stdout=output_file)

    # Stop the container
    if not c.stop():
        print("Failed to kill the container", file=sys.stderr)
        return 'Internal error'

    # Destroy the container
    if not c.destroy():
        print("Failed to destroy the container.", file=sys.stderr)
        return 'Internal error'
    with open(OUTPUT_FILE, 'r') as output_file:
        return output_file.read()

#!/usr/bin/env python
import lxc
import sys
import os
from time_limit import time_limit, TimeoutException

base = lxc.Container('base')

def sandbox_python(code, container_name, input_data):
    output_filename = get_output_filename(container_name)
    error_filename = get_error_filename(container_name)
    input_filename = get_input_filename(container_name)
    def user_code():
        exec(code)

    # Setup the container object
    prepare_lxc(container_name)
    c = lxc.Container(container_name)
    print_state(container_name)

    with open(input_filename, 'w') as input_file:
        input_file.write(input_data)
        print('Wrote input:', input_data)
    with open(input_filename) as input_file:
        print('file has:', input_file.read())

    # Run the code in the container
    try:
        with time_limit(2):
            with open(output_filename, 'w') as output_file, \
                open(error_filename, 'w') as error_file, \
                open(input_filename, 'r+') as input_file:
                c.attach_wait(lxc.attach_run_command, ['python3', '-c', code],
                    stdout=output_file, stderr=error_file, stdin=input_file)
    except TimeoutException as e:
        return {'output': '', 'errors': 'Program timed out.'}

    # Ignore first 5 lines of errors
    with open(error_filename, 'r') as error_file:
        data = error_file.read().splitlines(True)
    with open(error_filename, 'w') as error_file:
        error_file.writelines(data[5:])

    with open(output_filename, 'r') as output_file, open(error_filename, 'r') as error_file:
        results = {'output': output_file.read(), 'errors': error_file.read()}
    return results

def prepare_lxc(container_name):
    base.clone(container_name, bdevtype="overlayfs",
        flags=lxc.LXC_CLONE_SNAPSHOT)
    c = lxc.Container(container_name)

    # Start the container
    if not c.start():
        print("Failed to start the container", file=sys.stderr)
        return

def stop_and_destroy(container_name):
    c = lxc.Container(container_name)

    if c.defined:
        # Stop the container
        if not c.stop():
            print("Failed to kill the container", file=sys.stderr)
            return

        # Destroy the container
        if not c.destroy():
            print("Failed to destroy the container.", file=sys.stderr)
            return
    os.remove(get_output_filename(container_name))
    os.remove(get_error_filename(container_name))
    os.remove(get_input_filename(container_name))

def setup_base():
    # Create the container rootfs
    if not base.defined:
        if not base.create("download", lxc.LXC_CREATE_QUIET, {"dist": "ubuntu",
                                                           "release": "trusty",
                                                           "arch": "amd64"}):
            print("Failed to create the container rootfs", file=sys.stderr)
            return


    base.set_config_item('lxc.ephemeral', '1')
    base.set_config_item('lxc.prlimit.as', '128000000')


def print_state(container_name):
    c = lxc.Container(container_name)
    # Query some information
    print("Container state: %s" % c.state)
    print("Container PID: %s" % c.init_pid)

def get_output_filename(container_name):
    return 'io/' + container_name + '.out'

def get_error_filename(container_name):
    return 'io/' + container_name + '.error'

def get_input_filename(container_name):
    return 'io/' + container_name + '.in'

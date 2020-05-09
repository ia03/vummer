import lxc
import sys
import os
from time_limit import time_limit, TimeoutException
from utils import time_limit_lxc
from threading import Thread

base = lxc.Container('base')

def sandbox_python(code, container_name, input_data):
    output_filename = get_output_filename(container_name)
    error_filename = get_error_filename(container_name)
    input_filename = get_input_filename(container_name)
    log_filename = get_log_filename(container_name)
    def user_code():
        exec(code)

    # Setup the container object
    prepare_lxc(container_name)
    c = lxc.Container(container_name)
    print_state(container_name)

    with open(input_filename, 'w') as input_file:
        input_file.write(input_data)
        print('Wrote input:', input_data)

    # Run the code in the container

    time_limit_thread = Thread(target=time_limit_lxc, args=(container_name, 2))
    time_limit_thread.start()
    with open(output_filename, 'w') as output_file, \
        open(error_filename, 'w') as error_file, \
        open(input_filename, 'r+') as input_file:
        c.attach_wait(lxc.attach_run_command, ['python3', '-c', code],
            stdout=output_file, stderr=error_file, stdin=input_file)
    if not c.running:
        return {'output': '', 'errors': '[Timeout error.]'}

    ignore_first_error(error_filename)

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

def stop_and_destroy(container_name):
    c = lxc.Container(container_name)

    if c.defined:
        # Stop the container
        if not c.stop():
            print("Failed to kill the container", file=sys.stderr)

    os.remove(get_output_filename(container_name))
    os.remove(get_error_filename(container_name))
    os.remove(get_input_filename(container_name))

def setup_base():
    # Create the container rootfs
    if not base.defined:
        print('Base container not defined, creating...')
        if not base.create("download", lxc.LXC_CREATE_QUIET, {"dist": "ubuntu",
                                                           "release": "trusty",
                                                           "arch": "amd64"}):
            print("Failed to create the container rootfs", file=sys.stderr)
            return
        print('Base container created')


    base.set_config_item('lxc.ephemeral', '1')

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

def get_log_filename(container_name):
    return 'log/' + container_name + '.log'

def ignore_first_error(error_filename):
    # Ignore first 5 lines of errors
    with open(error_filename, 'r') as error_file:
        data = error_file.read().splitlines(True)
    with open(error_filename, 'w') as error_file:
        error_file.writelines(data[5:])

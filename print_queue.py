from multiprocessing import Queue

message_queue = Queue()

def send_message(channel_id, text):
    """Adds a message to the message queue."""
    message_queue.put((channel_id, text))

def pop_message():
    """Pops a message from the message queue."""
    return message_queue.get(False)

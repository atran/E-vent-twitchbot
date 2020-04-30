import queue
import threading

class TwitchBot(threading.Thread):
	SECONDS_BETWEEN_NEXT_COMMAND = 5.0
	
	def __init__(self, irc, command_queue, log_filename=None, *args, **kwargs):
		self.irc = irc
		self.command_queue = command_queue
		self.running_command = None
		self.next_run = None

		reading_thread = threading.Thread(target=self.read_messages)
		reading_thread.start()

		throttle_thread = threading.Thread(target=self.throttle_messages)
		throttle_thread.start()

	def read_messages(self):
		while True:
			new_messages = self.irc.recv_messages()
			if not new_messages:
				continue
			else:
				print("[INFO] Message receieved")
				for message in new_messages:
					self.command_queue.put(message)

	def throttle_messages(self):
		while True:
			queue_empty = self.command_queue.empty()
			not_running = self.running_command is None		
			# If we're not running a command
			# and the queue is not empty
			# let's run something
			if (not_running and not queue_empty):
				self.running_command = self.command_queue.get()
				threading.Timer(
					self.SECONDS_BETWEEN_NEXT_COMMAND, 
					self.clear_running_command, 
				).start()
				print(self.running_command)

	def clear_running_command(self):
		print("[INFO] Done executing command")
		self.running_command = None

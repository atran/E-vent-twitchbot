import time
import queue
import threading

class TwitchBot(threading.Thread):	
	def __init__(self, irc, command_queue, reply_enabled, log_filename=None, *args, **kwargs):
		self.irc = irc
		self.command_queue = command_queue
		self.respond = reply_enabled
		self.running_command = None
		self.next_run = None

		self.reading_thread = threading.Thread(target=self.read_messages)
		self.reading_thread.start()

	def read_messages(self):
		while True:
			time.sleep(0.5)
			new_messages = self.irc.recv_messages()
			if not new_messages:
				continue
			else:
				print("[INFO] Message receieved")
				for message in new_messages:
					self.command_queue.put(message)

	def throttle_messages(self, debounce_time):
		queue_empty = self.command_queue.empty()
		not_running = self.running_command is None		
		# If we're not running a command
		# and the queue is not empty
		# let's run something
		if (not_running and not queue_empty):
			this_command = self.command_queue.get()
			self.running_command = this_command
			threading.Timer(
				debounce_time, 
				self.clear_running_command, 
			).start()

			if (self.respond):
				self.irc.send_msg('Running "%s" from %s 🤖⚡' % (this_command['message'], this_command['username']))
			return this_command
		else:
			return None

	def clear_running_command(self):
		print("[INFO] Done executing command")
		self.running_command = None

	def run(self, debounce_time):
		return self.throttle_messages(debounce_time)
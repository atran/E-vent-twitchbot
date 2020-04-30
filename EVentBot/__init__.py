#!/usr/bin/env python3
"""
E-Vent Twitch Bot
~~~~~~~~~~~~~~~~~~~~~
This bot monitors a Twitch channel's chat and relays the messages
to various external applications. A queue is used when too many
messages are sent.
"""

__author__ = "Anthony Tran"
__version__ = "0.1.0"
__license__ = "MIT"

import multiprocessing

from .irc import IRCClient
from .bot import TwitchBot

class BotManager:
  def __init__(self, username, password, channel):
    settings = {
      'username': username,
      'password': password,
      'channel': channel
    }

    self.irc = IRCClient(settings)
    self.bot = TwitchBot(self.irc, multiprocessing.Queue())

  def rcv_messages(self, debounce_time=5.0):
    return self.bot.run(debounce_time)
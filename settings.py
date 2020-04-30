import os

IRC = {
  'SERVER': 'irc.chat.twitch.tv',
  'USERNAME': os.environ['USERNAME'],
  'PASSWORD': os.environ['TWITCH_TOKEN'],
  'PORT': 6667,
  'CHANNEL': os.environ['CHANNEL']
}
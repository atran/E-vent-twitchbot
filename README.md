# E-Vent Bot

This bot is written for the SCI-Arc 2020 Spring Show. It reads messages from the Twitch chat window via IRC, parses them into commands, and then throttles the commands.


## Quickstart

Below is an example of how to use this library. Please note the `time.sleep` command as this protects from high CPU usage. 

```
import time
from EVentBot import BotManager

username = 'YOUR_USERNAME'
password = 'oauth:YOUR_OAUTH_TOKEN'
channel = '#twitchplaysarchitecture'
msg_debounce_time = 10.0

b = BotManager(username, password, channel)

while True:
    time.sleep(0.2)
    message = b.rcv_messages(msg_debounce_time)
    if message is None:
        continue
    else:
        print(message)
```

The `rcv_messages()` method returns a dictionary:

```
{
  'channel': '#twitchplaysarchitecture', 
  'username': 'sciarcforever', 
  'message': 'yak yak yak'
}
```

## Python Versions & Package Management

This module uses [Pipenv](https://github.com/pypa/pipenv) for package management. 

For installing and managing different Python versions, [Pyenv](https://github.com/pyenv/pyenv) is recommended. There is a [Windows version](https://github.com/pyenv-win/pyenv-win) that also exists.
# E-Vent Bot

This bot is written for the SCI-Arc 2020 Spring Show. It reads messages from the Twitch chat window via IRC, parses them into commands, and then throttles the commands.


## Quickstart

1. Copy `.env.example` to `.env` which will populate those variables into `settings.py`.  
2. This is run on Python 3.7 but any version of Python 3 works. There are no external dependencies. Because of this, it should just run out of the box:

```
python main.py
```

## Python Versions & Package Management

This module uses [Pipenv](https://github.com/pypa/pipenv) for package management. 

For installing and managing different Python versions, [Pyenv](https://github.com/pyenv/pyenv) is recommended. There is a [Windows version](https://github.com/pyenv-win/pyenv-win) that also exists.
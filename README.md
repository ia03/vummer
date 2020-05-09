# Vummer

Vummer is a Discord bot that can run Python scripts. To do this securely, it
creates an LXC container in which the code is run. Check out the Discord server
[here.](https://discord.gg/2NGbScj)

## Install

Dependencies are located in `requirements.txt`

```
pip install -r requirements.txt
```

[python3-lxc](https://github.com/lxc/python3-lxc) is also needed.

```
git clone https://github.com/lxc/python3-lxc.git
cd python3-lxc
pip install .
```

You need LXC installed and configured to support unprivileged LXC containers.

## Configuration

Create a new file `config.py` with the token variable set to that of your bot.
```
token='TOKEN HERE'
```

## Start

Run `main.py`
```
python3 main.py
```

## Disclaimer

I'm not responsible if you get hacked while running this. You are responsible
for your own safety.

<p align="center">
    <a href="github.address">
        <img src="https://upcdn.io/W142hJk/thumbnail/demo/4mrDXtYPJA.png.crop" alt="Rubpy" width="128">
    </a>
    <br>
    <b>Shad API Framework for Python</b>
    <br>
    <a href="https://github.com/shayanheidari01/rubika">
        Homepage
    </a>
    •
    <a href="https://github.com/shayanheidari01/rubika/tree/master/docs">
        Documentation
    </a>
    •
    <a href="https://pypi.org/project/rubpy/#history">
        Releases
    </a>
    •
    <a href="https://t.me/rubika_library">
        News
    </a>
</p>

## Rubpy

> Elegant, modern and asynchronous Shad API framework in Python for users and bots

### Accounts
```python
import asyncio
from shadpy import Client, handlers, Message

async def main():
    async with Client(session='ShadPy') as client:
        @client.on(handlers.MessageUpdates())
        async def updates(message: Message):
            await update.reply('`hello` __from__ **shadpy**')
        await client.run_until_disconnected()

asyncio.run(main())
```

**Another example:**
```python
from shadpy import Client
from asyncio import run

async def main():
    async with Client(session='ShadPy') as client:
        result = await client.send_message('me', '`hello` __from__ **shadpy**')
        print(result)

run(main())
```

**ShadPy** is a modern, elegant and asynchronous framework. It enables you to easily interact with the main Shad API through a user account (custom client) or a bot
identity (bot API alternative) using Python.


### Key Features

- **Ready**: Install Rubpy with pip and start building your applications right away.
- **Easy**: Makes the Shad API simple and intuitive, while still allowing advanced usages.
- **Elegant**: Low-level details are abstracted and re-presented in a more convenient way.
- **Fast**: Boosted up by pycryptodome, a high-performance cryptography library written in C.
- **Async**: Fully asynchronous (also usable synchronously if wanted, for convenience).
- **Powerful**: Full access to Shad's API to execute any official client action and more.

### Installing

``` bash
pip3 install -U shadpy
```
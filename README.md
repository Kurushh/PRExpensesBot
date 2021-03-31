# Requirements:
* python 3.9.2
* [redis-server](https://redis.io/topics/quickstart)
# Python dependencies:
* [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
* [redis-py](https://github.com/andymccurdy/redis-py)

# If you're new to redis or never used it:
If you plan to keep this bot running, please be sure to read atleast [this](https://redis.io/topics/memory-optimization#memory-allocation).
Keep your redis istance in [protected mode](https://redis.io/topics/security) because a malicious adversary could easily exploit your database if you expose your redis-server to the internet. Protected Mode is enabled by default, so if you don't change anything in config you'll be ok. 

# Usage
1. Get your [telegram bot token](https://core.telegram.org/bots#creating-a-new-bot)
2. Download the code, look for the ``mytoken`` variable (line 162) and insert your bot token inside the ``".."``
3. Install redis-server, test it, config it and so on
4. Run a redis-server istance
5. Run the bot
6. Go on Telegram, look for you bot, type /help
7. Enjoy
8. (Optional) Make sure to complain about it or suggest how it could be improved

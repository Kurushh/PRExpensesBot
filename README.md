# Requirements:
* [python 3.9.2](https://www.python.org/)
* [redis-server](https://redis.io/topics/quickstart)
# Python dependencies:
* [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
* [redis-py](https://github.com/andymccurdy/redis-py)

# If you're new to redis or never used it:
If you plan to keep this bot running, please be sure to read atleast [this](https://redis.io/topics/memory-optimization#memory-allocation).
Keep your redis istance in [protected mode](https://redis.io/topics/security) because a malicious adversary could easily exploit your database if you expose your redis-server to the internet. Protected Mode is enabled by default, so if you don't change anything in config you'll be ok. 

# Usage
1. Get your [telegram bot token](https://core.telegram.org/bots#creating-a-new-bot)
2. Download the code
3. Edit ``bot.py`` with your favorite editor: look for the ``mytoken`` variable (line 162) and insert your bot token inside the ``".."``
4. Install redis-server, test it, config it and so on
5. Run a redis-server istance
6. Run the bot
7. Go on Telegram, look for you bot, type /help
8. Enjoy
9. (Optional) Make sure to complain about it or suggest how it could be improved

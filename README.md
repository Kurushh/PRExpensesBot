# Introduction
PRExpensesBot is a telegram bot that works as an user interface to a redis database you (or someone else) host! It runs without smoothly on a Raspberry Pi.
It is used to keep track of your monthly expenses, bills, purchases and so on.
## What this bot can do:
* You can add new expenses to the database
* For each item you can (optionally) specify a group or category i.e "Food","Bills","Hobby"
* At the end of each month, the bot will send you a recap (or use /log if in whanever you want)
* It is multi-user compatible, if your friends or relatives want to use it, they can use your redis server instance.
* You added something by mistake (or something you regret)? Don't worry there's a command to /del ete it!
* At the end of each year, you will get a long general recap
* (Work in progress) If recap bothers you, you can disable them!
* (Work in progress) Data visualization
# Requirements:
* [python 3.9.2](https://www.python.org/)
* [redis-server](https://redis.io/topics/quickstart)
## Python dependencies:
* [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
* [redis-py](https://github.com/andymccurdy/redis-py)

# If you're new to redis or never used it:
If you just wanna try the bot one time, you're fine with redis default configs
Otherwise, please be sure to read atleast [this](https://redis.io/topics/memory-optimization#memory-allocation). I'm actually testing it with a limit of 50mb; generally the more people use the same istance, the more the expenses amount to, the greater the limit need to be. But chill, you're not running twitter, so it is unlikely that you will use tons of memory.
Please, keep your redis istance in [protected mode](https://redis.io/topics/security), it is enabled by default, so if you don't change anything in config you'll be ok. 

# Usage
1. [Create a new bot and get its telegram bot token](https://core.telegram.org/bots#creating-a-new-bot)
2. Download the code, edit ``bot.py`` inside the directory with your favorite editor
3. Look for the ``mytoken`` variable (line 162) and insert your bot token inside the quotation marks ``" "``
4. Install redis-server, test it, eventually config it
5. Run a redis-server istance
6. Run the bot
7. Go on Telegram, look for you bot, type /help
8. Enjoy
9. (Optional) Make sure to complain about it or suggest how it could be improved

# License
Released under the [MIT License](https://mit-license.org/)

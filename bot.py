import telegram.ext
from telegram.ext import Updater, CommandHandler, CallbackContext
import logging
import redis
import datetime


# Basic logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO #eventually switched with DEBUG
        )
logger = logging.getLogger(__name__)

client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

def generate_log(context):
    usr_id = str(context)
    psum = 0.0
    cnt = 0
    groups = dict()
    itlist = []
    for item in client.smembers(get_current_month()):
        iprice = 0.0
        iqt = 0.0
        if(client.hget(item, 'owner') == usr_id ): 
            iprice = float(client.hget(item,'price') )
            iqt = float(client.hget(item, 'qt') )
            psum = psum + (iprice * iqt)
            cnt = cnt + int(iqt)
            i = client.hget(item,'name')
            i2 = str (round( (iprice*iqt), 2) )
            if client.hexists(item,'group') == True:
                grpname = client.hget(item, 'group')
                itlist = itlist + [[grpname,i,i2]]
                if grpname in groups:
                    groups[grpname] = groups[grpname] + iprice * iqt
                else:
                    groups[grpname] = iprice * iqt
            else:
                itlist = itlist + [['*',i,i2]]

    text = "You spent a total of " + str(round(psum, 2)) + " bucks\n"
    text = text + "You added a total of " +str(cnt)+" items\n\n\n"
    text2 = "" #please delete text2, it's useless just use text

    itlist.sort() # .sort() by the first element in list: the group
    flag = '*'
    for key in itlist:
        if key[0] != flag:
            text2 = text2 + "\n\n"
            flag = key[0]
            text2 = text2 + key[0] + ': ' + str(round(groups[key[0]],2)) + " bucks\n"
        text2 = text2 + key[1] + " " + key[2] + "\n"

    return text+text2


def debug_log(update, context):
    text = generate_log(update.message.from_user.id)
    context.bot.send_message(update.message.chat_id, text=text)


def _log(context):
    chat_id = str(context.job.context.message.chat_id)
    text = generate_log(context.job.context.message.from_user.id)
    context.bot.send_message(chat_id=chat_id, text=text)


def del_last_added(update, context): #investigate on why pipeline give problems
    #context.args[0] is an integer taken as (optional) input argument from user
    #If context.args[0] exists and the list is not empty
    #And the qt value of the last added item is strictly greater than the input 
    #Then decrement last added item 'qt' by context.args[0] value

    text = 'Success!'
    usr_id = update.message.from_user.id
    i_to_decr = client.lindex(str(usr_id), 0)
    if i_to_decr is not None and len(context.args)==1: 
        can_decr = int(client.hget(i_to_decr, 'qt')) > int(context.args[0])
        if can_decr:
            client.hincrby(i_to_decr, 'qt', -(int(context.args[0])) )
            update.message.reply_text(text)
            return

    #Otherwise , just delete the last added voice
    try:    
        last_added = client.lpop(usr_id)
        client.delete(last_added)
        client.srem(get_current_month(), last_added)
    except redis.exceptions.DataError:
        text = "Database empty, feel free to /add something"
    finally:
        update.message.reply_text(text)


def add(update,context):
        cm = get_current_month()
        usr_id = update.message.from_user.id
        text = 'Item successfully inserted! Next!'

        # For each item inserted this month, filter for items owned by the 
        # user,if you find that name and price is the same of a previously 
        #added item, then there is no need to create a new item: increase quantity of item
        try:
            for item in client.sscan_iter(cm):
                same_owner = client.hget(item, 'owner') == str(usr_id)
                same_name = client.hget(item, 'name') == context.args[0].capitalize()
                same_price = float(client.hget(item, 'price')) == float(context.args[1])
                if (same_owner and same_name and same_price) == True:
                        client.hincrby(item,'qt',context.args[2])
                        return

            # Otherwise, create a new voice for the database
            new_voice = dict() 
            new_voice['name']= context.args[0].capitalize()
            new_voice['price']= float(context.args[1])
            new_voice['qt'] = context.args[2]
            new_voice['date']= cm
            new_voice['owner']= usr_id
            if len(context.args)==4:
                new_voice['group']= context.args[3].capitalize()

            client.incr("unique_item_id")
            item_id = str(client.get("unique_item_id"))
            client.hset(name=item_id, mapping=new_voice)
            client.lpush(usr_id, item_id)
            client.sadd(cm, item_id) 

        except ValueError: 
            text = "Error: make sure 'name' is a string, 'price' a float or integer"
            text = text+" and 'price' an integer"
        except IndexError:
            text = "Error:  you need to use the format:\n/add 'name' 'price' 'qt'"
        finally:
            update.message.reply_text(text)


def get_current_month(): 
    current_month = str(datetime.date.today().month)
    current_year = str(datetime.date.today().year)
    return current_month +'-'+current_year

def start(update,context):
    chat_id = update.message.chat.id
    username = update.message.from_user.username
    text = "Hi "+ username + "! Bot is initialized\n"
    text = text + "Use /help to get the full list of commands"

    context.bot.send_message(chat_id=chat_id, text=text)
    
    time = datetime.time(19,00,00)
    context.job_queue.run_monthly(callback=_log, when=time, day=30,\
            context=update, day_is_strict=False)


def help(update,context):
    text= '''
    Hi this bot can help you to keep track of your expenses.\n\n
    Use "/start" to initialize the bot \nAfter you initialized it,every last 
    day of the month, the bot will send you a message with the sum of expenses
    and items inserted into the database\n\n
    Use "/add <name> <price> <quantity>" to add a new item in the bot's database\n
    Price and quantity need to be numbers!\n Example: '/add pizza 4 1' ( 3.86 instead
    of 4 also works)\nYou can also specify an extra argument <group> i.e "Food" or "Bills". 
    At the end of the month you will get a message with the total cost of all items for each group you've created\n\n
    Use "/del (optional)<number>" to delete the last item added or decrement his quantity by 
    some value\n Example:"/del 2" it will decrease the stored quantity of the last added item by 2.
    \nThis command is meant to be used in case of mistakes\n\n.
    Use "/log" to istantly get the monthly log (for debug purposes)
    '''
    update.message.reply_text(text)

def main():
    mytoken = ""
    updater = Updater(mytoken, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('help',help))
    dispatcher.add_handler(CommandHandler('start',start, pass_job_queue=True))
    dispatcher.add_handler(CommandHandler('add',add))
    dispatcher.add_handler(CommandHandler('del',del_last_added))
    dispatcher.add_handler(CommandHandler('log',debug_log)) #for debug purposes
    updater.start_polling()
    updater.idle()


if __name__=='__main__':
    main()

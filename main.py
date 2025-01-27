import MetaTrader5 as mt5
from telethon import TelegramClient, events
import re

#Metatrade5 login details
account=313156863
serverName="XMGlobal-MT5 7"
password="@Hayabusa256"

#Telegram login details
api_id = '24319261'
api_hash = '617b129d2d42790112702f2cc783211c'
phone_number = '+639539870591'

if not mt5.initialize(login=account, server=serverName,password=password):
    print("initialize() failed, error code =",mt5.last_error())
    quit()
 
else:
    print("initialize() succeeded")
    mt5.shutdown()




    

# def telegramBotListener():
#     print("Bot is listening to telegram...")


    # symbol="GOLD"
    # point=mt5.symbol_info(symbol).point
    # request = {
    # "action": mt5.TRADE_ACTION_DEAL,
    # "symbol": symbol,
    # "volume": 1.0,
    # "type": mt5.ORDER_TYPE_BUY,
    # # "price": mt5.symbol_info_tick(symbol).ask,
    # # "sl": mt5.symbol_info_tick(symbol).ask-100*point,
    # # "tp": mt5.symbol_info_tick(symbol).ask+100*point,
    # "deviation": 10,
    # "magic": 234000,
    # "comment": "python script",
    # "type_time": mt5.ORDER_TIME_GTC,
    # "type_filling": mt5.ORDER_FILLING_IOC,
    # }

    # result = mt5.order_send(request)

    # if result.retcode == mt5.TRADE_RETCODE_DONE:
    #     print("Market order placed successfully")
    # else:
    #     print(f"Failed to place market order. Error code: {result.retcode}")



if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    quit()

telegram = TelegramClient('anon', api_id, api_hash)
trading = mt5.login(login=account, server=serverName, password=password)

if trading:
    print("Login successful in Metatrader5")
    #telegramBotListener()
else:
    print("Login failed")
    print(mt5.last_error())

#################################Telegram Bot############################################

async def create_order(request):

    result = mt5.order_send(request)

    if result.retcode == mt5.TRADE_RETCODE_DONE:
        print("Market order placed successfully")
        #return True
    else:
        print(f"Failed to place market order. Error code: {result.retcode}")
        #return False
    
async def garyGoldTrader(message):
    pattern = r"(buy|sell)\s+now.*sl:(\d+(\.\d+)?)\s*tp1:(\d+(\.\d+)?)\s*tp2:(\d+(\.\d+)?)"


    # Extract data
    symbol = "GOLD"
    match = re.search(pattern, message)

    if match:
        action = match.group(1).lower()  # Action (buy or sell)
        sl = float(match.group(2))  # Stop loss value
        tp1 = float(match.group(4))  # Take profit 1 value
        tp2 = match.group(6)  # Take profit 2 value
        #print(f"Action: {action.capitalize()}, SL: {sl_value}, TP1: {tp1_value}, TP2: {tp2_value}")

        if(action == "buy"):
            action = mt5.ORDER_TYPE_BUY
        else:
            action = mt5.ORDER_TYPE_SELL
        
        request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": 1.0,
        "type": action,
        # "price": mt5.symbol_info_tick(symbol).ask,
        "sl": sl,
        "tp": tp1,
        "deviation": 10,
        "magic": 234000,
        "comment": "python script",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
        }
            
        await create_order(request)
    else:
        print("No match found in Gary Gold Trader!")


async def benGoldTrader(message):
    pattern = r"(buy|sell)\s+.*sl\s*[:\s]*(\d+(\.\d+)?)\s*tp1\s*[:\s]*(\d+(\.\d+)?)\s*tp2\s*[:\s]*(\d+(\.\d+)?)"

# Search for the pattern in the text
    match = re.search(pattern, message)

    if match:
        action = match.group(1)  # Action (buy or sell)
        sl = float(match.group(2))  # Stop loss value
        tp1 = float(match.group(4))  # Take profit 1 value
        tp2 = float(match.group(6))  # Take profit 2 value
        #print(f"Action: {action.capitalize()}, SL: {sl_value}, TP1: {tp1_value}, TP2: {tp2_value}")

        symbol = "GOLD"

        if(action == "buy"):
            action = mt5.ORDER_TYPE_BUY
        else:
            action = mt5.ORDER_TYPE_SELL

        request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": 1.0,
        "type": action,
        # "price": mt5.symbol_info_tick(symbol).ask,
        "sl": sl,
        "tp": tp1,
        "deviation": 10,
        "magic": 234001,
        "comment": "python script",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
        }
        
        print(action, sl, tp1, tp2)
        await create_order(request)
    else:
        print("No match found in Ben Gold Trader!")
        
async def chat_filter(chatId, message):
    if chatId == -1001774783341:
        await garyGoldTrader(message)
    if chatId == -1001765226347:
        await benGoldTrader(message)

async def list_chats():
    await telegram.start(phone=phone_number)  # Ensure the client is started
    dialogs = await telegram.get_dialogs()
    for dialog in dialogs:
        print(f"Chat Name: {dialog.name}, Chat ID: {dialog.id}")

@telegram.on(events.NewMessage)
async def telegramBotListener(event):
    message = re.sub(r'\s+', ' ', event.message.text).strip().lower()
    await chat_filter(event.chat_id, message)
    print(message)

async def telegramBot():
    await telegram.start(phone=phone_number)
    await list_chats()

telegram.loop.run_until_complete(telegramBot())
telegram.run_until_disconnected()
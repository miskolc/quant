# ae_h - 2018/8/11
import websockets
import asyncio

import asyncio
import websockets
from dao.futu_opend import futu_opend
import asyncio
import json
import logging
import websockets
from log.quant_logging import logger


logging.basicConfig()

STATE = {'value': 0}

USERS = set()

def state_event():
    return json.dumps({'type': 'state', **STATE})

def users_event():
    return json.dumps({'type': 'users', 'count': len(USERS)})

async def notify_state():
    if USERS:       # asyncio.wait doesn't accept an empty list
        message = state_event()
        await asyncio.wait([user.send(message) for user in USERS])

async def notify_users():
    if USERS:       # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])

async def register(websocket):
    USERS.add(websocket)
    logger.debug(USERS)
    await notify_users()

async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()

async def counter(websocket, path):
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    try:
        await websocket.send(state_event())
        async for message in websocket:
            data = json.loads(message)
            if data['action'] == 'minus':
                STATE['value'] -= 1
                await notify_state()
            elif data['action'] == 'plus':
                STATE['value'] += 1
                await notify_state()
            else:
                logging.error(
                    "unsupported event: {}", data)
    finally:
        await unregister(websocket)

asyncio.get_event_loop().run_until_complete(
    websockets.serve(counter, 'localhost', 6789))
asyncio.get_event_loop().run_forever()


# async def ws(websocket, path):
#     while True:
#         st, df = futu_opend.quote_ctx.get_market_snapshot(['SH.601398'])
#         df = df.to_json(orient='records')
#
#         await websocket.send(df)
#         await asyncio.sleep(5)
#
#
# # start_server = websockets.serve(ws, '127.0.0.1', 5678)
# #
# # asyncio.get_event_loop().run_until_complete(start_server)
# # asyncio.get_event_loop().run_forever()
#
#
# import time
# from futuquant import *
#
#
# class StockQuoteTest(StockQuoteHandlerBase):
#     def on_recv_rsp(self, rsp_str):
#         ret_code, data = super(StockQuoteTest, self).on_recv_rsp(rsp_str)
#         if ret_code != RET_OK:
#             print("StockQuoteTest: error, msg: %s" % data)
#             return RET_ERROR, data
#
#         # print("StockQuoteTest ", data) # StockQuoteTest自己的处理逻辑
#
#         return RET_OK, data
#
#
# quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
# handler = StockQuoteTest()
# quote_ctx.set_handler(handler)
# time.sleep(15)
# quote_ctx.close()

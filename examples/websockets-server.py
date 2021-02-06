import os
import json
import logging

import aiohttp
from aiohttp import web

HOST = os.getenv('HOST', '127.0.0.1')
PORT = int(os.getenv('PORT', 1339))


#  Just a modified echo server to demo expectations.
#  The good stuff is in: websockets-client.py


async def websocket_handler(request):
    print('Websocket connection starting')
    ws = aiohttp.web.WebSocketResponse()
    await ws.prepare(request)
    print('Websocket connection ready')
    await ws.send_str(json.dumps({
        'method': 'welcome',
        'data': "Welcome to the server.",
        'eid': 0.1
    }))
    async for msg in ws:
        print(msg)
        if msg.type == aiohttp.WSMsgType.TEXT:
            try:
                client_message = msg.data.rstrip()
                j = json.loads(client_message)
                print('Got JSON from client: ', j)
            except:
                print('Got plain message from client:', msg.data)
                continue

            if j['method'] == 'close':
                await ws.close()
            else:
                await ws.send_str(json.dumps({
                    'method': 'echo',
                    'data': j['method'],
                    'eid': j['eid']
                }))

    print('Websocket connection closed')
    return ws


def main():
    app = web.Application()
    app.add_routes([
        web.get('/ws', websocket_handler)
    ])
    web.run_app(app, host=HOST, port=PORT)


if __name__ == '__main__':
    main()

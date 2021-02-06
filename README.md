# Expectations for Python

**Asynchronous expectations (Jobs/tasks) for future events.**

If client user sends a message to server, a new eid is generated and sent with the message. If server sends back a message
with an eid, the eid is checked against our expectations. If eid matches an expectation, that expectation's callback
will run. If server sends a message without an eid, no expectations will be checked.

## Installation

Pypi package is present.

`pip install expectations`

## Implementation

**Important steps are marked 1-4.**

```python
import asyncio
import os
import json
import aiohttp
from expectations import Expector, eidgen

HOST = os.getenv('HOST', '127.0.0.1')
PORT = int(os.getenv('PORT', 1339))

URL = f'http://{HOST}:{PORT}/ws'


def my_expected_proc(data):  # Simple function we will use as our expectation callback.
	print('Processed expectation:', data)


async def main():
	session = aiohttp.ClientSession()
	expector = Expector()  # 1: Get setup.
	async with session.ws_connect(URL) as ws:
		async for msg in ws:
			try:
				server_message = msg.data.rstrip()
				j = json.loads(server_message)

				if 'eid' in j:
					# 4: See if incoming eid from server matches any of our expectations.
					expected = await expector.check_expectations(j['eid'], server_message)
					if expected:
						# Give expected callback a second to process (For demo purposes; so it runs before prompt)
						await asyncio.sleep(1000)
					else:
						raise Exception(f'Unexpected message from server: {msg}')
			except Exception as ex:
				print(ex)
			finally:
				await prompt_and_send(ws, expector)

			if msg.type in (aiohttp.WSMsgType.CLOSED,
			                aiohttp.WSMsgType.ERROR):
				break


async def prompt_and_send(ws, expector):
	user_msg = input('Type a message to send to the server: ')
	if user_msg == 'exit':
		print('Exiting!')
		raise SystemExit(0)

	eid = eidgen()  # 2: Create new expectation ID (eid).
	await expector.expect(eid, my_expected_proc)  # 3: Create new expectation using eid and any callback function.

	await ws.send_str(json.dumps({
		'method': user_msg,
		'eid': eid  # eid is sent with msg (For demo). If we get this eid back later, the expectation callback will run.
	}))


if __name__ == '__main__':
	print('Type "exit" to quit')
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())

```


**MIT License**
# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['expectations']

package_data = \
{'': ['*']}

install_requires = \
['aiojobs<1.0']

setup_kwargs = {
    'name': 'expectations',
    'version': '1.0.1',
    'description': 'Asynchronous expectations (Jobs/tasks) for future events.',
    'long_description': '# Expectations for Python\n\n**Asynchronous expectations (Jobs/tasks) for future events.**\n\nIf client user sends a message to server, a new eid is generated and sent with the message. If server sends back a message\nwith an eid, the eid is checked against our expectations. If eid matches an expectation, that expectation\'s callback\nwill run. If server sends a message without an eid, no expectations will be checked.\n\n## Installation\n\nPypi package is present.\n\n`pip install expectations`\n\n## Implementation\n\n**Important steps are marked 1-4.**\n\n```python\nimport asyncio\nimport os\nimport json\nimport aiohttp\nfrom expectations import Expector, eidgen\n\nHOST = os.getenv(\'HOST\', \'127.0.0.1\')\nPORT = int(os.getenv(\'PORT\', 1339))\n\nURL = f\'http://{HOST}:{PORT}/ws\'\n\n\ndef my_expected_proc(data):  # Simple function we will use as our expectation callback.\n\tprint(\'Processed expectation:\', data)\n\n\nasync def main():\n\tsession = aiohttp.ClientSession()\n\texpector = Expector()  # 1: Get setup.\n\tasync with session.ws_connect(URL) as ws:\n\t\tasync for msg in ws:\n\t\t\ttry:\n\t\t\t\tserver_message = msg.data.rstrip()\n\t\t\t\tj = json.loads(server_message)\n\n\t\t\t\tif \'eid\' in j:\n\t\t\t\t\t# 4: See if incoming eid from server matches any of our expectations.\n\t\t\t\t\texpected = await expector.check_expectations(j[\'eid\'], server_message)\n\t\t\t\t\tif expected:\n\t\t\t\t\t\t# Give expected callback a second to process (For demo purposes; so it runs before prompt)\n\t\t\t\t\t\tawait asyncio.sleep(1000)\n\t\t\t\t\telse:\n\t\t\t\t\t\traise Exception(f\'Unexpected message from server: {msg}\')\n\t\t\texcept Exception as ex:\n\t\t\t\tprint(ex)\n\t\t\tfinally:\n\t\t\t\tawait prompt_and_send(ws, expector)\n\n\t\t\tif msg.type in (aiohttp.WSMsgType.CLOSED,\n\t\t\t                aiohttp.WSMsgType.ERROR):\n\t\t\t\tbreak\n\n\nasync def prompt_and_send(ws, expector):\n\tuser_msg = input(\'Type a message to send to the server: \')\n\tif user_msg == \'exit\':\n\t\tprint(\'Exiting!\')\n\t\traise SystemExit(0)\n\n\teid = eidgen()  # 2: Create new expectation ID (eid).\n\tawait expector.expect(eid, my_expected_proc)  # 3: Create new expectation using eid and any callback function.\n\n\tawait ws.send_str(json.dumps({\n\t\t\'method\': user_msg,\n\t\t\'eid\': eid  # eid is sent with msg (For demo). If we get this eid back later, the expectation callback will run.\n\t}))\n\n\nif __name__ == \'__main__\':\n\tprint(\'Type "exit" to quit\')\n\tloop = asyncio.get_event_loop()\n\tloop.run_until_complete(main())\n\n```\n\n\n**MIT License**',
    'author': 'TensorTom',
    'author_email': '14287229+TensorTom@users.noreply.github.com',
    'maintainer': 'TensorTom',
    'maintainer_email': '14287229+TensorTom@users.noreply.github.com',
    'url': 'https://localhost',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asynctranslator']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=4.5.0,<5.0.0']

setup_kwargs = {
    'name': 'asynctranslator',
    'version': '1.0.1',
    'description': 'Typed Async-to-sync & Sync-to-async utility',
    'long_description': '# ASyncTranslator\n\nA package to transform your **sync** methods to **async** methods and to turn **async** methods to **sync** methods.\n\n🤩 ✨ **FINALLY TYPED EDITION!!!** ❤️ 🤌\n\nThis is an heavy inspiration from Django\'s implementation.\nPlease see https://github.com/django/asgiref/blob/30d891fab0a7caa265bda0cbe04bb35a00a3b3b9/asgiref/sync.py for original reference.\n\n## Show me an example, pretty please.\n\nHere you go!\n\nTo transform from an **async** to **sync** method:\n```py\nfrom asynctranslator import async_to_sync\n\nasync def my_async_func(food_name: str) -> int:\n    print(f"{food_name} are my favorite!")\n    return 42\n\ndef main():\n    final_func = async_to_sync(my_async_func)\n    result = final_func("Cookies")\n    print(result)  # We got "42"!\n\nmain()\n```\n\nAnd now, to transform from a **sync** to **async** method:\n```py\nimport asyncio\nfrom asynctranslator import sync_to_async\n\ndef my_async_func(food_name: str) -> int:\n    print(f"{food_name} are my favorite!")\n    return 42\n\nasync def main():\n    final_func = sync_to_async(my_async_func)\n    result = await final_func("Cookies")\n    print(result)  # We got "42"!\n\nasyncio.run(main())\n```\n\nBut you can also use it as a decorator!\n\n```py\nimport asyncio\nfrom asynctranslator import sync_to_async\n\n@sync_to_async\ndef my_async_func(food_name: str) -> int:\n    print(f"{food_name} are my favorite!")\n    return 42\n\nasync def main():\n    result = await my_async_func("Cookies")\n    print(result)\n\nasyncio.run(main())\n```\n',
    'author': 'Predeactor',
    'author_email': 'pro.julien.mauroy@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

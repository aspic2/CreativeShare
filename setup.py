try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Tool for Google DFP. Shares creative from one Line Item to another',
    'author': 'Michael Thompson',
    'url': 'n/a',
    'download_url': 'n/a',
    'author_email': 'm thompson at cars dot com',
    'version': '0.1',
    'install_requires': ['nose', 'googleads', 'openpyxl'],
    'packages': ['NAME'],
    'scripts': [],
    'name': 'CreativeShare'
}

setup(**config)

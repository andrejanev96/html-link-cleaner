from setuptools import setup

APP = ['app.py']  # Your Flask app file
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'includes': ['flask', 'bs4'],
    'packages': ['flask', 'bs4'],
    'plist': {
        'CFBundleName': 'HTML Link Cleaner',
        'CFBundleDisplayName': 'HTML Link Cleaner',
        'CFBundleGetInfoString': "HTML Cleaner for removing specific links",
        'CFBundleIdentifier': 'com.yourname.htmllinkcleaner',
        'CFBundleVersion': '0.1',
        'CFBundleShortVersionString': '0.1',
    },
}

setup(
    app=APP,
    name='HTML Link Cleaner',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
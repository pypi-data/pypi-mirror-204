from setuptools import setup

setup(
    name="tgbox-cli",
    version='0.1',
    author='NotStatilko',
    author_email='thenonproton@pm.me',
    py_modules=['tgbox_cli','tgbox_cli_tools'],
    description='A CLI Interface to the TGBOX < 1.0',
    url = 'https://github.com/NotStatilko/tgbox-cli',

    install_requires=[
        'click==8.1.3',
        'tgbox<1'
    ],
    entry_points='''
        [console_scripts]
        tgbox-cli=tgbox_cli:safe_cli
    ''',
)

from setuptools import setup

setup(
    name = 'ATHERIUSMT5',
    version = '0.0.2',
    description = 'support get candle from mt5',
    py_modules=['atheriusmt5'],
    package_dir = {'': 'src'},
    install_requires=[
        'MetaTrader5',
        'pandas',
        'requests',
        'Pillow'
    ]
)
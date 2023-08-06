from setuptools import setup

setup(
    name='squad-foundries-plugins',
    version='1.0',
    author='Milosz Wasilewski',
    author_email='milosz.wasilewski@foundries.io',
    url='https://github.com/foundries/squadplugins',
    packages=['mcu'],
    entry_points={
        'squad_plugins': [
            'mcu=mcu:MCUResults',
        ]
    },
    license='LGPLv3+',
    description="SQUAD Foundries plugins",
    long_description="""
    SQUAD plugins that are compatible with Linaro's test-definitions.
    The package contains plugin for parsing MCU testing logs.
    """,
    platforms='any',
    install_requires=['squad[postgres]>=1.32', 'requests']
)

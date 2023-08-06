from setuptools import setup

packages = [
    'liftcord',
    'liftcord.types',
    'liftcord.ui',
    'liftcord.webhook',
    'liftcord.app_commands',
    'liftcord.ext.commands',
    'liftcord.ext.tasks',
    'liftcord.mobile'
]

setup(
    name='liftcord',
    author='go.',
    url='https://github.com/devliftz/lift.py',
    version=25.9,
    packages=packages,
    license='MIT',
    description='A Python wrapper for the Discord API',
    long_description_content_type='text/x-rst',
    include_package_data=True,
    install_requires=['aiohttp>=3.7.4,<4'],
    python_requires='>=3.8.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Typing :: Typed',
    ],
)

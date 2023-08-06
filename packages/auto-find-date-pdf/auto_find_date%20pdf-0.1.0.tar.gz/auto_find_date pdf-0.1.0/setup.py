from setuptools import setup, find_packages

setup(
    name='auto_find_date pdf',
    version='0.1.0',
    description='A simple lib to find dates from any txt/ pdf/ rtf source',
    author='Your Name',
    packages=find_packages(),
    author_email='opensource@marvsai.com',
    py_modules=['text_search', 'main'],
    install_requires=[
        'pypdf',
        'pytz',
        'striprtf',
        'Pillow'
    ],
    entry_points='''
        [console_scripts]
        your_script_name=main:main
    '''
)

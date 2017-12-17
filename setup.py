from setuptools import setup, find_packages
from snake import constants

setup(
	name = 'console-snake',
	packages = ['snake'],
	python_requires='>=3',
	version = constants.VERSION,
	description = 'Snake for console',
	author = 'Marcus Mu',
	author_email = 'chunkhang@gmail.com',
	license = 'UNLICENSE',
	url = 'https://github.com/chunkhang/console-snake',
	keywords = [
		'snake',
		'console',
		'curses'
	], 
	classifiers = [
		'Intended Audience :: End Users/Desktop',
		'Environment :: Console',
		'Programming Language :: Python :: 3 :: Only'
	],
	entry_points = {
		'console_scripts': [
			'snake=snake.snake:main'
		]
	}	
)
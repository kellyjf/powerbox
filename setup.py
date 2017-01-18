from setuptools import setup

setup(
	name="powerbox",
	version="1.0",
	description="Open source power strip controller",
	author="John Kelly",
	author_email="jfkelly07@gmail.com",
	url="https://github.com/kellyjf/powerbox",
	license="BSD",
	py_modules=['app_gpio','app_monitor'],
	entry_points={'console_scripts': [ 'powerbox=app_monitor' ] }
)


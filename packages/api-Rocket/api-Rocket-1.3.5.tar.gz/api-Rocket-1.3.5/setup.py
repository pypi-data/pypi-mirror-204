import setuptools
with open(r'C:\Users\User\Desktop\Readme.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='api-Rocket',
	version='1.3.5',
	author='Redpiar',
	author_email='Regeonwix@gmail.com',
	description='Api for Ton Rocket',
	long_description=long_description,
	long_description_content_type='text/markdown',
	packages=['api_Rocket'],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)
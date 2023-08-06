import setuptools
with open(r'C:\Users\mr946\Desktop\Upload PYPI\WiFi_Access\README.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='WiFi_Access',
	version='1.0.0',
	author='MY_INSIDE',
	author_email='my.inside.dream@gmail.com',
	description='Простой инструмент для получения списка всех имён сетей WiFi и их пароля, к которым когда-либо был подключён ПК.',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/MY-INSIDE/WiFi_Access',
	packages=['WiFi_Access'],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)
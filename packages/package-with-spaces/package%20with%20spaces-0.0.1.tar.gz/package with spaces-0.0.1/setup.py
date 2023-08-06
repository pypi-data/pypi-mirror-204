import setuptools
import pip

setuptools.setup(
	name="package with spaces",
	version="0.0.1",
	author="me",
	author_email="email@email.it",
	description="Description",
	python_requires='>=3.6, <4',
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"Operating System :: OS Independent",
	],
	install_requires=[]
)
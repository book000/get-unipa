import setuptools

setuptools.setup(
    name='get-unipa',
    version=open("get-unipa.version").read().strip(),
    packages=setuptools.find_packages(),
    install_requires=["beautifulsoup4", "requests", "html5lib"],
    url='https://github.com/book000/get-unipa',
    license='MIT',
    author='Tomachi',
    author_email='tomachi@tomacheese.com',
    maintainer='Tomachi',
    maintainer_email='tomachi@tomacheese.com',
    description='Library for get various information about UNIVERSAL PASSPORT.',
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
    ],
)

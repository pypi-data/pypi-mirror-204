from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    
]

setup(
    name="fymjosh",
    version="1.0.6",
    description = 'A library that focuses on customization of console and discord',
    long_description ="fymjosh is a library that allows for your discord account to change statuses to like streaming, watching, listening, playing and helps to customize your discord account. Also has custom printing with rich features",
    url='',
    author='fymjosh',
    author_email='lone.cord12@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='discord, console',
    packages=find_packages(),
    install_requires=['websocket', 'websocket-client', 'asyncio', 'requests']
)
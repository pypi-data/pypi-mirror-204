from setuptools import setup, find_packages
import re

requirements = ['numpy', 'pandas', 'matplotlib', 'yfinance', "PyOpenGL", "glfw", "imgui[glfw]", "Pillow"] 

version = '0.0.5'

if not version:
    raise RuntimeError('version is not set')

readme = 'Coming Soon ...'

setup(
    name = 'py-portfolio-tools',
    author = 'Jaysmito Mukherjee',
    author_email = 'jaysmito101@gmail.com',
    url = 'https://gitlab.com/Jaysmito101/py-portfolio-tools',
    project_urls = {
        'Documentation': 'https://gitlab.com/Jaysmito101/py-portfolio-tools/-/wikis/Home',
        'Issue tracker': 'https://gitlab.com/Jaysmito101/py-portfolio-tools/-/issues',
    },
    version = version,
    packages = find_packages(),
    license = 'MIT',
    description = 'A Python Library and set of GUI tools for Portfolio Management',
    long_description = readme,
    long_description_content_type = 'text/markdown',
    include_package_data = True,
    install_requires = requirements,
    python_requires='>=3.8.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Office/Business :: Financial',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Typing :: Typed',
    ],
)

### [bwc-bsconf 0.1.1](https://pypi.org/project/bwc-bsconf/0.1.1/) 

This project better define server configurations, repairs and installations in various operating environments.

Developers can use the main features of the tool with this pip package.

Facilitate the installation of web servers, games, email, etc.

#### To Developers

<br>

### Installation

Install the package with pip:

via PyPI:

`pip install bwc-bsconf`

or via GitHub

`pip install git+https://github.com/BarcaWebCloud/bsconf-py.git`

<br>

Now Create a Python file to start using the **bwc-bsconf** package in your project. In the example below, the file named `main.py` was specified to run the bsconf module. Add the following content in the main file.

`main.py`

```py
import importlib

bwc_bsconf = importlib.import_module("bwc-bsconf")
init = bwc_bsconf.bsconf

init()
```

<br>

Run the main program

```
python3 main.py*
```
<br>

Will display on your screen something like this:

```
Welcome to BSconf
```
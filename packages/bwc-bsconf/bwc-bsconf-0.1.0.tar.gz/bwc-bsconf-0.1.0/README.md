### Pip [bwc-bsconf 0.1.0](https://pypi.org/project/bwc-bsconf/0.1.0/) 

This project better define server configurations, repairs and installations in various operating environments.


#### To Developers

<br>

1. Install the **wheel** module in your python environment

`pip install wheel`

<br>

2. Install **twine** which will be used to upload the tarball

`pip install twine`

<br>

3. Now compile the library setup of bsconf module

`python .\setup.py sdist bdist_wheel`

...

<br>

4. Publish or update package in Pip Manager

```
python3 -m twine upload dist/*
```
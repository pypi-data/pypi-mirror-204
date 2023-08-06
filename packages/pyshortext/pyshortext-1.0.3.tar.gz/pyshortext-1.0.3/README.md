# PyShorText
Python 3 library
# Description
PyShorText your url or text, author : RayServer
# Features 1.0.0
# Quickstart & Installation
PyShorText requires an installation of Python 3.6 or greater, as well as pip. (Pip is typically bundled with Python 
To install from the source with pip:
```
pip install pyshortext
```
- Using Short Url in a Python script
```
import pyshortext


text = "My Text or My URL"
url_acortada = pyshortext.short(text)
print(url_acortada)

url_desacortada = pyshortext.unshort(url_desacortada)
print(url_desacortada)
```


# lyxithea

Last Updated on 10/17/17

Written by [Alex Hagen](http://alexhagen.github.io)

Hosted at [github.com/alexhagen/lyxithea](http://github.com/alexhagen/lyxithea)

Documentation at [alexhagen.github.io/lyxithea/](http://alexhagen.github.io/lyxithea/)

## Introduction

``lyxithea`` - named as a mix between ``LyX``, the great $\LaTeX$ editing program, and *Lisithea* a moon of Jupiter - is a (very alpha) way to write LaTeX documents in Jupyter Notebook.  It currently allows completely for LaTeX export, and also some components allow HTML export.  It includes

- Bibliography
- LaTeX figure environments
- LaTeX tabulate environments
- Cross Referencing

For any problems or feature requests, send me an issue on [github](github.com/alexhagen/lyxithea) and I'll work on it!

### Demo

Once ``lyxithea`` is installed (a how-to is below), we can start to use it.  Below is an example on how to write a quick two column document with a figure, a table, and a bibliography, and export that to a pdf.

### Installation

To install `lyxithea`, all we have to do is install `numpy`, `scipy`, and
`matplotlib`, then download `lyxithea` to our code directory (or wherever, really).
To do this, we can use

```bash

$ pip install numpy
$ pip install scipy
$ pip install matplotlib
$ pip install colours
$ cd ~/code
$ git clone https://github.com/alexhagen/lyxithea.git

```

and then, we can use the library within any script by adding

```bash
sudo echo "export PYTHONPATH=${PYTHONPATH}:~/code:~/util" >> ~/.bashrc

```
to our ``.bashrc``.


```python

```

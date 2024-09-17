---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.4
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Hello Python and Jupyter

In this notebook you will:

* Learn how to use a Jupyter notebook such as this one
* Get a very quick tour of Python syntax and scientific libraries
* Learn some IPython features that we will use in later tutorials


## What is this?

This is Jupyter notebook running in a personal "container" just for you, stocked with example data, demos, and tutorials that you can run and modify. All of the software you'll need is already installed and ready to use.


## Run some Python code!

To run the code below:

1. Click on the cell to select it.
2. Press `SHIFT+ENTER` on your keyboard or press the <button class='btn btn-default'><span class='fa fa-step-forward'></span > Run</button> button in the toolbar above (in the toolbar above!).

```{code-cell} ipython3
1 + 1
```

Notice that you can edit a cell and re-run it.


The notebook document mixes executable code and narrative content. It supports text, links, embedded videos, and even typeset math: $\int_{-\infty}^\infty x\, d x = \frac{x^2}{2}$


## Whirlwind Tour of Python Syntax

### Lists

```{code-cell} ipython3
stuff = [4, 'a', 8.3, True]
```

```{code-cell} ipython3
stuff[0]  # the first element
```

```{code-cell} ipython3
stuff[-1]  # the last element
```

### Dictionaries (Mappings)

```{code-cell} ipython3
d = {'a': 1, 'b': 2}
```

```{code-cell} ipython3
d
```

```{code-cell} ipython3
d['b']
```

```{code-cell} ipython3
d['c'] = 3
```

```{code-cell} ipython3
d
```

**TIP:** For large or nested dictionaries, it is more convient to use `list()`.  Often custom python objects can be interrogated in the same manner.

```{code-cell} ipython3
list(d)
```

### Functions

```{code-cell} ipython3
def f(a, b):
    return a + b
```

In IPython `f?` or `?f` display information about `f`, such as its arguments.

```{code-cell} ipython3
f?
```

If the function includes inline documentation (a "doc string") then `?` displays that as well.

```{code-cell} ipython3
def f(a, b):
    "Add a and b."
    return a + b
```

```{code-cell} ipython3
f?
```

```{code-cell} ipython3
f??
```

Arguments can have default values.

```{code-cell} ipython3
def f(a, b, c=1):
    return (a + b) * c
```

```{code-cell} ipython3
f(1, 2)
```

```{code-cell} ipython3
f(1, 2, 3)
```

Any argument can be passed by keyword. This is slower to type but clearer to read later.

```{code-cell} ipython3
f(a=1, b=2, c=3)
```

If using keywords, you don't have to remember the argument order.

```{code-cell} ipython3
f(c=3, a=1, b=2)
```

## Fast numerical computation using numpy

For numerical computing, a numpy array is more useful and performant than a plain list.

```{code-cell} ipython3
import numpy as np

a = np.array([1, 2, 3, 4])
```

```{code-cell} ipython3
a
```

```{code-cell} ipython3
np.mean(a)
```

```{code-cell} ipython3
np.sin(a)
```

We'll use the IPython `%%timeit` magic to measure the speed difference between built-in Python lists and numpy arrays.

```{code-cell} ipython3
%%timeit

big = list(range(10000))  # setup line, not timed
sum(big)  # timed
```

```{code-cell} ipython3
%%timeit

big = np.arange(10000)  # setup line, not timed
np.sum(big)  # timed
```

If a single loops is desired for a longer computation, use `%time` on the desired line.

```{code-cell} ipython3
big = np.arange(10000)  # setup line, not timed
%time np.sum(big)  # timed
```

## Plotting using matplotlib

In an interactive setting, this will show a canvas that we can pan and zoom. (Keep reading for what we can do in a non-interactive setting, such as the static web page version of this tutorial.)

```{code-cell} ipython3
# We just have to do this line once, before we do any plotting.
%matplotlib widget
import matplotlib.pyplot as plt

plt.figure()
```

We can plot some data like so. In an interactive setting, this will update the canvas above.

```{code-cell} ipython3
plt.plot([1, 1, 2, 3, 5, 8])
```

And we can show a noninteractive snapshot of the state of the figure at this point by display the figure itself.

```{code-cell} ipython3
plt.gcf()
```

Displaying `plt.gcf()` (or any `Figure`) shows a non-interactive snapshot of a figure. Displaying `plt.gcf().canvas` or any `Canvas` gives us another interactive, live-updating view of the figure.


## Interrupting the IPython Kernel

Run this cell, and then click the square 'stop' button in the notebook toolbar to interrupt the infinite loop.

(This is equivalent to Ctrl+C in a terminal.)

```{code-cell} ipython3
# This runs forever -- hit the square 'stop' button in Jupyter to interrupt
# The following is "commented out". Un-comment the lines below to run them.
# while True:
#     continue
```

## "Magics"


The code entered here is interpreted by _IPython_, which extends Python by adding some conveniences that help you make the most out of using Python interactively. It was originally created by a physicist, Fernando Perez.

"Magics" are special IPython syntax. They are not part of the Python language, and they should not be used in scripts or libraries; they are meant for interactive use.

The `%run` magic executes a Python script.

```{code-cell} ipython3
%run hello_world.py
```

When the script completes, any variables defined in that script will be dumepd into our namespace. For example (as we will see below), this script happens to define a variable named `message`. Now that we have `%run` the script, `message` is in our namespace.

```{code-cell} ipython3
message
```

This behavior can be confusing, in the sense that the reader has to do some digging to figure out where ``message`` was defined and what it is, but it has its uses. Throughout this tutorial, we will use the `%run` magic as a shorthand for running boilerplate configuration code and defining variables representing hardware.


The `%load` magic copies the contents of a file into a cell but does not run it.

```{code-cell} ipython3
%load hello_world.py
```

Execute the cell a second time to actually run the code. Throughout this tutorial, we use the `%load` magic to load solutions to exercises.


## System Shell Access

Any input line beginning with a `!` character is passed verbatim (minus the `!`, of course) to the underlying operating system.

```{code-cell} ipython3
!ls
```

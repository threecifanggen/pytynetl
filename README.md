# pyTynETL

![branch-cov](badge/cov-badge.svg)  ![License](https://img.shields.io/github/license/threecifanggen/pytynetl) ![Issues](https://img.shields.io/github/issues/threecifanggen/pytynetl)

A Light-weighted Framework for ETL Task. The name `pytynetl` means "a tiny ETL framwork for Python."

## Function Composing

`pytynetl` provides an `f_` decorator to quickly composing functions to execute like a queer. For example, if you want to regard the functions below as a whole pipeline, using `f_` makes it more neatly. This feature
makes it possible to use functional programming to handle an ETL project, especially if it is just a list of tasks requiring linear executing.

```python
def f(x): return x + 1
def g(x): return x * 2
def h(x): return x / 3

h(g(f(1)))
```

```python
@f_
def f(x): return x + 1

@f_
def g(x): return x * 2

@f_
def h(x): return x / 3

(f >> g >> h)(1)
```

# pyTynETL

![branch-cov](badge/cov-badge.svg)  ![License](https://img.shields.io/github/license/threecifanggen/pytynetl) ![Issues](https://img.shields.io/github/issues/threecifanggen/pytynetl)

A Light-weighted Framework for ETL Task. The name `pytynetl` means "a tiny ETL framwork for Python."

## Function Composing

`pytynetl` provides an `f_` decorator to quickly composing functions to execute like a queer. For example, if you want to regard the functions below as a whole pipeline, using `>=` operator (can be read as "and then") makes it more neatly.  This feature makes it possible to use functional programming to handle an ETL project, especially if it is just a list of tasks requiring linear executing.

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

(f >= g >= h)(1)
```

## DAG Generating operators and decorators

The philosophy of ETL is to regard every task as a node in DAG. `pyTynETL` provides a lot of human-friendly operators and decorators to make DAG-generating processing quickly.  

### Node

We are using decorators to define ETL Node functions without initializing an object, which makes the codes more functional. You just need to write tasks as plain functions.

```python
from pytynetl import node_

@node_
def add1(x):
    return x + 1
```

### DAG

DAG is initialized by using the `etl_dag` function. The only things you do are containing nodes in it. After a dag is initialized, you can use `@` operator or `node_` decorator to add a node in it.

```python
from pytynetl import etl_dag

@node_
def mul2(x):
    return x

## using etl_dag to make a dag and add some nodes in it,
dag = etl_dag(add1)

## `@` operator to add a node to dag
mul2 @ dag

## `node_` decorator to add a function directly to dag 
@dag.node_
def pow2(x):
    return x ** 2
```

Edge operators attach two nodes. Two kinds of edges can defined here: dependent-task edges and independent-task edges.

While you want to put the formal task's output as input to deliver to the next task, dependent-task edges operator `>>=`/`<<=` can be applied here.

```python
add1 >>= pow2

# or, but not recommended
pow2 <<= add1
```

While you plainly want two tasks to execute in order, independent-task edges operator `>>`/`<<` can be applied here.

```python
mul2 >> pow2
add1 << pow2 # nor recommended
```

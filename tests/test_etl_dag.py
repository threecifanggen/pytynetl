from pytynetl.etl_dag import (
    node_,
    etl_dag_list,
)

def test_dag_operator():
    dag = etl_dag_list()

    @node_
    def add1(x):
        return x + 1

    @node_(task_name="multiple")
    def mul2(x):
        return x * 2
    
    @dag.node_
    def pow2(x):
        return x ** 2
    
    add1 @ dag 
    add1 >>= mul2 >> pow2

    print(mul2.dag)
    print(mul2.task_name)
    print(dag.nodes)
    print(dag)

    assert (add1 in dag)
    assert (mul2 in dag)
    assert (pow2 in dag)
    assert dag['multiple'](2) == 4
    assert dag['add1'](1) == 2
    assert dag['pow2'](1) == 1

def test_generate_dag_from_list():
    dag = etl_dag_list()

    @node_
    def add1(x):
        return x + 1

    @node_(task_name="multiple")
    def mul2(x):
        return x * 2
    
    @node_
    def pow2(x):
        return x ** 2
    
    etl_dag_list(add1, mul2, pow2)

    assert (add1 in dag)
    assert (mul2 in dag)
    assert (pow2 in dag)
    assert dag['multiple'](2) == 4
    assert dag['add1'](1) == 2
    assert dag['pow2'](1) == 1

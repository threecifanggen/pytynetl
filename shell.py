import os

from pytynetl import __version__

def test():
    """运行测试

    Examples:
        ```python
        ## 在代码行种使用如下命令即可执行测试
        poetry run test
        ```
    """
    os.system((
        'pytest '
        '--cov-report html:cov_html '
        '--cov-report xml:cov.xml '
        '--cov-report annotate:cov_annotate '
        '--cov-report= '
        '--cov=pytynetl '
        'tests/'))
    if os.path.isfile('badge/cov-badge.svg'):
        os.remove('badge/cov-badge.svg')
    os.system('coverage-badge -o badge/cov-badge.svg')

def docs():
    """生成DOC
    """
    build_dir = 'docs/build/'+ __version__
    source_dir = 'docs/source'
    build_main_dir = 'docs/build/main'
    os.system((
        f'sphinx-build -b html {source_dir} {build_dir}'
        ))
    os.system((
        f'sphinx-build -b html {source_dir} {build_main_dir}'
        ))
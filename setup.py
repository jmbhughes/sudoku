from setuptools import setup

setup(
    name='sudoku',
    version='0.1',
    packages=['tests', 'sudoku'],
    url='',
    license='',
    author='Marcus Hughes',
    author_email='hughes.jmb@gmail.com',
    description='',
    python_requires="~=3.7",
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    test_suite="tests",
    install_requires=["numpy", "graphviz"],
)

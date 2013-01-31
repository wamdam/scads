#!/bin/bash

#python runtests.py -s --doctest-glob='*.rst' --doctest-modules -l --cov=src --cov-report=term-missing src
python runtests.py -s --doctest-glob='*.rst' --doctest-modules --pep8 -l --cov=src --cov-report=term-missing src
#python runtests.py -s --doctest-glob='*.rst' --doctest-modules --pep8 -l --pdb --cov=src --cov-report=term-missing src

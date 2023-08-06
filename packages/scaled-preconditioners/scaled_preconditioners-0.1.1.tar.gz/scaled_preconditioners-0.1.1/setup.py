# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scaled_preconditioners']

package_data = \
{'': ['*']}

install_requires = \
['black>=23.3.0,<24.0.0',
 'flake8>=6.0.0,<7.0.0',
 'isort>=5.12.0,<6.0.0',
 'mypy>=1.2.0,<2.0.0',
 'nox-poetry>=1.0.2,<2.0.0',
 'pytest>=7.3.0,<8.0.0',
 'scikit-learn>=1.2.2,<2.0.0',
 'scipy>=1.10.1,<2.0.0']

setup_kwargs = {
    'name': 'scaled-preconditioners',
    'version': '0.1.1',
    'description': '',
    'long_description': '# Preconditioner Design via Bregman Divergences\n\nThis package implements the preconditioners in [1]. A simple use case\nis demonstrated below. See `examples/example_pcg.py` for a demo of all the \npreconditioners defined in this package.\n\n[1] TODO\n\n## Build Status\n\n[![Tests](https://github.com/andreasbock/scaled_preconditioners/actions/workflows/tests.yml/badge.svg)](https://github.com/andreasbock/scaled_preconditioners/actions/workflows/tests.yml)\n\n## Installation\n\n``pip install scaled_preconditioners``\n\n## A simple example\n\n#### Define some parameters\n```\ndimension = 100\npsd_rank = 50\n```\n\n#### Construct S = A + B\n```\nF = csc_matrix(np.random.rand(dimension, psd_rank))\nB = F @ F.T\nQ = csc_matrix(np.random.rand(dimension, dimension))\nS = Q @ Q.T + B\n```\n\n#### Construct the preconditioner\nHere we use a randomised SVD, other options include truncated SVD, the\nNyström approximation. There is support for oversampling and power iteration\nschemes.\n```\nrank_approx = 15\npc = compute_preconditioner(\n    Q,\n    B,\n    algorithm="randomized",\n    rank_approx=rank_approx,\n    n_oversamples=4,\n    n_power_iter=0,\n)\n```\n\n#### Set up a right-hand side\n\n```\nrhs = np.random.rand(dimension)\ncounter = ConjugateGradientCounter()\n```\n\n#### Solve `Sx=b` with and without a preconditioner \n```\n_, info = linalg.cg(S, rhs, callback=counter)\nprint("No preconditioner:")\nprint(f"\\t Converged: {info == 0}")\nprint(f"\\t Iterations: {counter.n_iter}\\n")\n\ncounter.reset()\n_, info = linalg.cg(S, rhs, M=rsvd_pc, callback=counter)\nprint("Randomised SVD preconditioner:")\nprint(f"\\t Converged: {info == 0}")\nprint(f"\\t Iterations: {counter.n_iter}\\n")\n```',
    'author': 'Andreas Bock',
    'author_email': 'aasbo@dtu.dk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<3.12',
}


setup(**setup_kwargs)

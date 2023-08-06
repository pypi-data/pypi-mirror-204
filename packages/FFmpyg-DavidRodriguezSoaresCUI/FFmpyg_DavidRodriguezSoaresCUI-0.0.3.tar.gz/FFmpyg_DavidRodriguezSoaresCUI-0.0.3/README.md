# [FFmpyg](https://github.com/DavidRodriguezSoaresCUI/FFmpyg) - A FFMPEG interface for Python by DavidRodriguezSoaresCUI

A library by me, for my purposes, with goals:

- Powerful: makes it easy to do complex actions
- Transparent: its power shouldn't come at the cost of losing the ability to exploit the full range of features of FFMPEG
- Specific: tailored to my needs (see PlexOptimizer)
- Self-sufficient: uses as little non-built-in libraries as possible
- Documented: has type hints and comments
- Statically tested: see `Code quality` section

While I do provide this work under a permissive license, I do not provide any guarantees of any kind, so use it at your own discretion.


## Code quality

This library was written while using [the Black formatter](https://github.com/psf/black) for PEP-8 compliance and code style consistency, a choice made to enhance source code readability. Note that the author reserves the right to locally disable Black formatting in those rare instances where manual formatting looked better in their opinion.

The code is also checked by multiple static checkers, to ensure some level of stability and runtime safety: [Mypy](https://github.com/python/mypy), [Bandit](https://github.com/PyCQA/bandit), [Pylint](https://github.com/pylint-dev/pylint), [Flake8](https://github.com/pycqa/flake8)

The author chose to exclude some rules:

- Bandit ``B404,B603``: This library uses the `subprocess` module for external calls, but commands are constructed in a way to avoid as much as possible the possibility of exploit.

- Pylint ``line-too-long, invalid-name, too-many-branches, too-many-locals, too-many-arguments, too-many-statements``: The author understands why following these rules is in general good practice, but they found them to be sometimes too constraining and chose to disregard them at their discretion.

- Flake8 `E203,E221,E501`: Either incompatible with Black or the author felt like some exceptions enhanced readability

Note: False positive warnings are typically disabled with an inline comment

A Windows script for running these modules (*with exceptions listed above*) on the source code files is provided (outputs file `analyze_code_report.txt`): `analyze_code.bat`

**Any commit/PR to master branch must pass static checks with MINIMAL amount of warnings !**
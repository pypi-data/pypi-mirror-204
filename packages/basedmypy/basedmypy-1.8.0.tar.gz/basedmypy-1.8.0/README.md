# Based  <img src="docs/source/mypy_light.svg" alt="mypy logo" width="300px"/>

[![Discord](https://img.shields.io/discord/948915247073349673?logo=discord)](https://discord.gg/7y9upqPrk2)
[![Stable Version](https://img.shields.io/pypi/v/basedmypy?color=blue)](https://pypi.org/project/basedmypy/)
[![Downloads](https://img.shields.io/pypi/dm/basedmypy)](https://pypistats.org/packages/basedmypy)
[![Checked with basedmypy](https://img.shields.io/badge/basedmypy-checked-green)](https://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

Basedmypy: Based Static Typing for Python
=========================================

What is basedmypy?
-------------
Basedmypy is a fork of mypy that adds based functionality and breaks
compatibility with the cringe parts of pep 484.

Based features include:
- Typesafe by default (optional and dynamic typing still supported)
- Baseline functionality
- Support for `Intersection` types
- Default return type of `None` instead of `Any`
- Infer parameter type from default value
- Infer overload types
- Bare literals

See the [features](#features) for a more information.

## Usage

### Installation

Basedmypy can be installed using pip from PyPI or from this GitHub repo:

    python -m pip install -U basedmypy

### Running
Basedmypy is installed as an alternative to, and in place of, the `mypy` installation:

    mypy test.py

    python -m mypy test.py

## Features

Ever tried to use pythons type system and thought to yourself "This doesn't seem based".

Well fret no longer as basedmypy got you covered!

### Baseline

Basedmypy has baseline, baseline is based! It allows you to adopt new strictness or features
without the burden of fixing up every usage, just save all current errors to the baseline
file and deal with them later.

```py
def foo(a):
    print(a)
```
```
> mypy test.py
error: missing typehints !!!!!
Epic fail bro!

> mypy --write-baseline test.py
error: missing typehints
Baseline successfully written to .mypy/baseline.json

> mypy test.py
Success: no issues found in 1 source file
```
Then on subsequent runs the existing errors will be filtered out.

```py
def foo(a):
    print(a)

def bar(b: str, c: int) -> bool:
    return b + c
```
```
> mypy test.py
test.py:4:5: error: Returning Any from function declared to return "bool"  [no-any-return]
test.py:4:16: error: Unsupported operand types for + ("str" and "int")  [operator]
Found 2 errors in 1 file (checked 1 source file)
```
### Intersection Types

Using the `&` operator or `basedtyping.Intersection` you can denote intersection types.

```py
class Growable(ABC, Generic[T]):
    @abstractmethod
    def add(self, item: T): ...

class Resettable(ABC):
    @abstractmethod
    def reset(self): ...

def f(x: Resettable & Growable[str]):
    x.reset()
    x.add("first")
```
### Type Joins

Mypy joins types like so:
```py
a: int
b: str
reveal_type(a if bool() else b)  # Revealed type is "builtins.object"
``````
Basedmypy joins types into unions instead:
```py
a: int
b: str
reveal_type(a if bool() else b)  # Revealed type is "int | str"
```
### Bare Literals

`Literal` is so cumbersome! just use a bare literal instead.

```py
class Color(Enum):
    RED = auto()

a: 1 | 2
b: True | Color.RED
```

### Default Return Type

With the `default_return` option, the default return type of functions becomes `None` instead of `Any`.

```py
def f(name: str):
    print(f"Hello, {name}!")

reveal_type(f)  # (str) -> None
```
### Nested TypeVars

With nested `TypeVar`s you are able to have functions with polymorphic generic parameters.

```py
E = TypeVar("E")
I = TypeVar("I", bound=Iterable[E])

def foo(i: I, e: E) -> I:
    assert e not in i
    return i

reveal_type(foo(["based"], "mypy"))  # N: Revealed type is "list[str]"
reveal_type(foo({1, 2}, 3))  # N: Revealed type is "set[int]"
```

### Overload Implementation Inference

Specifying types in overload implementations is completely redundant! basedmypy will infer them.

```py
@overload
def f(a: int) -> str: ...

@overload
def f(a: str) -> int: ...

def f(a):
    reveal_type(a)  # int | str
    return None  # error: expected str | int

class A:
    @property
    def foo(self) -> int: ...
    @foo.setter
    def foo(self, value): ...  # no need for annotations
```

### Infer Function Parameters

Infer the type of a function parameter from it's default value.

```py
def f(a=1, b=True):
    reveal_type((a, b))  # (int, bool)
```
### Better Types in Messages

```py
T = TypeVar("T", bound=int)

def f(a: T, b: list[str | 1 | 2]) -> Never:
    reveal_type((a, b))

reveal_type(f)
```
Mypy shows
```
Revealed type is "Tuple[T`-1, Union[builtins.str, Literal[1], Literal[2]]]"
Revealed type is "def [T <: builtins.int] (a: T`-1, b: Union[builtins.str, Literal[1], Literal[2]]) -> <nothing>"
```
Basedmypy shows
```
Revealed type is "(T@f, str | 1 | 2)"
Revealed type is "def [T: int] (a: T, b: str | 1 | 2) -> Never"
```
### Ignore Unused Type Ignores

In code that is targeting multiple versions of python or multiple platforms it is difficult
to work with `type: ignore` comments and use the `warn_unused_ignore` option.

The `unused-ignore` error code can be used for this situation.

```py
if sys.platform != "linux":
  foo()  # type: ignore[misc, unused-ignore]
```

Got a question or found a bug?
----------------------------------

Feel free to start a discussion or raise an issue, we're happy to respond:

- [basedmypy tracker](https://github.com/KotlinIsland/basedmypy/issues)
  for basedmypy issues
- [basedtypeshed tracker](https://github.com/KotlinIsland/basedtypeshed/issues)
  for issues with specific modules
- [basedtyping tracker](https://github.com/KotlinIsland/basedtyping/issues)
  for issues with the 'basedtyping' package (runtime functionality).

Readme from [python/mypy](https://github.com/python/mypy)
===========

[![Stable Version](https://img.shields.io/pypi/v/mypy?color=blue)](https://pypi.org/project/mypy/)
[![Downloads](https://img.shields.io/pypi/dm/mypy)](https://pypistats.org/packages/mypy)
[![Build Status](https://github.com/python/mypy/actions/workflows/test.yml/badge.svg)](https://github.com/python/mypy/actions)
[![Documentation Status](https://readthedocs.org/projects/mypy/badge/?version=latest)](https://mypy.readthedocs.io/en/latest/?badge=latest)
[![Chat at https://gitter.im/python/typing](https://badges.gitter.im/python/typing.svg)](https://gitter.im/python/typing?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

Got a question?
---------------

We are always happy to answer questions! Here are some good places to ask them:

- for anything you're curious about, try [gitter chat](https://gitter.im/python/typing)
- for general questions about Python typing, try [typing discussions](https://github.com/python/typing/discussions)

If you're just getting started,
[the documentation](https://mypy.readthedocs.io/en/stable/index.html)
and [type hints cheat sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)
can also help answer questions.

If you think you've found a bug:

- check our [common issues page](https://mypy.readthedocs.io/en/stable/common_issues.html)
- search our [issue tracker](https://github.com/python/mypy/issues) to see if
  it's already been reported
- consider asking on [gitter chat](https://gitter.im/python/typing)

To report a bug or request an enhancement:

- report at [our issue tracker](https://github.com/python/mypy/issues)
- if the issue is with a specific library or function, consider reporting it at
  [typeshed tracker](https://github.com/python/typeshed/issues) or the issue
  tracker for that library

To discuss a new type system feature:
- discuss at [typing-sig mailing list](https://mail.python.org/archives/list/typing-sig@python.org/)
- there is also some historical discussion [here](https://github.com/python/typing/issues)


What is mypy?
-------------

Mypy is a static type checker for Python.

Type checkers help ensure that you're using variables and functions in your code
correctly. With mypy, add type hints ([PEP 484](https://www.python.org/dev/peps/pep-0484/))
to your Python programs, and mypy will warn you when you use those types
incorrectly.

Python is a dynamic language, so usually you'll only see errors in your code
when you attempt to run it. Mypy is a *static* checker, so it finds bugs
in your programs without even running them!

Here is a small example to whet your appetite:

```python
number = input("What is your favourite number?")
print("It is", number + 1)  # error: Unsupported operand types for + ("str" and "int")
```

Adding type hints for mypy does not interfere with the way your program would
otherwise run. Think of type hints as similar to comments! You can always use
the Python interpreter to run your code, even if mypy reports errors.

Mypy is designed with gradual typing in mind. This means you can add type
hints to your code base slowly and that you can always fall back to dynamic
typing when static typing is not convenient.

Mypy has a powerful and easy-to-use type system, supporting features such as
type inference, generics, callable types, tuple types, union types,
structural subtyping and more. Using mypy will make your programs easier to
understand, debug, and maintain.

See [the documentation](https://mypy.readthedocs.io/en/stable/index.html) for
more examples and information.

In particular, see:
- [type hints cheat sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)
- [getting started](https://mypy.readthedocs.io/en/stable/getting_started.html)
- [list of error codes](https://mypy.readthedocs.io/en/stable/error_code_list.html)

Quick start
-----------

Mypy can be installed using pip:

    python3 -m pip install -U mypy

If you want to run the latest version of the code, you can install from the
repo directly:

    python3 -m pip install -U git+https://github.com/python/mypy.git
    # or if you don't have 'git' installed
    python3 -m pip install -U https://github.com/python/mypy/zipball/master

Now you can type-check the [statically typed parts] of a program like this:

    mypy PROGRAM

You can always use the Python interpreter to run your statically typed
programs, even if mypy reports type errors:

    python3 PROGRAM

You can also try mypy in an [online playground](https://mypy-play.net/) (developed by
Yusuke Miyazaki). If you are working with large code bases, you can run mypy in
[daemon mode], that will give much faster (often sub-second) incremental updates:

    dmypy run -- PROGRAM

[statically typed parts]: https://mypy.readthedocs.io/en/latest/getting_started.html#function-signatures-and-dynamic-vs-static-typing
[daemon mode]: https://mypy.readthedocs.io/en/stable/mypy_daemon.html


Integrations
------------

Mypy can be integrated into popular IDEs:

* Vim:
  * Using [Syntastic](https://github.com/vim-syntastic/syntastic): in `~/.vimrc` add
    `let g:syntastic_python_checkers=['mypy']`
  * Using [ALE](https://github.com/dense-analysis/ale): should be enabled by default when `mypy` is installed,
    or can be explicitly enabled by adding `let b:ale_linters = ['mypy']` in `~/vim/ftplugin/python.vim`
* Emacs: using [Flycheck](https://github.com/flycheck/)
* Sublime Text: [SublimeLinter-contrib-mypy](https://github.com/fredcallaway/SublimeLinter-contrib-mypy)
* Atom: [linter-mypy](https://atom.io/packages/linter-mypy)
* PyCharm: [mypy plugin](https://github.com/dropbox/mypy-PyCharm-plugin) (PyCharm integrates
  [its own implementation](https://www.jetbrains.com/help/pycharm/type-hinting-in-product.html) of [PEP 484](https://peps.python.org/pep-0484/))
* VS Code: provides [basic integration](https://code.visualstudio.com/docs/python/linting#_mypy) with mypy.
* pre-commit: use [pre-commit mirrors-mypy](https://github.com/pre-commit/mirrors-mypy).

Web site and documentation
--------------------------

Additional information is available at the web site:

  http://www.mypy-lang.org/

Jump straight to the documentation:

  https://mypy.readthedocs.io/

Follow along our changelog at:

  https://mypy-lang.blogspot.com/


Contributing
------------

Help in testing, development, documentation and other tasks is
highly appreciated and useful to the project. There are tasks for
contributors of all experience levels.

To get started with developing mypy, see [CONTRIBUTING.md](CONTRIBUTING.md).

If you need help getting started, don't hesitate to ask on [gitter](https://gitter.im/python/typing).


Mypyc and compiled version of mypy
----------------------------------

[Mypyc](https://github.com/mypyc/mypyc) uses Python type hints to compile Python
modules to faster C extensions. Mypy is itself compiled using mypyc: this makes
mypy approximately 4 times faster than if interpreted!

To install an interpreted mypy instead, use:

    python3 -m pip install --no-binary mypy -U mypy

To use a compiled version of a development
version of mypy, directly install a binary from
https://github.com/mypyc/mypy_mypyc-wheels/releases/latest.

To contribute to the mypyc project, check out https://github.com/mypyc/mypyc

# The Tex Programming Language

<img src="Tex_Logo.png" alt="Tex Logo" width="200"/>

![GitHub last commit](https://img.shields.io/github/last-commit/Visual-mov/Tex-lang)

Tex is a general-purpose dynamically-typed toy language written in Python. Tex's main goal is to be my first language and an exercise. As such, it's very simplistic and finicky. All planned features haven't been implemented yet, see *TODO* for the list.

To start programming in Tex, check out the [Tex Reference](doc/Tex-reference.md)

## Getting Started
Clone repo
```
~$ git clone https://github.com/Visual-mov/Tex-lang
~$ cd Tex-lang/src
```

The Tex Language includes a REPL for executing Tex code directly.
```
~$ python3 repl.py
```
You can also run a Tex program in the form of a file. Specify the location of the file with "--file"
```
~$ python3 repl.py --file [path]
```
You can save Tex programs as files with the '.tx' extension.

## TODO
- Implement context system ✔️
- Add 'continue' and 'break' keywords ✔️
- Allow multiple Strings and Floats to be added together (Compound strings) ✔️
- Allow for variable names to include numbers.
- Fix line number for "Expected 'end' token" exception.
- Add user-defined functions.
- Add built-in functions for math, and input.

## Project Status
At this time, Tex is still in active development. I'm planning on continuing its development intermittently until February 2020 or so.


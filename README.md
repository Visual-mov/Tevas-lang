# The Tex Programming Language

<img src="Tex_Logo.png" alt="Tex Logo" width="200"/>

Tex is a general-purpose dynamically-typed toy language written in Python. Tex's main goal exercise in demonstrating key programming concepts, such as control flow and variables. It's the first language I've ever written, and as such it's very simplistic and finicky.

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
- Add 'continue' and 'break' keywords ✔️
- Allow multiple Strings and Floats to be added together (Compound strings) ✔️
- Allow for variable names to include numbers. ✔️
- Fix line number for "Expected 'end' token" exception.
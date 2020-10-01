# The Tevas Programming Language Reference
## REPL
The Tevas REPL takes in Tevas code one line at a time. It will print the evaluated value of any expression entered into it. For example:
```
>> 2 + 2 = 4
true
>> (400 - 399)/2
0.5
>> "Hello" + " world!"
Hello world!
>>
```

## Syntax
Tevas is a dynamically typed language. A variable's type does not need to be declared in assignment. All the type checking is done in runtime. Tevas is not sensitive to indention (spaces and tabs) and line breaks. Line breaks are not tokenized, meaning Tevas has no concept of them within the parser. This makes the syntax very "loose" feeling.
Each one of these strings is a valid Tevas program.

` 2 -> a 2 -> b println a * b`

```
           0 -> i 
       while[i 
             < 10]:
println i         i + 1 -> i
            end
```
Expressions and assignments can even be declared on multiple lines! :O Isn't that crazy!
```
false
||
true &&

true
->
myVar
```

## Comments
Comments are signified in Tevas with the tilde character, '~'. All characters after the tilde on the same line will be ignored.
```
~ This is my program!
println "Hello World"
```
Comments can also come after tokens on the same line.

`2 + 2 -> a  ~ Sets a equal to 4.`

## Variables
To declare a variable, use the store/assignment (->) operator. The expression on the left operand is the value to be stored, while the identifier is on the right. Identifiers can contain numbers, however they can't start with them.

```
2 * (2 + 2) -> a
(8.6 * 10.44) / 65 + 2 % 2.5 -> c
true -> d
```

### *Types*
Tevas has 3 different types: Float, String, and Boolean. All type checking is done at runtime.

#### Float
Floats represent numbers in Tevas. There is no "integer" type in Tevas.
```
5.5 + 2.9 -> myVar
23 - 4 -> myVar2
```

#### String
Strings are defined as being multiple characters between two double quotes. Strings can span multiple lines, however newline characters will be included.
```
"Foo!" -> myString
"Bar!" -> myString2
```

Compound Strings can be formed by adding multiple Strings together, or combining Strings with Floats. If a String is combined Boolean, it will result in a type conflict however. Like every other expression, compound Strings are evaluated from left to right. This means the expression `2 + 2 + " = 4"` would be evaluated to `"4.0 = 4"`, as `2 + 2` is first evaluated as an arithmetical expression, and is then turned into a compound String when added to the string `" = 4"`

```
"Lo" + "gin" -> myString
100 + " many iterations!" -> myString2
(100 + 100) / 50 + " is equal to 4." -> myString3
```

#### Boolean
Booleans can have only one of two values, those being *true* or *false*. Only logical and comparison operations can be performed on booleans, which will evaluate to a boolean.
```
true -> myBool
false -> myBool2
myBool = myBool2 -> myBool3
```

## Control Structures
### *Check*
The if/else control structure checks whether a given expression is true, and subsequently executes or skips the following block statement. Zero or more *celse* (check-else) statements can follow a *check* statement, which will be evaluated if the *check* statement fails. If these all evaluate to false, the optional *else* block will be executed.
The given expression must evaluate to a boolean value. Expressions that evaluate to any other type are invalid.

```
check[expr]:
  ...statements
end
celse[expr]:
  ...statements
end
else:
  ...statements
end
```
```
check[string = "Yes"]:
  println "You said yes!"
end
celse[string = "No"]:
  println "You said no!"
end
else:
  println "You didn't say yes or no!"
end
```

### *While*
The while control structure continues to execute all statements within it until the given expression is false. While is the only loop/repetition structure that exists in Tevas.

```
while[expr]:
  ...statements
end
```
```
0 -> i
while[i < 10]:
  print i
  println " iterations"
  i + 1 -> i
end
```

*continue* and *break* keywords allow you to control a loop's execution. *break* allows you to break out of the given loop, and continue execution. While *continue* returns the execution to the beginning of the loop, as well as re-evaluating the exit condition.

#### Break
```
0 -> i
while[i < 5]:
  println i
  check[i = 3]: break end
  i + 1 -> i
end
```

```
Expected output:
0.0
1.0
2.0
3.0
```

#### Continue
```
0 -> i
while[i < 5]:
  println i
  check[i = 3]: continue end
  i + 1 -> i
end
```

```
Expected output:
0.0
1.0
2.0
3.0
3.0
3.0
3.0
...
```

## Other Statements
### *Print*
Prints a given expression / variable using stdout.

```
print "Hello World!"

Output: Hello World!
```


### *Println*
Same functionality as *print* statement, but appends a new-line character at the end of the value.

```
println "Hello World!"

Output: Hello World!\n
```

## Expressions
There exists three types of expressions in Tevas, logical, arithmetical and compound Strings.

### *Binary Operators*
#### Logical Operators
```
= : Comparative equals (Is equal to)
!= : Comparative not equals (Is not equal to)
&& : Logical AND
|| : Logical OR

< : Less than
> : Greater than
<= : Less than or equal to
>= : Greater than or equal to
```
#### Arithmetical Operators
```
- : Subtract
+ : Add (Also used for compound Strings)
* : Multiply
/ : Divide
% : Modulo
```

### *Unary Operators*
```
- : Negative Float
+ : Positive Float
! : Logical NOT
```

## Keywords
- *while* - While loop control structure
- *continue* - Continue statement
- *break* - Break statement
- *check* - If/else control structure
- *celse* - Optional of else-if block following if
- *else* - Optional else block following if
- *end* - Ends block statement
- *print* - Print statement
- *println* - Println statement
- *true* - Logical true
- *false* - Logical false
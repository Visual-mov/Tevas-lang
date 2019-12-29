# The Tex Programming Language Reference

## Comments
Comments are signified in Tex with the tilde character, '~'. All tokens after the tilde on the same line will be ignored.
```
~ This is my program!
println "Hello World"
```
Comments can also come after tokens on the same line.
```
2 + 2 -> a  ~ Sets a equal to 4.
```
## Variables
To declare a variable, use the store/assignment (->) operator. The expression on the left operand is the value to be stored, while the token on the right operand is the variable identifier.

```
2 * (2 + 2) -> a
(8.6 * 10.44) / 65 + myFunc(a) -> c
true -> d
```

### *Types*
Tex has 3 different types: Float, String, and Boolean. All type checking is done at runtime.

*Float* - Floats represent both floating-point numbers as well as integers in Tex.
```
5.5 + 2.9 -> myVar
23 - 4 -> myVar2
```

*String* - A String is a defined as being multiple between two double quotes. Strings can not span multiple lines.
```
"Foo" -> myString
"Foo" + "bar: " + val -> myString2
```

*Boolean* - Booleans can have only one of two values, those being *true* or *false*. Only logical and comparison operations can be performed on booleans, which will evaluate to either *true* or *false*. In this case, myBool3 is equal to false.
```
true -> myBool
false -> myBool2
myBool = myBool2 -> myBool3
```

## Control Structures

### *Check*
The if/else control structure checks whether a given expression is true, and subsequently executes or skips the following block statement to execute the optional *else* block. Zero or more *celse* (check-else) blocks can follow a *check* block, which will be evaluated if the *check* block fails. This structure is implemented in the Tex language with the the keywords *check*, *celse*, and *else*. 
The given expression must evaluate to either true, or false. Expressions that evaluate to any other type are invalid.

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
check[a = b]:
  println "a is equal to b!"
end
celse[a > b]:
  println "a is larger than b!"
end
celse[a < b]:
  println "a is less than b!"
end
else:
  println "Hold on, a is not equal to b!"
end
```

### *While*
The while control structure continues to execute its block statement until the given expression evaluates to false. While is the only loop/repetition structure that exists in Tex.

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
## Other Statements

### *Print*
Prints a given Float, Boolean, or String using stdout.

```
"Hello World!" -> myString
print myString
```
```
Output: Hello World!
```


### *Println*
Same functionality as *print* statement, but appends a new-line character at the end of the given value.

```
"Hello World!" -> myString
print myString
```
```
Output: Hello World!\n
```

## Expressions
There exists two types of expressions in Tex, logical and arithmetical.

### *Binary Operators*

#### Logical Operators
```
= : Comparative equals (Is equal to)
!= : Comparative not equals (Is not equal to)
< : Less than.
> : Greater than.
<= : Less than or equal to.
>= : Greater than or equal to.
&& : Logical AND
|| : Logical OR
```
#### Arithmetical Operators
```
- : Subtract.
+ : Add.
* : Multiply.
/ : Divide.
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
- *check* - If/else control structure
- *celse* - Optional of else-if block following if.
- *else* - Optional else block following if.
- *end* - Ends block statement.
- *print* - Print statement
- *println* - Println statement
- *true* - Logical true
- *false* - Logical false
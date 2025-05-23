# Math_Compiler

# EBNF

```
FUNC_BLOCK    = "def" IDENTIFIER "(" [ PARAMS ] ")" ":" BLOCK ;
BLOCK         = "{" "\n" { STATEMENT } "}" ;
STATEMENT     = ( ASSIGN
                | IF
                | RETURN
                | WHILE
                ) "\n" ;
ASSIGN        = IDENTIFIER "=" EXPR ;
RETURN        = "return" EXPR ;
IF            = "if" "(" BIEXPRESSION ")" ":" BLOCK [ "else" ":" BLOCK ] ;
WHILE         = "while" "(" BIEXPRESSION ")" ":" BLOCK ;
PARAMS        = IDENTIFIER { "," IDENTIFIER } ;
  
EXPR          = TERM { ("+" | "-") TERM } ;
TERM          = FACT { ("*" | "/") FACT } ;
FACT          = NUMBER
              | IDENTIFIER [ "(" [ ARG ] ")" ]
              | "(" EXPR ")"
              | "sqrt" "(" EXPR ")"
              | SUM
              | EXPR "^" NUMBER ;
SUM           = "sum" "(" EXPR "," EXPR "," EXPR "," EXPR ")" ;
ARG           = EXPR { "," EXPR } ;
  
BIEXPRESSION  = BITERM { "or" BITERM } ;
BITERM        = RELEXPRESSION { "and" RELEXPRESSION } ;
RELEXPRESSION = EXPR { ("==" | "!=" | "<" | ">" | "<=" | ">=") EXPR } ;
  
IDENTIFIER    = LETTER { LETTER | DIGIT | "_" } ;
NUMBER        = DIGIT { DIGIT } ;
LETTER        = "a" | … | "z" | "A" | … | "Z" ;
DIGIT         = "0" | … | "9" ;

```

## Exemplos

### 1

```
x = 5 + 3  
```

$$ x = 5 + 3 $$

### 2

```
7 * (2 + 1) 
```

$$7 \times (2 + 1)$$

### 3

```
def sq(x): {
    return x * x
}
```

$$\mathrm{sq}(x) = x^{2}$$

### 4

```
def root(x): {
    return sqrt(x)
}
```

$$\mathrm{root}(x) = \sqrt{x}$$

### 5

```
if (x < 0): {
y = -x
} else: {
y = x
}
```

$$y =
\begin{cases}
  -x, & x < 0,\\
  x,  & \text{caso contrário.}
\end{cases}$$

### 6.
```
def sum1(n): {
    return sum(i,1,n,i)
    }
```
$$ \mathrm{sum1}(n)=\sum_{i=1}^{n}i$$

### 7.
```
def sumsq(n):{
    return sum(i,1,n,i*i)
}
```
$$ \mathrm{sumsq}(n)=\sum_{i=1}^{n}i^{2}$$

### 8.
```
x = 0
while (x < 3): {
  x = x + 1
}
```
$$ x = 0,\quad
\text{enquanto }x<3:\;x \leftarrow x + 1$$

### 9.
```
def incr(n): {
  return n + 1
}
```

$$\mathrm{incr}(n) = n + 1$$
### 10.
```
def fact(n): {
  if (n <= 1): {
    return 1
  } else: {
    return n * fact(n - 1)
  }
}
```
$$ \mathrm{fact}(n) =
\begin{cases}
  1, & n \le 1,\\
  n \times \mathrm{fact}(n-1), & \text{caso contrário.}
\end{cases}$$
### 11.
```
def fib(n): {
  if (n <= 1): {
    return n
  } else: {
    return fib(n - 1) + fib(n - 2)
  }
}
```
$$ \mathrm{fib}(n) =
\begin{cases}
  n, & n \le 1,\\
  \mathrm{fib}(n-1) + \mathrm{fib}(n-2), & \text{caso contrário.}
\end{cases}$$

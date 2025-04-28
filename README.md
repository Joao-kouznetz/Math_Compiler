# Math_Compiler

# EBNF

```
RELEXPRESSION = EXPRESSION, [ ("=" | ">" | "<" | "∈" | "∉" | "→"), EXPRESSION ] ;
EXPRESSION = TERM, { ("+" | "-"), TERM } ;
TERM = POTERM, { ("*" | "/"), POTERM } ;
POTERM = FACTOR, [ ("**", "^"), FACTOR ] ;
FACTOR = IDENT | INT | ("+" | "-"), FACTOR | "(", RELEXPRESSION, ")" ;
INT = DIGIT, { DIGIT } ;
IDENT = LETTER, { LETTER | DIGIT } ;
DIGIT = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
LETTER = "a" | ... | "z" | "A" | ... | "Z" ;

```

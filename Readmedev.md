# como compilar

```zsh
bison -d lan.y 

flex lan.l 

gcc -o myparser lan.tab.c lex.yy.c  -Wall
```

## testando

```zsh
./myparser < exemplo.txt
```

```zsh
```

```zsh
```

```zsh
```

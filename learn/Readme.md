# Comando para compilar o tokenizer

``` zsh
flex -t words.l > tokenizer.c                                                    ✔ 
cc -c tokenizer.c
```

# COmnado para testar o tokenizer

```zsh
cc -o test_tokenizer test_tokenizer.c tokenizer.o 
```

```zsh
./test_tokenizer
```

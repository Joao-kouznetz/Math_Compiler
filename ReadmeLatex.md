# Sobre latex

começa com $ e termina com $

superscripts $1^{2}$ subscripts $1_{2}$

operadores:

- $\sin$
- $\cos$
- $\tan$
- $\ln$
- $\log_{10}$
- $\exp$
- $\sqrt{3}$
- $\pi$
- $\theta$
- $\times$
- $\div$
- $\infty$
- $\leq$
- $\geq$
- $\neq$
- $\approx$
- $\mid$
- $\parallel$
- $\perp$
- $\cup$
- $\cap$
- $\setminus$
- $\subseteq$
- $\supseteq$
- $\subset$
- $\supset$
- $\in$
- $\notin$
- $\exists$
- $\forall$
- $\mathbb{R}$
- $\mathbb{N}$
- $\mathbb{Z}$

# Coisas que precisa ter

```
𝑀 = (𝑄, Σ, 𝛿, 𝑞0, 𝐹 )
𝛿 ∶ 𝑄 × Σ → 𝑄
𝑞0 ∈ 𝑄
𝐹 ⊆ 𝑄
𝐿 = {𝑎ℎ𝑛0 (𝑏ℎ𝑛𝑖 )𝑚𝑐|𝑛0 ≥ 1, 𝑛𝑖 ≥ 1, 𝑖 ≥ 1, 𝑚 ≥ 0}
𝑦 ≠ 𝜆
|𝑥𝑦| ≤ 𝑛

lim 𝑥→10+ 𝑉(𝑥) = 𝟒0
𝑓(𝑥) = 𝑥^2−1 / 𝑥−1
𝑑𝑇/𝑑𝑡 = −𝑘(𝑇 − 𝑇𝑎𝑚𝑏)

∫ 𝑓(𝑦) 𝑑𝑦 e ∫ 𝑔(𝑥) 𝑑x

𝐶=[[-1, 2],[3,1]]   #Matriz

```

# Minha Latex

```
ASSIGNMENT = (IDENTIFIER | NUMBER), "=", BIEXPRESSION ;
BIEXPRESSION = BITERM, { "||" , BITERM  } ;
BITERM = RELEXPRESSION, { "&&" , RELEXPRESSION }
RELEXPRESSION = EXPRESSION, { ("==" | ">" | "<"), EXPRESSION } ;
EXPRESSION = TERM, { ("+" | "-"), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = (NUMBER | IDENTIFIER  ("+" | "-" ), FACTOR) |  "(", FACTOR, ")"  ;
IDENTIFIER = LETTER, { LETTER | DIGIT  } ;
NUMBER = DIGIT, { DIGIT } ;
LETTER = ( a | ... | z | A | ... | Z ) ;
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;

```

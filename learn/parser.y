%{
\#include \<stdio.h>
\#include \<stdlib.h>
\#include \<string.h>

/\* Prototipo do yylex fornecido pelo Flex \*/
extern int yylex();
extern int yylineno;
void yyerror(const char \*s) {
fprintf(stderr, "Erro de sintaxe: %s na linha %d\n", s, yylineno);
}
%}


%token T_DEF T_RETURN T_IF T_ELSE T_WHILE
%token T_SUM T_SQRT T_AND T_OR
%token T_EQ T_NE T_LE T_GE T_LT T_GT
%token T_ASSIGN T_PLUS T_MINUS T_TIMES T_DIV T_POW
%token T_LPAREN T_RPAREN T_LBRACE T_RBRACE T_COLON T_COMMA
%token T_IDENT T_NUMBER T_NEWLINE


%left T_OR
%left T_AND
%nonassoc T_EQ T_NE
%nonassoc T_LT T_LE T_GT T_GE
%left T_PLUS T_MINUS
%left T_TIMES T_DIV
%right T_POW

%%

program:

\| program stmt
;

stmt:
T\_IDENT T\_ASSIGN expr T\_NEWLINE      { printf("$%s = %s$\n", \$1, \$3); free(\$1); free(\$3); }
\| T\_DEF T\_IDENT T\_LPAREN opt\_params T\_RPAREN T\_COLON block  { /\* Função */ }
\| T\_IF T\_LPAREN expr T\_RPAREN T\_COLON block opt\_else      { /* if/else */ }
\| T\_WHILE T\_LPAREN expr T\_RPAREN T\_COLON block T\_NEWLINE  { /* while \*/ }
;

opt\_params:
/\* vazio */       { \$\$ = NULL; }
\| params             { /* lista de parâmetros \*/ }
;

params:
T\_IDENT           { /\* primeiro param */ }
\| params T\_COMMA T\_IDENT  { /* parâmetros adicionais \*/ }
;

opt\_else:
/\* vazio */               { /* sem else */ }
\| T\_ELSE T\_COLON block      { /* bloco else \*/ }
;

block:
T\_LBRACE T\_NEWLINE stmts T\_RBRACE T\_NEWLINE
;

stmts:
/\* vazio \*/
\| stmts stmt
;

expr:
term                              { \$\$ = \$1; }
\| expr T\_PLUS term                 { /\* soma */ }
\| expr T\_MINUS term                { /* subtração \*/ }
;

term:
factor                            { \$\$ = \$1; }
\| term T\_TIMES factor               { /\* multiplicação */ }
\| term T\_DIV factor                 { /* divisão \*/ }
;

factor:
T\_NUMBER                          { /\* número */ }
\| T\_IDENT opt\_args                  { /* chamada de função */ }
\| T\_LPAREN expr T\_RPAREN            { \$\$ = \$2; }
\| T\_SQRT T\_LPAREN expr T\_RPAREN     { /* raiz */ }
\| T\_SUM T\_LPAREN expr T\_COMMA expr T\_COMMA expr T\_COMMA expr T\_RPAREN  { /* sum(i,a,b,expr) */ }
\| factor T\_POW T\_NUMBER             { /* exponenciação \*/ }
;

opt\_args:
/\* vazio */                       { /* sem args */ }
\| T\_LPAREN args T\_RPAREN            { /* lista de args \*/ }
;

args:
expr                              { /\* 1 arg */ }
\| args T\_COMMA expr                 { /* múltiplos args \*/ }
;

%%

int main(void) {
return yyparse();
}

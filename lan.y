/* lan.y — Parser Bison para a toy language */

%{
#include <stdio.h>
#include <stdlib.h>
int   yylex(void);
void  yyerror(const char *s);
%}

/* valor semântico */
%union {
  int    num;
  char  *str;
}

/* tokens do Flex */
%token <str> T_IDENT
%token <num> T_NUMBER
%token       T_DEF T_RETURN T_IF T_ELSE T_WHILE T_SUM T_SQRT
%token       T_LE T_GE T_EQ T_NE
%token       NEWLINE

%left '+' '-'
%left '*' '/'
%right '^'

%%

/* programa = zero ou mais top_items que terminam em NEWLINE */
program:
    /* vazio */
  | program top_item NEWLINE
  | program top_item        /* <-- permite fechar sem \n final */
  ;


top_item:
    statement
  | FUNC_BLOCK
  ;
/* STATEMENT de topo */
statement:
    ASSIGN
  | RETURN
  | IF
  | WHILE
  ;

/* bloco de função exigido em {} seguido de NEWLINE */
FUNC_BLOCK:
    T_DEF T_IDENT '(' opt_params ')' ':' BLOCK
  ;
/* 2 Regra auxiliar para opcionalizar um \n */
opt_nl:
    /* vazio */
  | NEWLINE
  ;
  
/* blocos em chaves, com pelo menos um \n antes de statements */
BLOCK:
    '{' NEWLINE stmt_list '}'  opt_nl
  ;

/* lista de statements, aceita zero ou mais */
stmt_list:
    /* vazio */
  | stmt_list statement NEWLINE
  ;

/* statements internos */
ASSIGN:
    T_IDENT '=' EXPR
  ;

RETURN:
    T_RETURN EXPR
  ;

IF:
    T_IF '(' EXPR ')' ':' BLOCK opt_else
  ;

opt_else:
    /* vazio */
  | T_ELSE ':' BLOCK
  ;

WHILE:
    T_WHILE '(' EXPR ')' ':' BLOCK
  ;

/* parâmetros opcionais */
opt_params:
    /* vazio */
  | PARAMS
  ;
PARAMS:
    T_IDENT
  | PARAMS ',' T_IDENT
  ;

/* expressões aritméticas */
EXPR:
    EXPR '+' TERM
  | EXPR '-' TERM
  | TERM
  ;

TERM:
    TERM '*' FACT
  | TERM '/' FACT
  | FACT
  ;

/* FACT agora inclui sum e sqrt */
FACT:
    T_NUMBER
  | T_IDENT
  | T_IDENT '(' opt_args ')'      /* chamada genérica */
  | '(' EXPR ')'
  | T_SQRT '(' EXPR ')'
  | T_SUM '(' T_IDENT ',' EXPR ',' EXPR ',' EXPR ')'  /* sum(i,a,b,EXPR) */
  | EXPR '^' T_NUMBER
  ;

/* args de chamadas */
opt_args:
    /* vazio */
  | ARG_LIST
  ;
ARG_LIST:
    EXPR
  | ARG_LIST ',' EXPR
  ;

%%

int main(void) {
    return yyparse();
}

void yyerror(const char *s) {
    fprintf(stderr, "Erro sintático: %s\n", s);
    exit(1);
}

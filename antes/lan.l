/* lan.l — Lexer Flex para a toy language */

%option noyywrap

%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "lan.tab.h"    /* tokens gerados pelo Bison */
extern YYSTYPE yylval;
%}

/* Definições auxiliares */
LETTER   [A-Za-z]
DIGIT    [0-9]

%%

[ \t\r]+                       ;   /* ignora espaços e tabs */
\n                             return NEWLINE;
"/\\*([^*]*\\*+([^*/][^*]*\\*+)*)?/"  ;   /* ignora /* ... */ 
"//".*                         ;   /* ignora // ... */

"def"                          return T_DEF;
"return"                       return T_RETURN;
"if"                           return T_IF;
"else"                         return T_ELSE;
"while"                        return T_WHILE;
"sum"                          return T_SUM;
"sqrt"                         return T_SQRT;
"and"                          return T_AND;
"or"                           return T_OR;

"<="                           return T_LE;
">="                           return T_GE;
"=="                           return T_EQ;
"!="                           return T_NE;

"<"                            return '<';
">"                            return '>';
"="                            return '=';
"+"                            return '+';
"-"                            return '-';
"*"                            return '*';
"/"                            return '/';
"^"                            return '^';
"("                            return '(';
")"                            return ')';
"{"                            return '{';
"}"                            return '}';
":"                            return ':';
","                            return ',';

{LETTER}({LETTER}|{DIGIT}|_)*  {
                                  yylval.str = strdup(yytext);
                                  return T_IDENT;
                               }
{DIGIT}+                        {
                                  yylval.num = atoi(yytext);
                                  return T_NUMBER;
                               }

.                               {
                                  fprintf(stderr, "Erro léxico: `%s`\n", yytext);
                                  exit(1);
                               }
%%

/* words.l */

/* relacionando palavras com numero para facilitar retorno do flex */
%{
#include "tokens.h"
#include <stdio.h> // Para fprintf
%}

/* don't generate functions we don't need */
%option nounput noinput noyywrap

/* generate a scanner that's thread safe */
%option reentrant

/* Generate "token" rather than "yy" as a prefix, e.g.
   wordslex() rather than yylex(). This allows multiple
   Flex scanners to be linked with the same application */
%option prefix="token"

%%

"("             { return OPEN_PAR; }
")"             { return CLOSE_PAR;}
"{"             { return OPEN_BRA; }
"}"             { return CLOSE_BRA; }
"while"         { return WHILE; }
"for"           { return FOR; }
"["             { return OPEN_COL; }
"]"             { return CLOSE_COL; }
":"             { return COLON; }
","             { return COMMA; }
"**"            { return POT; }
"*"             { return TIMES; }
"/"             { return DIVIDED; }
"+"             { return PLUS; }  // Adicionado
"-"             { return MINUS; } // Adicionado
"=="            { return EQUAL_EQUAL; }
"="             { return EQUAL; }
"!="            { return NOT_EQUAL; }
"<"             { return LESS; }
">"             { return GREATER; }
"%"             { return PERCENT; }
"^"             { return CIRCUMFLEX; }
"def"           { return DEF;     }

[0-9]+          { return NUM; }
[A-Za-z_][A-Za-z0-9_]* { return IDENT; }

[ \t\r]+        ; /* Ignora espaços em branco */
\n              { return NEWLINE; }

.               {
                  /* imprime no stderr e retorna um token de erro */
                  fprintf(stderr,
                          "Invalid character: '%s'\n",
                          tokenget_text(yyscanner));
                  return ERROR;
                }

%%

/* Callers interact with this function, which neatly hides
   the Flex inside.

   Also, we'll call "yy" functions like "yylex()" inside,
   and Flex will rename them in the resulting C file to
   calls with the "words" prefix, like "wordslex()"

   Zero return means success, nonzero is a Flex error
   code. */

int token_callback(char *s, void (*f)(const char *, const char *))
{
    yyscan_t scanner;
    YY_BUFFER_STATE buf;
    int tok;

    if ((tok = tokenlex_init(&scanner))) return tok;
    buf = token_scan_string(s, scanner);

    while ((tok = tokenlex(scanner)) > 0) {
        const char *name = token_names[tok];
        f(name, tokenget_text(scanner));
    }

    token_delete_buffer(buf, scanner);
    tokenlex_destroy(scanner);
    return 0;
}

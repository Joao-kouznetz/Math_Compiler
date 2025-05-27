// tokens.h
#ifndef TOKENS_H
#define TOKENS_H

// liste aqui **só uma vez** todos os tokens:
#define TOKEN_LIST \
  X(ERROR)   \
  X(IDENT)        \
  X(NUM)          \
  X(OPEN_PAR)     \
  X(CLOSE_PAR)    \
  X(OPEN_BRA)     \
  X(CLOSE_BRA)    \
  X(WHILE)        \
  X(FOR)          \
  X(OPEN_COL)     \
  X(CLOSE_COL)    \
  X(COLON)        \
  X(COMMA)        \
  X(PLUS)         \
  X(MINUS)        \
  X(TIMES)        \
  X(POT)          \
  X(DIVIDED)      \
  X(LESS)         \
  X(GREATER)      \
  X(EQUAL)        \
  X(EQUAL_EQUAL)  \
  X(PERCENT)      \
  X(NOT_EQUAL)    \
  X(CIRCUMFLEX)   \
  X(NEWLINE)

// gera o enum
typedef enum {
#define X(name) name,
    TOKEN_LIST
#undef X
} TokenType;

// gera o array de strings
static const char* token_names[] = {
#define X(name) [name] = #name,
  TOKEN_LIST
#undef X
};

#undef TOKEN_LIST
#endif // TOKENS_H
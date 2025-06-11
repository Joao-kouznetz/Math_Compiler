/* lan.y — Parser Bison para a toy language */

%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int yylex(void);
void yyerror(const char *s);

// Definição da AST
typedef enum {
  EXPR_BINOP, EXPR_NUM, EXPR_IDENT, EXPR_CALL, EXPR_POW,
  STMT_ASSIGN, STMT_RETURN, STMT_IF, STMT_WHILE, STMT_BLOCK, STMT_FUNC
} NodeType;

typedef struct Expr Expr;
typedef struct Stmt Stmt;
typedef struct ExprList ExprList;
typedef struct StmtList StmtList;

struct ExprList {
  Expr *expr;
  ExprList *next;
};

struct StmtList {
  Stmt *stmt;
  StmtList *next;
};

struct Expr {
  NodeType kind;
  union {
    struct { char op; Expr *left, *right; } binop;
    int num;
    char *ident;
    struct { char *name; ExprList *args; } call;
    struct { Expr *base; int exp; } pow;
  } u;
};

struct Stmt {
  NodeType kind;
  union {
    struct { char *name; Expr *expr; } assign;
    Expr *ret_expr;
    struct { Expr *cond; Stmt *then_branch; Stmt *else_branch; } if_stmt;
    struct { Expr *cond; Stmt *body; } while_stmt;
    StmtList *block;
    struct { char *name; char **params; int param_count; Stmt *body; } func;
  } u;
};

Expr *make_binop(char op, Expr *left, Expr *right) {
  Expr *e = malloc(sizeof(Expr));
  e->kind = EXPR_BINOP;
  e->u.binop.op = op;
  e->u.binop.left = left;
  e->u.binop.right = right;
  return e;
}

Expr *make_num(int num) {
  Expr *e = malloc(sizeof(Expr));
  e->kind = EXPR_NUM;
  e->u.num = num;
  return e;
}

Expr *make_ident(char *name) {
  Expr *e = malloc(sizeof(Expr));
  e->kind = EXPR_IDENT;
  e->u.ident = name;
  return e;
}

Expr *make_pow(Expr *base, int exp) {
  Expr *e = malloc(sizeof(Expr));
  e->kind = EXPR_POW;
  e->u.pow.base = base;
  e->u.pow.exp = exp;
  return e;
}

Expr *make_call(char *name, ExprList *args) {
  Expr *e = malloc(sizeof(Expr));
  e->kind = EXPR_CALL;
  e->u.call.name = name;
  e->u.call.args = args;
  return e;
}

ExprList *append_expr(ExprList *list, Expr *expr) {
  ExprList *node = malloc(sizeof(ExprList));
  node->expr = expr;
  node->next = NULL;
  if (!list) return node;
  ExprList *cur = list;
  while (cur->next) cur = cur->next;
  cur->next = node;
  return list;
}

Stmt *make_assign(char *name, Expr *expr) {
  Stmt *s = malloc(sizeof(Stmt));
  s->kind = STMT_ASSIGN;
  s->u.assign.name = name;
  s->u.assign.expr = expr;
  return s;
}

Stmt *make_return(Expr *expr) {
  Stmt *s = malloc(sizeof(Stmt));
  s->kind = STMT_RETURN;
  s->u.ret_expr = expr;
  return s;
}

Stmt *make_if(Expr *cond, Stmt *then_b, Stmt *else_b) {
  Stmt *s = malloc(sizeof(Stmt));
  s->kind = STMT_IF;
  s->u.if_stmt.cond = cond;
  s->u.if_stmt.then_branch = then_b;
  s->u.if_stmt.else_branch = else_b;
  return s;
}

Stmt *make_while(Expr *cond, Stmt *body) {
  Stmt *s = malloc(sizeof(Stmt));
  s->kind = STMT_WHILE;
  s->u.while_stmt.cond = cond;
  s->u.while_stmt.body = body;
  return s;
}

Stmt *make_block(StmtList *list) {
  Stmt *s = malloc(sizeof(Stmt));
  s->kind = STMT_BLOCK;
  s->u.block = list;
  return s;
}

StmtList *append_stmt(StmtList *list, Stmt *stmt) {
  StmtList *node = malloc(sizeof(StmtList));
  node->stmt = stmt;
  node->next = NULL;
  if (!list) return node;
  StmtList *cur = list;
  while (cur->next) cur = cur->next;
  cur->next = node;
  return list;
}

Stmt *make_func(char *name, char **params, int count, Stmt *body) {
  Stmt *s = malloc(sizeof(Stmt));
  s->kind = STMT_FUNC;
  s->u.func.name = name;
  s->u.func.params = params;
  s->u.func.param_count = count;
  s->u.func.body = body;
  return s;
}

char **param_list = NULL;
int param_count = 0;
%}

%union {
  int    num;
  char  *str;
  struct Expr *expr;
  struct ExprList *elist;
  struct Stmt *stmt;
  struct StmtList *slist;
  char **strlist;
}

%token <str> T_IDENT
%token <num> T_NUMBER
%token       T_DEF T_RETURN T_IF T_ELSE T_WHILE T_SUM T_SQRT
%token       T_LE T_GE T_EQ T_NE
%token       NEWLINE
%token       T_AND T_OR

%left T_OR
%left T_AND
%left '<' '>' T_LE T_GE T_EQ T_NE
%left '+' '-'
%left '*' '/'
%right '^'

%type <expr> EXPR TERM FACT RELEXPR BIEXPR BITERM
%type <elist> opt_args ARG_LIST
%type <stmt> statement ASSIGN RETURN IF WHILE BLOCK FUNC_BLOCK
%type <slist> stmt_list

%%

program:
    /* vazio */
  | program NEWLINE
  | program top_item NEWLINE
  | program top_item
  ;

top_item:
    statement
  | FUNC_BLOCK
  ;

statement:
    ASSIGN { $$ = $1; }
  | RETURN { $$ = $1; }
  | IF     { $$ = $1; }
  | WHILE  { $$ = $1; }
  ;

FUNC_BLOCK:
    T_DEF T_IDENT '(' opt_params ')' ':' BLOCK {
      $$ = make_func($2, param_list, param_count, $7);
      param_list = NULL; param_count = 0;
    }
  ;

opt_nl:
    /* vazio */
  | NEWLINE
  ;

BLOCK:
    '{' opt_nl stmt_list '}' opt_nl { $$ = make_block($3); }
  ;

stmt_list:
    /* vazio */           { $$ = NULL; }
  | stmt_list NEWLINE     { $$ = $1; }
  | stmt_list statement NEWLINE { $$ = append_stmt($1, $2); }
  ;

ASSIGN:
    T_IDENT '=' EXPR { $$ = make_assign($1, $3); }
  ;

RETURN:
    T_RETURN EXPR { $$ = make_return($2); }
  ;

IF:
    T_IF '(' BIEXPR ')' ':' BLOCK opt_else {
      $$ = make_if($3, $6, $7);
    }
  ;

opt_else:
    /* vazio */         { $$ = NULL; }
  | T_ELSE ':' BLOCK    { $$ = $3; }
  ;

WHILE:
    T_WHILE '(' BIEXPR ')' ':' BLOCK {
      $$ = make_while($3, $6);
    }
  ;

opt_params:
    /* vazio */ { param_list = NULL; param_count = 0; }
  | PARAMS
  ;

PARAMS:
    T_IDENT {
      param_list = malloc(sizeof(char*));
      param_list[0] = $1; param_count = 1;
    }
  | PARAMS ',' T_IDENT {
      param_list = realloc(param_list, sizeof(char*) * (++param_count));
      param_list[param_count-1] = $3;
    }
  ;

BIEXPR:
    BITERM               { $$ = $1; }
  | BIEXPR T_OR BITERM  { $$ = make_binop('|', $1, $3); }
  ;

BITERM:
    RELEXPR               { $$ = $1; }
  | BITERM T_AND RELEXPR { $$ = make_binop('&', $1, $3); }
  ;

RELEXPR:
    EXPR { $$ = $1; }
  | RELEXPR '<' EXPR  { $$ = make_binop('<', $1, $3); }
  | RELEXPR '>' EXPR  { $$ = make_binop('>', $1, $3); }
  | RELEXPR T_LE EXPR { $$ = make_binop('L', $1, $3); }
  | RELEXPR T_GE EXPR { $$ = make_binop('G', $1, $3); }
  | RELEXPR T_EQ EXPR { $$ = make_binop('E', $1, $3); }
  | RELEXPR T_NE EXPR { $$ = make_binop('N', $1, $3); }
  ;

EXPR:
    EXPR '+' TERM { $$ = make_binop('+', $1, $3); }
  | EXPR '-' TERM { $$ = make_binop('-', $1, $3); }
  | TERM { $$ = $1; }
  ;

TERM:
    TERM '*' FACT { $$ = make_binop('*', $1, $3); }
  | TERM '/' FACT { $$ = make_binop('/', $1, $3); }
  | FACT { $$ = $1; }
  ;

FACT:
    T_NUMBER { $$ = make_num($1); }
  | T_IDENT { $$ = make_ident($1); }
  | T_IDENT '(' opt_args ')' { $$ = make_call($1, $3); }
  | '(' EXPR ')' { $$ = $2; }
  | T_SQRT '(' EXPR ')' { $$ = make_call("sqrt", append_expr(NULL, $3)); }
  | T_SUM '(' T_IDENT ',' EXPR ',' EXPR ',' EXPR ')' { $$ = make_call("sum", append_expr(append_expr(append_expr(append_expr(NULL, make_ident($3)), $5), $7), $9)); }
  | EXPR '^' T_NUMBER { $$ = make_pow($1, $3); }
  ;

opt_args:
    /* vazio */ { $$ = NULL; }
  | ARG_LIST { $$ = $1; }
  ;

ARG_LIST:
    EXPR { $$ = append_expr(NULL, $1); }
  | ARG_LIST ',' EXPR { $$ = append_expr($1, $3); }
  ;

%%

int main(void) {
    return yyparse();
}

void yyerror(const char *s) {
    fprintf(stderr, "Erro sintático: %s\n", s);
    exit(1);
}

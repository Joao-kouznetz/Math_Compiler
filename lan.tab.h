/* A Bison parser, made by GNU Bison 2.3.  */

/* Skeleton interface for Bison's Yacc-like parsers in C

   Copyright (C) 1984, 1989, 1990, 2000, 2001, 2002, 2003, 2004, 2005, 2006
   Free Software Foundation, Inc.

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2, or (at your option)
   any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 51 Franklin Street, Fifth Floor,
   Boston, MA 02110-1301, USA.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* Tokens.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
   /* Put the tokens into the symbol table, so that GDB and other debuggers
      know about them.  */
   enum yytokentype {
     T_IDENT = 258,
     T_NUMBER = 259,
     T_DEF = 260,
     T_RETURN = 261,
     T_IF = 262,
     T_ELSE = 263,
     T_WHILE = 264,
     T_SUM = 265,
     T_SQRT = 266,
     T_LE = 267,
     T_GE = 268,
     T_EQ = 269,
     T_NE = 270,
     NEWLINE = 271,
     T_AND = 272,
     T_OR = 273
   };
#endif
/* Tokens.  */
#define T_IDENT 258
#define T_NUMBER 259
#define T_DEF 260
#define T_RETURN 261
#define T_IF 262
#define T_ELSE 263
#define T_WHILE 264
#define T_SUM 265
#define T_SQRT 266
#define T_LE 267
#define T_GE 268
#define T_EQ 269
#define T_NE 270
#define NEWLINE 271
#define T_AND 272
#define T_OR 273




#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef union YYSTYPE
#line 11 "lan.y"
{
  int    num;
  char  *str;
}
/* Line 1529 of yacc.c.  */
#line 90 "lan.tab.h"
	YYSTYPE;
# define yystype YYSTYPE /* obsolescent; will be withdrawn */
# define YYSTYPE_IS_DECLARED 1
# define YYSTYPE_IS_TRIVIAL 1
#endif

extern YYSTYPE yylval;


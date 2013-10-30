%option nounput
%{
#include <iostream>
#include "agglparser.hpp"
using namespace std;
#define YY_DECL extern "C" int yylex()
int line_num = 1;

%}
%%
===            { return SEPARATOR;}
=>             { return GETS; }
->             { return LINKEDTO; }
[ \t]          ;
[\(\)\{\}:=,]  { return yytext[0]; }
[0-9]+         { yylval.ival = atoi(yytext); return INT; }
[a-zA-Z0-9]+   { yylval.sval = strdup(yytext); return STRING; }
\n             { ++line_num; return ENDL; }
.              ;
%%
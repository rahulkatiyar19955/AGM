%{
#include <cstdio>
#include <iostream>
using namespace std;

#include "agglparser.hpp"


#include <agm.h>
AGM *inputAGM = NULL;
std::vector <AGGLRule> *agmRules = NULL;

AGGLRule rule;
bool leftGraph = true;


std::string i2String(int i);
void addLink(bool l, const char *a, const char *b, const char *label);
void addSymbol(bool l, const char *id, const char *type, int x, int y);
void addSymbol(bool l, int id, const char *type, int x, int y);

extern "C" int yylex();
extern "C" int yyparse();
extern "C" FILE *yyin;
extern int line_num;

void yyerror(const char *s);
%}

%union
{
	int ival;
	char *sval;
}

// define the constant-string tokens:
%token SNAZZLE TYPE
%token END ENDL
%token SEPARATOR
%token GETS
%token LINKEDTO

%token <ival> INT
%token <sval> STRING

%%
aggl:
  header SEPARATOR ENDLS rules { cout << "AGGL file read ok!" << endl; }
;

header:
  header globalattribute
| globalattribute
;

globalattribute:
  STRING '=' STRING ENDLS { inputAGM->addAttribute($1, $3); }
| STRING '=' INT ENDLS    { inputAGM->addAttribute($1, $3); }
;

rules:
  rules rule
| rule
;
     
rule:
  STRING ':' STRING ENDLS '{' ENDLS graphL GETS ENDLS graphR '}' ENDLS {rule.computeEffects(); rule.setName($1); rule.setActive($3);agmRules->push_back(rule); rule.clear(); }
;

graphL:
  '{' ENDLS symbols links '}' ENDLS { leftGraph=false; }
| '{' ENDLS symbols '}' ENDLS       { leftGraph=false; }
;

graphR:
  '{' ENDLS symbols links '}' ENDLS { leftGraph=true; }
| '{' ENDLS symbols '}' ENDLS       { leftGraph=true; }
;

symbols:
  symbols symbol
| symbol
;

symbol:
  STRING ':' STRING '(' INT ',' INT ')' ENDLS { addSymbol(leftGraph, $1, $3, $5, $7); }
| INT    ':' STRING '(' INT ',' INT ')' ENDLS { addSymbol(leftGraph, $1, $3, $5, $7); }
;

links:
  links link
| link;

link:
  STRING LINKEDTO STRING '(' STRING ')' ENDLS {                                               addLink(leftGraph, $1, $3, $5); }
| INT    LINKEDTO INT    '(' STRING ')' ENDLS { std::string s1=i2String($1), s2=i2String($3); addLink(leftGraph, s1.c_str(), s2.c_str(), $5); }
| INT    LINKEDTO STRING '(' STRING ')' ENDLS { std::string s1=i2String($1); addLink(leftGraph, s1.c_str(), $3, $5); }
| STRING LINKEDTO INT    '(' STRING ')' ENDLS { std::string s2=i2String($3); addLink(leftGraph, $1, s2.c_str(), $5); }
;

ENDLS:
  ENDLS ENDL
| ENDL
;


%%

std::string i2String(int i)
{
	char text[512];
	snprintf(text, 511, "%d", i);
	return std::string(text);
}

void addLink(bool l, const char *a, const char *b, const char *label)
{
	rule.addLink(l, std::string(a), std::string(b), std::string(label));
}

void addSymbol(bool l, const char *id, const char *type, int x, int y)
{
	rule.addSymbol(l, id, type);
}

void addSymbol(bool l, int id, const char *type, int x, int y)
{
	char text[512];
	snprintf(text, 511, "%d", id);
	addSymbol(l, text, type, x, y);
}

bool parseAGGL(const char *path, AGM *agm, std::vector <AGGLRule> *rules)
{
	inputAGM = agm;
	agmRules = rules;
	FILE *myfile = fopen(path, "r");
	if (!myfile)
	{
		cout << "I can't open " << path << "!" << endl;
		return false;
	}
	yyin = myfile;
	do
	{
		yyparse();
	}
	while (!feof(yyin));
	
	return true;
}

void yyerror(const char *s)
{
	cout << "Parse error on line " << line_num << "!  Message: " << s << endl;
	exit(-1);
}

%token NUM
%token ID
%start program
%%
program: declaration_list
;
declaration_list: declaration_list declaration
| declaration
;
declaration: var_declaration 
| fun_declaration 
;
var_declaration: type_specifier pid ID ';'
| type_specifier pid ID '[' pnum NUM ']' get_value ';'
;
type_specifier: "int" 
| "void"
;
fun_declaration: type_specifier pid ID '(' params ')' compound_stmt
;
params: param_list
| "void"
;
param_list: param_list ',' param
| param
;
param: type_specifier pid ID
| type_specifier pid ID '[' ']'
;
compound_stmt: '{' local_declarations statement_list '}'
;
local_declarations: local_declarations var_declaration
| /* epsilon */
;
statement_list: statement_list statement
| /* epsilon */
;
statement: expression_stmt
| compound_stmt
| selection_stmt
| iteration_stmt
| return_stmt
| switch_stmt
;
expression_stmt: expression ';'
| "break" ';'
| ';'
;
selection_stmt: "if" '(' expression ')' save statement jpf "endif"
| "if" '(' expression ')' save statement "else" jpf_save statement jp "endif"
;
iteration_stmt: "while" label '(' expression ')' save statement while
;
return_stmt: "return" ';'
| "return" expression ';'
;
switch_stmt: "switch" '(' expression ')' '{' case_stmts default_stmt '}'
;
case_stmts: case_stmts case_stmt
| /* epsilon */
;
case_stmt: "case" NUM ':' statement_list
;
default_stmt: "default" ':' statement_list
| /* epsilon */
;
expression: var '=' expression assign
| simple_expression
;
var: pid ID
| pid ID '[' expression ']' get_value
;
simple_expression: additive_expression '<' additive_expression lt
| additive_expression | additive_expression "==" additive_expression equal
;
additive_expression: additive_expression '+' term add
| term | additive_expression '-' term minus
;
term: term '*' factor mul
| factor | term '/' factor div
;
factor: '(' expression ')'
| var
| call
| pnum NUM
;
call: pid ID '(' args ')'
;
args: arg_list
| /* epsilon */
;
arg_list: arg_list ',' expression
| expression
;
pid: /* epsilon */;
pnum: /* epsilon */;
assign: /* epsilon */;
add: /* epsilon */;
minus: /* epsilon */;
mul: /* epsilon */;
div: /* epsilon */;
equal: /* epsilon */;
lt: /* epsilon */;
save: /* epsilon */;
jpf: /* epsilon */;
jpf_save: /* epsilon */;
jp: /* epsilon */;
label: /* epsilon */;
while: /* epsilon */;
get_value: /* epsilon */;
%%

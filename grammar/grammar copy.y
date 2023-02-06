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
| type_specifier pid ID '[' pnum NUM ']' ';'
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
| output_fun
;
expression_stmt: expression ';' pop
| "break" ';' break_action
| ';'
;
selection_stmt: "if" '(' expression ')' save statement "endif" jpf
| "if" '(' expression ')' save statement "else" jpf_save statement "endif" jp
;
iteration_stmt: "while" label '(' expression ')' save statement while
;
return_stmt: "return" ';'
| "return" expression ';'
;
switch_stmt: "switch" jp_forward save '(' expression ')' '{' case_stmts default_stmt '}' jp_switch
;
case_stmts: case_stmts case_stmt
| /* epsilon */
;
case_stmt: "case" pnum NUM switch_compare save ':' statement_list jpf
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
output_fun: "output" '(' expression ')' output_action
;
pid: /* epsilon */;
pnum: /* epsilon */;
jpf_save: /* epsilon */;
label: /* epsilon */;
jp_forward: /* epsilon */;
switch_compare: /* epsilon */;
%%

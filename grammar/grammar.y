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
var_declaration: type_specifier pid add_to_symbol_table ID ';'
| type_specifier pid add_to_symbol_table ID '[' pnum add_array_type_kind NUM ']' ';'
;
type_specifier: "int" 
| "void"
;
fun_declaration: type_specifier pid add_to_symbol_table ID add_func_kind add_scope '(' params ')' compound_stmt
;
params: param_list
| "void"
;
param_list: param_list ',' param
| param
;
param: type_specifier pid add_to_symbol_table ID
| type_specifier pid add_to_symbol_table ID '[' ']'
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
selection_stmt: "if" '(' expression ')' save statement "endif"
| "if" '(' expression ')' save statement "else" jpf_save statement "endif"
;
iteration_stmt: "while" jp_forward break_save label '(' expression ')' save statement
;
return_stmt: "return" ';'
| "return" expression ';'
;
switch_stmt: "switch" jp_forward break_save '(' expression ')' '{' case_stmts default_stmt '}'
;
case_stmts: case_stmts case_stmt
| /* epsilon */
;
case_stmt: "case" pnum NUM switch_compare save ':' statement_list
;
default_stmt: "default" ':' statement_list
| /* epsilon */
;
expression: var '=' expression
| simple_expression
;
var: pid ID
| pid ID '[' expression ']'
;
simple_expression: additive_expression '<' additive_expression
| additive_expression | additive_expression "==" additive_expression
;
additive_expression: additive_expression '+' term
| term | additive_expression '-' term
;
term: term '*' factor
| factor | term '/' factor
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
jpf_save: /* epsilon */;
label: /* epsilon */;
jp_forward: /* epsilon */;
switch_compare: /* epsilon */;
save: /* epsilon */;
break_save: /* epsilon */;
add_array_type_kind: /* epsilon */;
add_func_kind: /* epsilon */;
add_scope: /* epsilon */;
add_to_symbol_table: /* epsilon */;
%%

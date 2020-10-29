doc_str = '''Usage : ./html2js.py <input_html> <output_js>

This script takes as input a html file and writes to a file a js function that generates the given html


Positional arguments:
	input_html						: Input file with the html code
	output_js 						: Output file with the generated js function


Optional arguments:
	-h / --help						: Show help message and exit
	-d / --doc						: Show extended documentation and exit
	-f function_name / --function-name function_name	: Set the name of the generated function
	-t test_file / --test test_file				: Generate a html test file
								  This option will raise a warning if is used with params of type element
	-v / --verbose						: Display generated js code in stdout
	-p / --param						: Parametrize some content of the given html as a function argument
								  Syntax : --param <pattern> <type> [variable_name]. Where:
									- Pattern : Text to match in the html file and replace by a parameter
									- Type : Either 'element' or 'text'. Whether the param should be added as a DOM element
										(with appendChild(param)) or as text (with appendChild(document.createTextNode(param)))
									- Variable name : Name of the variable in the function. Optional
								  This argument can be used as many times as desired
	-i n_tabs / --indent n_tabs				: Starting indent in tabs. (Function content will add another tab)
	--template-file template				: Template file used for the autogenerated tests files
	--supress-warning					: Supress the generated warning when creating a test file with element type params
	--remove-coments					: Remove the comments before the function declaration

Additional info:
- Inside the function the temporal created variables will be named based on the element id if there is one.
	If not, they will be incrementally named based on the tag name with the format '<tag>_<num>'
	Example :
		The first div does not have an id. It will be declared as 'let div_1 = ...'
		The second div does have an id, which is 'mydiv'. It will be declared as 'let mydiv = ...'
		The third div does not have an id. It will be declared as 'let div_2 = ...'
	Text nodes are not created as variables. They are directly appended as child
	Example : mydiv.appendChild(document.createTextNode('divtext'))

- Function argument names can be specified when using -p / --param.
	If the argument name is not specified they will follow the format 'param_<num>'
	In this case, the num increment is done based on the argument place.
	Example :
		If no argument is named : function func(param_1, param_2, param_3, ...)
		One argument is named   : function func(param_1, myparam, param_3, ...)

- One argument pattern can be in more than one place of the html file

'''

usage_examples = '''Usage examples:
	./html2js.py test/html/simple_div.html test/js/simple_div.js -f simple_div -t test/templates/simple_div.html -v
	./html2js.py test/html/service_div.html test/js/service_div.js -f service_div -t test/templates/service_div.html -v
	./html2js.py test/html/parametrized_service_div.html test/js/parametrized_service_div.js -f service_div -t test/templates/parametrized_service_div.html --param SERVICE text service_name --param OK text num_ok --param WARN text num_warnings --param ERR text num_errors -v
	./html2js.py -f table_header -v test/html/table_header.html test/js/table_header.js -i 2
	./html2js.py -f table_row -v -i 2 test/html/table_row.html test/js/table_row.js -p FECHA text fecha -p CLIENTE text cliente -p USER text user -p SERVER text server -p NAT text nat -p DESTINO text destino -p DURACION text duracion -p START text start -p END text end
	./html2js.py -f aviso_lentitud -v -i 2 test/html/aviso_lentitud.html test/js/aviso_lentitud.js
'''

repo = 'https://github.com/vLabayen/html2js'

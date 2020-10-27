#!/bin/python3

#Rcursively generate element code
def element_code(e, indent = 1):
	if e['type'] == 'text' or e['param']: return []

	e_code = []
	if e['type'] == 'tag':
		e_code.append(createElement(e['varname'], e['name'], indent))
		e_code.append(addProps(e['varname'], e['attrs']))
		e_code.append('\n')
		for c in e['childs']: e_code += element_code(c)

	return e_code

#Generate createElement statement
def createElement(var, tag, indent = 1):
	return "{}let {} = document.createElement('{}');\n".format('\t'*indent, var, tag)

#Generate add properties statements
def addProps(var, props, indent = 1):
	return ''.join("{}{}.{};\n".format('\t'*indent, var, get_method(p, v)) for p,v in props.items())

#Generate method to add property
def get_method(prop, value):
	if prop == 'id': return 'id = {}'.format(value)
	if prop == 'class': return 'classList.add(...{})'.format(value)
	if prop == 'style': return 'style = "{}"'.format(value)

	return 'setAttribute("{}", "{}")'.format(prop, value)

#Recusively generate appendChild statements
#We start appending in the end of the tree
def appendAll(e, indent = 1):
	if e['type'] == 'text': return []

	append_code = []
	for c in e['childs']:
		append_code += appendAll(c)
		append_code.append(appendChild(e, c))

	return append_code

#Generate appendChilds statement
def appendChild(parent, child, indent = 1):
	if child['type'] == 'tag':
		return "{}{}.appendChild({});\n".format('\t'*indent, parent['varname'], child['varname'])

	arg = child['varname'] if child['param'] else "'{}'".format(child['text'])
	return "{}{}.appendChild(document.createTextNode({}));\n".format('\t'*indent, parent['varname'], arg)

#Generate function return statement
def get_return(element_tree, indent = 1):
	if len(element_tree) == 1: return '{}return {};\n'.format('\t'*indent, element_tree[0]['varname'])
	return '{}return [{}]'.format('\t'*indent, ','.join(e['varname'] for e in element_tree))

#Generate js function
def generate_function(args, element_tree, repo, src_code, with_header = True):
	lines = []

	if with_header:
		lines += ['//AUTOGENERATED FUNCTION. Check the script in {}\n'.format(repo)]
		lines += ['//The output should be {} such that contains the following structure{}:\n'.format(
			*(('a element', '') if len(element_tree) <= 1 else ('an array of elements', 's'))
		)]
		lines += ['//{}\n'.format(l) for l in src_code.split('\n') if l != ""]

	lines += ['function {}({}) {}\n'.format(args.function_name, ', '.join(p['varname'] for p in args.param), '{')]
	lines += [''.join(element_code(e)) for e in element_tree]
	lines += [''.join(appendAll(e)) for e in element_tree]
	lines += [get_return(element_tree)]
	lines += ['}\n']
	return lines

#Generate html test template
def generate_test(args, function_lines):
	with open(args.template_file, 'r') as f: template = f.read()
	template = template.replace('###TITLE###', 'Test for {}'.format(args.function_name))
	template = template.replace('###FUNCTION_DEFINITION###', ''.join(function_lines))

	call_args = ', '.join([("'{}'".format(p['text']) if p['type'] == 'text' else "null") for p in args.param])
	template = template.replace('###FUNCTION_CALL###', 'document.getElementById("template_body").appendChild({}({}));\n'.format(args.function_name, call_args))
	with open(args.test, 'w') as f: f.write(template)

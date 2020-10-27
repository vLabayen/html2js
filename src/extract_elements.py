#!/bin/python3
from bs4.element import Tag, NavigableString
variable_name_counter = {}

#Recursively extract element data
def extract_element(e, params):
	global variable_name_counter
	params_names = [p['varname'] for p in params]

	if (type(e) == Tag):
		#Create tag element
		element = {'type' : 'tag', 'name' : e.name, 'attrs' : e.attrs, 'childs' : [], 'param' : False}

		#Asign variable name
		if 'id' in e.attrs: element['varname'] = e.attrs['id']
		else:
			if e.name not in variable_name_counter: variable_name_counter[e.name] = 0
			variable_name_counter[e.name] += 1
			#Ensure variable name does not match with a param
			while '{}_{}'.format(e.name, variable_name_counter[e.name]) in params_names: variable_name_counter[e.name] += 1
			element['varname'] = '{}_{}'.format(e.name, variable_name_counter[e.name])

		#Recusivelly append every child
		if len(list(e.children)) > 0:
			for c in e.children: element['childs'].append(extract_element(c, params))

	elif (type(e) == NavigableString):
		#Create text element
		element = {'type' : 'text', 'text' : str(e), 'param' : False}

		#Asign variable name
		for p in params:
			if str(e) == p['pattern']:
				element['varname'] = p['varname']
				element['param'] = True
				element['type'] = p['type']
				if p['type'] == 'element':
					element['attrs'] = {}
					element['childs'] = []

				#Text is stored for automate testing
				p['text'] = element['text']
				break
		else:
			if 'text' not in variable_name_counter: variable_name_counter['text'] = 0
			variable_name_counter['text'] += 1
			#Ensure variable name does not match with a param
			while 'text_{}'.format(variable_name_counter['text']) in params_names: variable_name_counter['text'] += 1
			element['varname'] = 'text_{}'.format(variable_name_counter['text'])

	return element

#!/bin/python3
import re
import os
import sys
import warnings
import argparse
from argparse import ArgumentTypeError as ate
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.abspath('src'))
from extract_elements import extract_element
from generate_code import *
from doc import doc_str, repo

#Define script arguments
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, epilog='''Usage examples:
	./html2js.py test/html/simple_div.html test/js/simple_div.js -f simple_div -t test/templates/simple_div.html -v
	./html2js.py test/html/service_div.html test/js/service_div.js -f service_div -t test/templates/service_div.html -v
	./html2js.py test/html/parametrized_service_div.html test/js/parametrized_service_div.js -f service_div -t test/templates/parametrized_service_div.html --param SERVICE text service_name --param OK text num_ok --param WARN text num_warnings --param ERR text num_errors -v
''')
parser.add_argument('input_html', help="File with html code")
parser.add_argument('output_js', help="File to write js function")
parser.add_argument('-d', '--doc', help="Show extended documentation and exit. input_html and output_js must be provided to show the doc (blame argparse)", default=False, action="store_true")
parser.add_argument('-f', '--function-name', help="Output function name", default="func", metavar="function_name")
parser.add_argument('-t', '--test', help="Generate test html file", default=None, metavar="test_file")
parser.add_argument('-v', '--verbose', help="Display generated code in stdout", default=False, action="store_true")
parser.add_argument('-p', '--param', help="Add function parameter. Syntax : --param <pattern> <type> [variable_name]", default=[], action='append', nargs='+', metavar='param_spec')
parser.add_argument('--template-file', help="Html test template file", default="test/templates/template.html", metavar='template')
parser.add_argument('--supress-warning', help="Supress the generated warning when creating a test file with element type params", default=False, action='store_true')
parser.add_argument('--remove-coments', help="Remove the comments before the function declaration", default=False, action='store_true')
args = parser.parse_args()

if args.doc: sys.exit(doc_str)

#Verify and parse param args
for i,params in enumerate(args.param):
	if len(params) < 2 or len(params) > 3: raise ate('Param args must be in the syntax <pattern> <type> [variable_name]')
	if params[1] not in ['element', 'text']: raise ate("Second argument must be either 'element' or 'text'")
	args.param[i] = {
		'pattern' : params[0],
		'type' : params[1],
		'varname' : params[2] if len(params) == 3 else 'param_{}'.format(i)
	}

#Raise warning if --test is used with --param of element type.
#We cannot fully generate a test for a element type param
if args.test is not None and any(p['type'] == 'element' for p in args.param) and not args.supress_warning:
	warnings.warn('''
		Cannot fully generate a test html file with element type parameters.
		The html file will be generated but element parameters should be manually provided
	''')

#Read file, replace tab and newlines by spaces, replace multiple consecutive spaces by one space
with open(args.input_html, 'r') as f: src_code = f.read()
html_code = src_code.replace('\t', '').replace('\n', '')
html_code = re.sub('\s+', ' ', html_code)

#Parse html and extract elements
soup = BeautifulSoup(html_code, features="html.parser")
element_tree = [extract_element(c, args.param) for c in soup.children]

#Generate js code
lines = generate_function(args, element_tree, repo, src_code, not args.remove_coments)

#Show generated code if verbose
if args.verbose: print(''.join(lines), end="")

#Write js code
with open(args.output_js, 'w') as f: f.write(''.join(lines))

#Generate html test file
if args.test is not None: generate_test(args, lines)

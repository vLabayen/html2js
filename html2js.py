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
from doc import doc_str, repo, usage_examples

#Define script arguments
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, epilog=usage_examples)
parser.add_argument('input_html', help="File with html code")
parser.add_argument('output_js', help="File to write js function")
parser.add_argument('-d', '--doc', help="Show extended documentation and exit. input_html and output_js must be provided to show the doc (blame argparse)", default=False, action="store_true")
parser.add_argument('-f', '--function-name', help="Output function name", default="func", metavar="function_name")
parser.add_argument('-t', '--test', help="Generate test html file", default=None, metavar="test_file")
parser.add_argument('-v', '--verbose', help="Display generated code in stdout", default=False, action="store_true")
parser.add_argument('-p', '--param', help="Add function parameter. Syntax : --param <pattern> <type> [optional_flags]", default=[], action='append', nargs='+', metavar='param_spec')
parser.add_argument('-i', '--indent', help="Starting indent in tabs", default=0, type=int, metavar="n_tabs")
parser.add_argument('--template-file', help="Html test template file", default="test/templates/template.html", metavar='template')
parser.add_argument('--supress-warning', help="Supress the generated warning when creating a test file with element type params", default=False, action='store_true')
parser.add_argument('--remove-coments', help="Remove the comments before the function declaration", default=False, action='store_true')
args = parser.parse_args()

if args.doc:
	print(doc_str)
	print(usage_examples)
	sys.exit()

#Verify and parse param args
for i,params in enumerate(args.param):
	supported_types = ['element', 'text']
	supported_flags = ['variable_name']

	if len(params) < 2: raise ate('Param args must be in the syntax <pattern> <type> [optional_flags]')
	if params[1] not in supported_types: raise ate("Second argument must be {} or {}".format(','.join(supported_types[:-1]), supported_types[-1]))

	try: flags = {flag_name : flag_value for flag_name,flag_value in (provided_flag.split("=") for provided_flag in params[2:]) if flag_name in supported_flags}
	except ValueError: raise ate("Optional flags must be provided in the syntax <flag_name>=<flag_value>")

	args.param[i] = {
		'pattern' : params[0],
		'type' : params[1],
		'varname' : flags['variable_name'] if 'variable_name' in flags else 'param_{}'.format(i)
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
lines = generate_function(args, element_tree, repo, src_code, not args.remove_coments, args.indent)

#Show generated code if verbose
if args.verbose: print(''.join(lines), end="")

#Write js code
with open(args.output_js, 'w') as f: f.write(''.join(lines))

#Generate html test file
if args.test is not None: generate_test(args, lines)

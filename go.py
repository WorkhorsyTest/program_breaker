#!/usr/bin/env python
# -*- coding: UTF-8 -*-


# Make sure we are in at least python 2.7
import sys
if sys.version_info < (2, 7) or sys.version_info >= (2, 8):
	print("Python 2.7 is required. Exiting ...")
	exit(1)

import os
import re
import pexpect


def before(s, n):
	i = s.find(n)
	if i == -1:
		return s
	else:
		return s[0 : i]

def before_last(s, n):
	i = s.rfind(n)
	if i == -1:
		return s
	else:
		return s[0 : i]

def after(s, n):
	i = s.find(n)
	if i == -1:
		return s
	else:
		return s[i+len(n) : ]

def between(s, l, r):
	return before(after(s, l), r)

def between_last(s, l, r):
	return before_last(after(s, l), r)

def to_bool(value):
	if value == 'false':
		return False
	elif value == 'true':
		return True

def to_python_type(str_c_type):
	int_types = [
		'short', 
		'int', 
		'long', 
		'long long', 
		'unsigned short', 
		'unsigned int', 
		'unsigned long', 
		'unsigned long long'
	]

	float_types = [
		'float', 
		'double', 
		'long double'
	]

	bool_types = [
		'_Bool'
	]

	char_types = [
		'char', 
		'unsigned char', 
		'signed char'
	]

	if str_c_type in int_types:
		return int
	elif str_c_type in float_types:
		return float
	elif str_c_type in bool_types:
		return bool
	elif str_c_type in char_types:
		return str
	elif re.search('\[\d+\]$', str_c_type):
		return list

def to_python_value(str_c_type, str_value):
	type = to_python_type(str_c_type)

	if type is int:
		return int(str_value)
	elif type is float:
		return float(str_value)
	elif type is bool:
		return to_bool(str_value)
	elif type is str:
		return str_value
	elif type is list:
		array_type = before(str_c_type, ' [')
		list_type = to_python_type(array_type)

		# String
		if list_type is str:
			retval = between_last(str_value, '"', '"')
			return retval
		# Array
		else:
			retval = []
			for n in between(str_value, '{', '}').split(', '):
				n = to_python_value(array_type, n)
				retval.append(n)
			return retval
	else:
		raise Exception("Unknown type '{0}' to convert from string.".format(str_c_type))


class Debugger(object):
	def __init__(self):
		self.child = None
		self.line_no = -1
		self.file = None
		self.function = None
		self.program = None
		self.program_path = None
		self.lines = None

		# Start GDB wihtout the intro copyright message
		command = None
		self.child = pexpect.spawn('gdb -quiet')
		self._run_command(command, False, False)

		# Turn off pagination
		command = 'set pagination off'
		self._run_command(command, False, False)

		print('init', self.file, self.function, self.line_no)

	def _run_command(self, command, get_function, get_line_number):
		# Run the command and get the output
		if command:
			self.child.sendline(command)
		self.child.expect('\(gdb\)')
		output = self.child.before + self.child.after
		assert(output.endswith('(gdb)'))

		# Get the lines
		self.lines = output.split('\r\n')

		# Get the function and file name
		if get_function:
			# Stepping
			if len(self.lines) >= 2 and re.match('\w+ \(\) at \w+.\w+:\d+', self.lines[1]):
				self.file = between(self.lines[1], 'at', ':').strip()
				self.function = before(self.lines[1], ' ')
			# Breakpoint
			elif len(self.lines) >= 3 and re.match('Temporary breakpoint \d+, \w+ \(\) at \w+.\w+:\d+', self.lines[-3]):
				self.file = between(self.lines[-3], 'at', ':').strip()
				self.function = between(self.lines[-3], ',', '(').strip()

		# Get the line number
		if get_line_number:
			self.line_no = int(self.lines[-2].split()[0])

		return output

	def load(self, program):
		self.program = program
		self.program_path = os.path.abspath(program)

		# Load the program
		command = 'file {0}'.format(self.program)
		self._run_command(command, False, False)
		self.line_no = -1
		self.file = None
		self.function = None
		print('load', self.file, self.function, self.line_no)

	def start(self):
		# Start the program and breakpoint on the first line
		command = 'start'
		output = self._run_command(command, True, True)
		self.file = between(output, 'file', ',').strip()
		self._run_command('target record-full', False, False)
		print('start', self.file, self.function, self.line_no)

	def step_to_line(self, line):
		command = 'next'

		if line < self.line_no:
			print("bad line")
			exit()

		while self.line_no < line:
			self._run_command(command, True, True)
		print('step_to_line', self.file, self.function, self.line_no)

	def step_forward(self, steps=1):
		command = 'next'

		for n in range(steps):
			self._run_command(command, True, True)
			print('step_forward', self.file, self.function, self.line_no)

	def step_back(self, steps=1):
		command = 'reverse-next'

		for n in range(steps):
			self._run_command(command, True, True)
			print('step_back', self.file, self.function, self.line_no)

	def step_in(self):
		command = 'step'
		output = self._run_command(command, True, True)
		print('step_in', self.file, self.function, self.line_no)

	def locals(self):
		variables = {}

		# Get the name and value for all the local variables
		command = 'info locals'
		output = self._run_command(command, False, False)
		output = between(output, 'info locals', '(gdb)').strip()
		for line in output.split('\r\n'):
			name, value = line.split(' = ')
			variables[name] = { 'value' : value }

		# Get the types for all the local variables
		for name, attr in variables.items():
			command = 'ptype {0}'.format(name)
			output = self._run_command(command, False, False)
			output = after(output.split('\r\n')[1], ' = ')
			attr['type'] = output

		# Convert any non string values
		for name, attr in variables.items():
			value = to_python_value(attr['type'], attr['value'])
			attr['value'] = value

		'''
		print('locals:')
		for name, attr in variables.items():
			print('    ' + name, attr['type'], attr['value'])
		'''
		return variables

if __name__ == '__main__':
	debugger = Debugger()
	debugger.load('main')
	debugger.start()

	debugger.step_to_line(41)
	locs = debugger.locals()

	debugger.step_in()

	debugger.step_to_line(12)
	print('value: "{0}"'.format(debugger.locals()['name']['value']))

	debugger.step_back()
	print('value: "{0}"'.format(debugger.locals()['name']['value']))


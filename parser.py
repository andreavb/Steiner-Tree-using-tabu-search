#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: Gustavo Serra Scalet
Licença: GPLv3 ou mais recente
"""

__VERSION__ = 0.1

def steinerParser(source, verbose = False, args = []):
	"""
	Parses the source file and returns the structure
	"""
	from re import compile, search
	
	content = open(source).read().splitlines()  # list of all the lines of the source file
	_EDGE_REGEX = compile('E\s+(?P<origin>[0-9]*)\s+(?P<destiny>[0-9]*)\s+(?P<weight>[0-9]*)')  # for a common edge
	_TERMINAL_REGEX = compile('T\s+(?P<edge_name>[0-9]*)')  # for a terminal vertex

	# edges[x] = (y,w) : there is an edge with weight w from x to y 
	edges = {}
	# list of all the vertex that are terminals, so we'll have to find a path
	# with them that has minimal cost 
	terminals = []

	for line in content:
		clean_line = line.strip().upper()  # removing spaces on [0] and [-1] and uppering case
		edge_match = search(_EDGE_REGEX, clean_line)
		if edge_match:  # found an edge line description
			data = edge_match.groupdict()
			if verbose:
				print "Line '%s' is an edge description line with %s" % (line, str(data))
			# non-directional graph
			edges[int(data['origin'])] = int(data['destiny']), int(data['weight'])
			edges[int(data['destiny'])] = int(data['origin']), int(data['weight'])
			continue
		terminal_match = search(_TERMINAL_REGEX, clean_line)
		if terminal_match:  # terminal description line
			data = terminal_match.groupdict()
			if verbose:
				print "Line '%s' is a terminal description line with %s" % (line, str(data))
			terminals.append(int(data['edge_name']))
			# continue  # not needed, it's the end of this loop anyway
	# end for
	return edges, terminals

if __name__ == "__main__":
	from sys import argv, exit
	from os import sep
	from optparse import OptionParser
	
	usage = """usage: %prog SOURCE_FILE [-v --verbose]
Parses input SOURCE_FILE to the desired structure"""
	parser = OptionParser(usage,
			description=steinerParser.__doc__.replace('\t',''),
			version="%%prog %s" % __VERSION__)
	parser.add_option('-v', '--verbose', dest='verbose', action="store_true",
		default=False, help="Verbose")
	
	if len(argv) == 2 and argv[1] in ('-h', '--help', '--version') or len(argv) == 1:
		# not enough arguments
		print """ERROR: not enough arguments.
Try `%s --help' for more information""" % argv[0].split(sep)[-1]
		exit(1)
	else:
		source = argv[1]

	(opt, args) = parser.parse_args(argv[2:])
	verbose = opt.verbose
	steinerParser(source, verbose, args)


#!/usr/bin/python

import xml.etree.ElementTree as ET
import sys
import re
import glob
import argparse
import os

def main(argv):
	parser = argparse.ArgumentParser(description="Parse NSE XML output and create CSV.  Will process all xml files in directory")
	parser.add_argument('-i', '--inputfile', help='The folder with the xml outputs')
	parser.add_argument('-o', '--outputfile', help='The output csv filename')
	parser.add_argument('-n', '--noheaders', action='store_true', help='This flag removes the header from the CSV output File')
	args = parser.parse_args()
	
	outputfile = "NSEoutput.csv"
	if(args.outputfile!=None):
		outputfile = args.outputfile
	fo = open(outputfile, 'w+')
	if(args.noheaders != True):
		out = "ip" + ',' + "hostname" + ',' + "port" + ',' + "protocol" + ',' + "service" + ',' + "version" + ',' + "output" + '\n'
		fo.write (out)
	folder = '*.xml'
	if(args.inputfile!=None):
		print ("here")
		if(args.inputfile.endswith(os.sep)):
			folder = args.inputfile + '*.xml'
		else:
			folder = args.inputfile + os.sep + '*.xml'
	for filename in glob.glob(folder):
		try:
			tree = ET.parse(filename)
			root = tree.getroot()
		except ParseError as e:
			print "Parse error({0}): {1}".format(e.errno, e.strerror)
			sys.exit(2)
		except:
			print "Unexpected error:", sys.exc_info()[0]
			sys.exit(2)
		
		for host in root.findall('host'):
			ip = host.find('address').get('addr')
			hostname = ""
			if host.find('hostnames').find('hostname') is not None:
				hostname = host.find('hostnames').find('hostname').get('name')
			for port in host.find('ports').findall('port'):
				protocol = port.get('protocol')
				if protocol is None:
					protocol = ""
				portnum = port.get('portid')
				if portnum is None:
					portnum = ""
				service = port.find('service').get('name')
				if service is None:
					service = ""
				version = port.find('service').get('product')
				if version is None:
					version = ""
				output = port.find('script').get('output')
				output = re.sub('&#xa;', '', output)
				if output is None:
					output = ""
				out = ip + ',' + hostname + ',' + portnum + ',' + protocol + ',' + service + ',' + version + ',' + output + '\n'
				fo.write (out)
		
	fo.close()
	
if __name__ == "__main__":
   main(sys.argv)

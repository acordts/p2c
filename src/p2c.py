# -*- coding: utf-8 -*-
import csv
import glob
import os
import re
import time

class contig(object):
    '''
    @summary: contig / primer structure including option for a position parameter
    '''
    def __init__(self, name, sequence, counter = None):
        if name.startswith('>'):
            name = name[1:]
        self.name       = name
        self.sequence   = sequence.upper()


class primer_reader(object):
    '''
    @summary: read primer_file as csv
    '''
    def __init__(self, primer_file):
        '''
        @summary: prepare primer file and create ordered primer list
        '''
        self._primer_file = primer_file
        self._primer_list = []
        self._read_csv()
        
    def _read_csv(self, delimiter = ';'):
        '''
        @summary: try to create primer object incl. probe, sequence [,position]
        '''
        stream = csv.DictReader(open(self._primer_file, 'r'), delimiter = delimiter)
        for line in stream:
            primer_name     = line.get('probe')
            primer_sequence = line.get('sequence')
            if primer_name and primer_sequence: 
                self._primer_list.append(contig(primer_name, primer_sequence))
                
    def get_primer(self):
        '''
        @return: primer collection of primer / contig objects
        @rtype: list
        '''
        return self._primer_list
    

class contig_reader(object):
    '''
    @summary: get contigs from txt file. 
    @note: format >name\nsequence\n>name ... aso.
    '''
    def __init__(self, sequencefile):
        self.sequencefile   = sequencefile
        self.contig_list    = []
        self._read_contigs_list()
        
    def get_contigs(self):
        '''
        return: contig object collection
        @rtype: list
        '''
        return self.contig_list
    
    def _read_contigs_list(self):
        '''
        @summary: create contig list out of fasta formated textfile
        '''
        lines           = [line.strip() for line in open(self.sequencefile, 'r')]
        contig_name     = ''
        contig_sequence = ''
        for line in lines:
            if line.startswith('>'):
                if contig_sequence:
                    self.contig_list.append(contig(contig_name, contig_sequence))
                contig_name     = line.strip()
                contig_sequence = ''
            else:
                contig_sequence += line.strip()
        self.contig_list.append(contig(contig_name, contig_sequence))

        
class chuck_norris(object):
	'''
	@summary: chuck norris count to infinity, twice and meanwhile he search for primer
	'''

	def __init__(self, contig_list, primer_list, output_file = 'hit_survey.csv'):
		self._columns = ['contig name', 'primer', 'start', 'end', 'length', 'requested', 'located']

		self._contig_list = contig_list
		self._primer_list = primer_list
		self._result_file = os.path.join('final', output_file)
		self._clean_up()

	def _clean_up(self):
		dst_folder = os.path.dirname(self._result_file)
		if not os.path.exists(dst_folder):
			os.makedirs(dst_folder)

		with open(self._result_file, 'w') as stream:
			stream.write('%s\n'%(';'.join(self._columns)))
		
    
	def roundhousekick(self):
		for contig_entry in self._contig_list:
			print(contig_entry.name)
			self._write_matches(contig_entry)

	def _write_matches(self, contig_entry):
		for primer in self._primer_list:
			hit_list = self._find_match(contig_entry, primer)
			if hit_list:
				self._write_lines(contig_entry, primer, hit_list)

	def _write_lines(self, contig, primer, hit_list):
		'''
		@summary: create entry for each hit
		'''
		for hit in hit_list:
			print('found: %s'%(primer.name))
			start       = hit[1]
			end         = hit[2]
			length      = end-start
			contig_name = contig.name 
			primer_name = primer.name
			requested   = primer.sequence
			located     = hit[0]
			line        = [contig_name, primer_name, start, end, length, requested, located]
			line        = [str(e) for e in line]
			with open(self._result_file, 'a') as stream:
				stream.write('%s\n'%(';'.join(line)))
    
	def _find_match(self, contig_entry, primer):
		text = contig_entry.sequence
		compiled_pattern = re.compile(r'(%s)'%(primer.sequence))
        
		hits = []
		for m in compiled_pattern.finditer(text):
			if m.group():
				start, end = m.span()
				hits.append((m.group(), start, end))
		return hits


if __name__ == '__main__':
	foo = contig_reader('./data/test_sequences.txt')
	primer_folder = './data/primer/'
	primer_files = glob.glob("./data/primer/*.csv")
	
	for primer_file in primer_files:
		bar = primer_reader(primer_file)
		dst_folder_name = 'hits_' + os.path.basename(primer_file)
		chucky = chuck_norris(foo.get_contigs(), bar.get_primer(), dst_folder_name)
		chucky.roundhousekick()
	print('runtime: ', time.process_time())
	print('done.')
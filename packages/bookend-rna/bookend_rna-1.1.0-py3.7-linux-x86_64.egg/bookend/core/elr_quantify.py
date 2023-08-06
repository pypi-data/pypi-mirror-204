import sys
import time
import os
import gzip
import bookend.core.cython_utils._rnaseq_utils as ru
from bookend.core.cython_utils._assembly_utils import Locus
from bookend.core.elr_sort import ELRsorter

class ELRquantifier:
    def __init__(self, args):
        """Parses input arguments for assembly"""
        self.args = args
        self.output = self.args['OUT']
        self.genome = self.args['GENOME']
        self.input = self.args['INPUT']
        self.allow_unstranded = self.args['UNSTRANDED']
        self.sort = self.args['SORT']
        self.sorter = ELRsorter(self.args)
        self.sorter.sort()
        self.elr_file = self.sorter.output
        self.elr = open(self.elr_file, 'r')
        self.output_file = open(self.output, 'w')
        self.dataset = ru.AnnotationDataset(
            annotation_files=self.input, 
            reference=None, 
            genome_fasta=self.genome, 
            config=ru.config_defaults, 
            gtf_config=ru.gtf_defaults, 
            gff_config=ru.gff_defaults
        )
        self.dataset.source_array = ['', 'bookend']
        self.locus_counter = 0
        self.new_gene_counter = 0
        self.input_transcripts
    
    def quant(self, locus):
        """Quantifies the expression of a locus."""
        pass


if __name__ == '__main__':
    from argument_parsers import quantify_parser as parser
    args = vars(parser.parse_args())
    obj = ELRquantifier(args)
    sys.exit(obj.run())

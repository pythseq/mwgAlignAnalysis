#!/usr/bin/env python
""" 
comparatorRepeatsWrapper.py
dent earl, dearl (a) soe ucsc edu
3 November 2011

Simple wrapper to perform an evaluation
using mafComparator and bed files for repeat 
annotations
"""
##################################################
# Copyright (C) 2009-2011 by
# Dent Earl (dearl@soe.ucsc.edu, dentearl@gmail.com)
# ... and other members of the Reconstruction Team of David Haussler's
# lab (BME Dept. UCSC)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
##################################################
import lib.libComparator as libComparator
import lib.libWrapper as libWrapper
from optparse import OptionParser
import os
import sys

def callEvaluation(options):
   annots = libComparator.getAnnots('repeats', options)
   cmds = []
   for t in ['MRCA', 'MRCAnp', 'ROOT', 'ROOTnp']:
      filename = 'comparator%sRepeats.xml' % t
      if os.path.exists(os.path.join(options.outDir, filename)):
         # these four analyses can take a long time to run, crashes should not force an entire restart,
         # just a partial restart. This conditional allows analysis checkpointing.
         continue
      cmd = libComparator.basicCommand(filename + '.tmp', 'truth%s' % t, options)
      cmd.append('--bedFiles=%s' % ','.join(annots))
      cmds.append(cmd)
      cmds.append(libComparator.moveCommand(os.path.join(options.outDir, filename + '.tmp'), 
                                            os.path.join(options.outDir, filename)))
   libWrapper.runCommands(cmds, os.curdir)
   libWrapper.recordCommands(cmds, os.path.join(options.outDir, 'commands.txt'))

def main():
   usage = ('usage: %prog location/ pred.maf set.reg.tab tempDir/ outDir/\n\n'
            '%prog takes five arguments, the path to the package set, the path\n'
            'to the predicted maf, the path to the registry file, the\n'
            'path to the temporary directory and the path to the output directory.')
   parser = OptionParser(usage)
   libComparator.initOptions(parser)
   options, args = parser.parse_args()
   libWrapper.checkOptions(options, args, parser)
   
   libWrapper.parseRegistry(os.path.basename(sys.argv[0]), options)
   if os.path.basename(sys.argv[0]) not in options.reg['evaluations']:
      sys.exit(0)
   
   callEvaluation(options)

if __name__ == '__main__':
   main()


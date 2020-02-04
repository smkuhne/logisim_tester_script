#!/usr/bin/env python3

import os
import sys
import re

if len(sys.argv) != 2:
    print("Usage: ./tester.py lab_num")

cwd = os.getcwd()

try:
    with open('logisim_tests', 'r') as tests:
        testVecs = tests.read().split('\n')

        with open('tester/{}tester.circ'.format(sys.argv[1]), 'r+') as toTest:
            content = toTest.read()

            if not re.match(r'<lib.+name="12"[/]>', content):
                content = content.replace('<lib desc="#Logisim ITA components" name="11"/>',
                    '<lib desc="#Logisim ITA components" name="11"/>\n  <lib desc="file#{}/base/{}.circ" name="12"/>'.format(cwd, sys.argv[1]))

            if not re.match(r'<comp lib="12".+/>', content):
                try:
                    index = content.index('</circuit>')


                    if int(sys.argv[1]) >= 1 and int(sys.argv[1]) <= len(testVecs):
                        content = content[:index] + '  {}\n  '.format(testVecs[int(sys.argv[1]) - 1]) + content[index:]
                    else:
                        print('Invalid test number')

                except ValueError:
                    print('Invalid logisim file')

            toTest.seek(0)
            toTest.write(content)
            toTest.truncate()

            os.system('mkdir -p results')
            os.system('java -jar logisim-evolution.jar tester/{}tester.circ -tty table > results/{}output.tsv'.format(sys.argv[1], sys.argv[1]))
            os.system('diff results/{}output.tsv tsv/{}.tsv'.format(sys.argv[1], sys.argv[1]))
except IOError:
    print('Encountered an error trying to check your files.')

#
#  Program to convert questionnaries in CSV format to YAML format
#
#  Questionary Copyright (c) 2021 Carlos Pardo
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import os
import codecs
import csv
import yaml


def main():
   """Main program"""

   for filename in os.listdir('.'):
       if filename[-4:].lower() != '.csv':
           continue
       questions = read_csv(filename)[1:]
       for block_name, block_questions in extract_block(questions):
           write_yaml(block_name, block_questions)

   questions = read_csv('bancoTecno_es.csv')
   for block_name, block_questions in extract_block(questions):
       write_yaml(block_name, block_questions)


def extract_block(questions):
    block_names = []
    for question in questions:
        if not question['Block'] in block_names:
            block_names.append(question['Block'])
    for block_name in block_names:
        block_questions = [question for question in questions if question['Block'] == block_name]
        yield(block_name, block_questions)
   


def read_csv(filename):
   with codecs.open(filename, encoding='utf-8') as csvfile:
      csv_questions = [question for question in csv.reader(csvfile, delimiter=',')]
   questions = []
   for question in csv_questions:
      questions.append( {
         'Question': question[0],
         'Image': question[1],
         'Choices': question[2:6],
         'Block': question[6],
         } )
   return questions[1:]



def write_yaml(block_name, questions):
   print(block_name)
   print(len(questions))
   yamldata = ['\nCategory: Electricity\nTitle: %s\nAuthor: Tucho Méndez\nShow_max: 0\n\n---\n\n' % (block_name)]
   for row in questions:
      yamldata.append(
         '- Question: "' + str(row['Question']) + '"\n' +
         '  Image: "' + str(row['Image']) + '"\n' +
         '  Choices:\n'
         '    - "' + str(row['Choices'][0]) + '"\n' +
         '    - "' + str(row['Choices'][1]) + '"\n' +
         '    - "' + str(row['Choices'][2]) + '"\n' +
         '    - "' + str(row['Choices'][3]) + '"\n'
         )
   with codecs.open('electric-' + block_name + '.yaml', 'w', encoding='utf-8') as yamlfile:
      pass
      yamlfile.write('\n'.join(yamldata))



main()

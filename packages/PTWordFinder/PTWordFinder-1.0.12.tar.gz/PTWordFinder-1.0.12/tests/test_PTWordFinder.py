import os
import subprocess
import sys
import pytest
from unittest import mock

from unittest.mock import Mock

from ptwordfinder.commands.PTWordFinder import calculate_words
from ptwordfinder.commands.PTWordFinder import nonblank_lines
from click.testing import CliRunner

# Functional test
path="ptwordfinder/commands/"

def test_help():
    exit_status = os.system(f'python3 {path}PTWordFinder.py --help')
    assert exit_status == 0
    
#Unit tests 
#  
@pytest.mark.parametrize(('files, lines, words, time'),
 [
     pytest.param('tests/pan-tadeusz-czyli-ostatni-zajazd-na-litwie.txt', 'Number of lines : 9513',
     'Found: 166 words', 'Time elapsed: 0.1 second',  marks=pytest.mark.xfail(reason="some bug")),
    ('tests/test-file.txt', 'Number of lines : 4',
     'Found: 6 words', 'Time elapsed: 0.0 second'),
],
)
def test_calculate_words(files, lines, words, time):
    ln = lines
    runner = CliRunner()
    result = runner.invoke(calculate_words, ['tests/words-list.txt', files])
    assert result.exit_code == 0      
    assert result.output == (f"{lines}\n"
                                f"{words}\n"
                                f"{time}\n")
    
def test_nonblank_lines_for_multilines():

    # given

    # multiline string
    # multiple spaces ale skipped
    # empty line not counting
    # specjal charakter not conting
    first_line = 'bb bbb, bbb       '
    second_line = "    ...   "
    third_line = "  dd d d  (ddd)   d      \n"

    text='\n'.join((first_line,second_line,third_line))

    filename ='test-file'
 
    text_data = mock.mock_open(read_data=text)
     
    with mock.patch('%s.open' % __name__,text_data, create=True):
        f = open(filename)
        
    #when
        print(f)
        result = nonblank_lines(f)
        result=list(result)
    
    #then        
    expected_text =[['bb', 'bbb', 'bbb'],[''],['dd', 'd', 'd','ddd','d']]    
    assert result ==  expected_text
 

def test_nonblank_lines_for_one_line():
    #given

    # one line string
    filename ='test-file'
    text= '     bb bbb, bbb,       '


    #when     
    text_data = mock.mock_open(read_data=text)
    
    with mock.patch('%s.open' % __name__,text_data, create=True):
        f = open(filename)
        
        result = nonblank_lines(f)
        result=list(result)

    #then
        expected_text = [['bb', 'bbb', 'bbb']]
    
        assert result ==  expected_text

if __name__ == "__main__":
    sys.exit(calculate_words(sys.argv))     

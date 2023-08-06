import time
import click
import re


@click.command()
@click.argument('words_input_file', type=click.File('r'))
@click.argument('searched_file', type=click.File('r'))
def calculate_words(words_input_file, searched_file):
    """ count specific word in "Pan Tadeusz" poem """

    # Open the list of words
    # for which we want to count the occurrence
    #  in the text of the book "Pan Tadeusz"
    file = words_input_file.readlines()

    word_list = [elt.strip() for elt in file]

    word_set = set(word_list)

    counter = 0
    word_counter = 0

    start_time = time.time()

    # calculate total number for lines and words
    for line in nonblank_lines(searched_file):
        # empty lines are not count
        if not '' in line:
            counter += 1
        
        for word in line:
            if word in word_set:
                word_counter += 1

    stop_time = time.time()

    print("Number of lines : %d" % counter)
    print("Found: %d words" % word_counter)
    print("Time elapsed: %.1f second" % (stop_time - start_time))


def nonblank_lines(text_file):
    """[summary]
    
    Function to erase blank lines from begin and end of string. 
    it also remove all nonalphanumerical characters, 
    but exclude spacex character

    Input: any string text from opened file

    Arguments:
    text_file {String} -- the contents of the file

    Yields:
    List with string elements  -- Lines of text (poem)
    example : ['word','','word']
    """ 
    
    stripped=''

    for lines in text_file:
        line = lines.strip()
        # split line only by one space multiple spaces are skipped in the list
        text = re.split(r'\s{1,}',line)
        stripp=[]
        for item in text:
            stripped=  ''.join(ch for ch in item if (ch.isalnum()))
            
            stripp.append(stripped)
        
        if stripp:
            yield stripp
###############################################
'''''
CMPUT 501, ASG 1
Authors: Mohammad Karimiabdolmaleki, Ali Zamani
CCIDs: karimiab, azamani1
'''''
###############################################
# Importing Prerequisites
import re
import csv
import sys

from os import listdir
from os.path import isfile, join

###############################################
# Section 1: Defining Time Intervals

# List of all intervals (day, week)
intervals = [
    '[wW]eek', '[sS]eason', '[dD]ay', '[yY]ear', '[hH]our', '[mM]inute',
    '[mM]onth', '[nN]oon', '[tT]oday', '[yY]esterday', '[tT]omorrow', '[tT]ime',
    '[dD]ecade', '[aA]fternoon', '[mM]orning', '[eE]vening', '[mM]idnight',
]

# Converting the list of intervals into the string format requird for RE
intervals = '|'.join(intervals)

# List of all days of the week (Mon, Fr)
day_of_week = ['[mM]on(?:day)?', '[tT]ue(?:sday)?', '[wW]ed(?:nesday)?',
               '[wW]ednesday', '[tT]hu(?:rsday)?', '[fF]r(?:iday)?',
               '[sS]at(?:urday)?', '[sS]un(?:day)?'
               ]
# Converting the list of day_of_week into the string format requird for RE
day_of_week = '|'.join(day_of_week)

# List of all deictics (next, last)
deictic = ['[aA]go', '[lL]ater', '[nN]ext', '[lL]ast',
           '[bB]efore', '[aA]fter', '[aA]go', '[pP]rior',
           '[eE]arlier'
           ]
# Converting the list of deictics into the string format requird for RE
deictic = '|'.join(deictic)

# List of all seasons (Fall, fall)
seasons = ['[sS]pring', '[sS]ummer', '[fF]all',
           '[aA]utumn', '[wW]inter',
           ]
# Converting the list of seasons into the string format requird for RE
seasons = '|'.join(seasons)

# List of all numbers (One, two)
numbers = ['[oO]ne', '[tT]wo', '[tT]hree',
           '[fF]our', '[fF]ive', '[sS]ix',
           '[sS]even', '[eE]igth', '[nN]ine',
           '[tT]en', '[Ee]leven', '[Tt]welve',
           '[Tt]hirteen', '[Ff]ourteen', '[Ff]ifteen',
           '[Ss]ixteen', '[Ss]eventeen', '[Ee]ighteen',
           '[Nn]ineteen', '[Tt]wenty', '[Mm]any',
           '[Ss]ome', '[Aa] few', '[Ff]ew',
           '[Aa] couple of', '1st', '2nd',
           '3rd', '[4-9]th', '[mM]any'
           ]
# Converting the list of numbers into the string format requird for RE
numbers = '|'.join(numbers)

# List of all possible months (Jan, Feb)
month = ['[jJ]an(?:uary)?', '[fF]eb(?:ruary)?',
         '[mM]ar(?:ch)?', '[aA]pr(?:il)?',
         '[mM]ay', '[jJ]un(?:e)?',
         '[jJ]ul(?:y)?', '[aA]ug(?:ust)?',
         '[sS]ep(?:tember)?', '[sS]ept',
         '[oO]ct(?:ober)?', '[nN]ov(?:ember)?',
         '[dD]ec(?:ember)?'
         ]
# Converting the list of months into the string format requird for RE
months = '|'.join(month)


###############################################

###############################################
# Section 2: Defining search_regex Function

def search_regex(text, name_of_file):
    '''
    Applies several RE patterns on the input text and returns the match and the offset
    Input:
    - text: the text file
    - name_of_file: name of the input file
    Output:
    - match_list: result of the matched pattern on the input text
    '''
    match_list = []
    type_list = []
    reg_list = []

    # 1st Pattern
    '''
    Name: Year
    Instance: 1996 and 2021
    '''
    reg_list.append(re.compile('(\s1\d{3}|20[0-3]\d)s*'))
    type_list.append('year')

    # 2nd Pattern
    '''
    Name: Month
    Instance: September, Sep, Sept
    '''
    reg_list.append(re.compile('\s({})\s'.format(months)))  # ('month') e.g. april-July-Aug
    type_list.append('month')

    # 3rd Pattern
    '''
    Name: day of week
    Instance: fr, Friday
    '''
    reg_list.append(re.compile('\s(?:{})\s'.format(day_of_week)))
    type_list.append('day_of_week')

    # 4th Pattern
    '''
    Name: decade
    Instance: 1960s
    '''
    reg_list.append(re.compile('(\s?(?:1\d\d\d|20[0-3]\d)s)'))
    type_list.append('decade')

    # 5th Pattern
    '''
    Name: season
    Instance: winter
    '''
    reg_list.append(re.compile('\s+(?:{})\s+'.format(seasons)))
    type_list.append('season')

    # 6th Pattern
    '''
    Name: relative year
    Instance: before 1996
    '''
    reg_list.append(re.compile('((?:{})[\s-]?(?:1\d\d\d|20[0-3]\d)s*)'.format(deictic)))
    type_list.append('year_relative')

    # 7th Pattern
    '''
    Name: relative intervals
    Instance: jun last month
    '''
    reg_list.append(re.compile('(?:{})?\s*(?:{})?\s*(?:{})\s*'.format(months, deictic, intervals)))
    type_list.append('month, intervals_relative')

    # 8th Pattern
    '''
    Name: day and month
    Instance: 2 oct 2021
    '''
    reg_list.append(re.compile('\s(?:[01]?\d|2\d|3[0-1])(?:\-|\s+)?(?:{})'.format(months)))
    type_list.append('day_and_month')

    # 9th Pattern
    '''
    Name: month and year
    Instance: jun 96
    '''
    reg_list.append(re.compile('\s(?:{})(?:\-|\s)?(?:\d\d)\s'.format(months)))
    type_list.append('month_and_year')

    # 10th Pattern
    '''
    Name: day month year
    Instance: 12/10/2021
    '''
    reg_list.append(re.compile(
        '((?:[01]?\d|2\d|3[0-1])(?:\-|\/|\s)(?:0?\d|1[012])(?:\-|\/|\s)(?:1\d\d\d|20[0-3]\d))'))
    type_list.append('day(dd)(-/ )month(mm)(-/ )year(yyyy)')

    # 11th Pattern
    '''
    Name: year month day
    Instance: 2021/10/12
    '''
    reg_list.append(re.compile(
        '((?:1\d\d\d|20[0-3]\d)(?:\-|\/|\s)(?:0?\d|1[012])(?:\-|\/|\s)(?:[01]?\d|2\d|3[0-1]))'))
    type_list.append('year(yyyy)(-/ )month(mm)(-/ )day(dd)')

    # 12th Pattern
    '''
    Name: month day yaer
    Instance: 10/12/2021
    '''
    reg_list.append(re.compile(
        '((?:0?\d|1[012])(?:\-|\/|\s)(?:[01]?\d|2\d|3[0-1])(?:\-|\/|\s)(?:1\d\d\d|20[0-3]\d))'))
    type_list.append('month(mm)(-/ )day(dd)(-/ )year(yyyy)')

    # 13th Pattern
    '''
    Name: from/since year
    Instance: from 2020 to 2021, since 1880
    '''
    reg_list.append(re.compile('((?:[Ff]rom|[Ss]ince)\s[1-2][09]\d\d(?:\s(?:until|to)\s[1-2][09]\d\d)?)'))
    type_list.append('from_since_year')

    # 14th Pattern
    '''
    Name: day and month year
    Instance: 2 sep 2021
    '''
    reg_list.append(re.compile(
        '((?:[01]?\d|2\d|3[0-1])(?:\-|\s*)?(?:{})(?:\-|\s*)?(?:1\d\d\d|20[0-3]\d))'.format(months)))
    type_list.append('day_and_month year')

    # 15th Pattern
    '''
    Name: month and month
    Instance: apr-jun
    '''
    reg_list.append(re.compile('((?:{0})-(?:{0}))'.format(months)))
    type_list.append('month_and_month')

    # 16th Pattern
    '''
    Name: preposition intervals relative
    Instance: at this time, by this afternoon
    '''
    reg_list.append(re.compile('((?:[Aa]t|[Bb]y)?\s(?:[Tt]his|[Tt]hat|[Nn]ext)\s(?:{}))'.format(intervals)))
    type_list.append('prep_intervals_relative')

    # 17th Pattern
    '''
    Name: preposition intervals 
    Instance: at this time, by this afternoon
    '''
    reg_list.append(re.compile('((?:{})\s(?:{})\s(?:{}))'.format(numbers, intervals, deictic)))
    type_list.append('prep_intervals')

    # 18th Pattern
    '''
    Name: the day after/before tomorrow/yesterday
    Instance: the day after tomorrow
    '''
    reg_list.append(re.compile('((?:[Tt]he day)\s(?:before|after)\s(?:yesterday|tomorrow))'))
    type_list.append('before_after_y_t')

    for i, p in enumerate(reg_list):
        for m in p.finditer(text):
            match_list.append([name_of_file, type_list[i], m.group(), m.start(), m.span()])

    # delete short spans
    spans = [x[4] for x in match_list]
    idxs = set()
    for j, large in enumerate(spans):
        for i, small in enumerate(spans):
            if small[0] >= large[0] and small[1] <= large[1] and i != j:
                idxs.add(i)
    for idx in sorted(list(idxs), reverse=True):
        del match_list[idx]

    return match_list


###############################################

###############################################
# Section 3: Combining All Functions and Producing the Output

def main():
    '''
    The primary function which calls the other procedures.
    Input:
    -None
  	Output:
    -The final CSV file
    '''

    fields = [['article_id', 'expr_type', 'value', 'char_offset', 'temp']]

    # the second argument of the input command, from the user (data/dev)
    directory_input = sys.argv[1]

    # the third argument of the input command, from the user, the output path
    directory_output = sys.argv[2]

    # appending all .txt files names into the list
    fname_list = [file_name for file_name in listdir(directory_input) if isfile(join(directory_input, file_name))]

    # applying the search_regex module to all of the text files, one by one
    for fname in fname_list:
        with open(join(directory_input, fname), encoding='unicode_escape') as txt_file:
            text = txt_file.read()
            fields.extend(search_regex(text, fname))

    # dropping the span (not required as mentioned in the instructions)
    fields = list(map(lambda x: x[0:4], fields))

    # saving the output csv file into the specified directory
    with open(directory_output, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(fields)


if __name__ == "__main__":
    main()
    print('Process Finished!')

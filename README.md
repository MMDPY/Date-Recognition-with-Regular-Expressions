# Intro to NLP - Assignment 1

## Team
|Student name| CCID |
|------------|------|
|student 1   |  karimiab    |
|student 2   |  azamani1    |


## Installation and Execution Instructions
- Clone the repository
- Open a terminal inside the cloned folder (the folder should consist of src, output, data, and README.md)
- No third-party library are required. All of the imported libraries are part of Python's Standard Library (re, sys, os, csv)
- Run the command ```python3 src/main.py data/dev/ output/dev.csv``` from the terminal
- The output can be found inside [output](output)

## Run
```bash
python3 src/main.py data/dev/ output/dev.csv
```

## Data

The data can be found inside [data/dev](data/dev).



## Introduction
In this tutprial we will explore the use of regular expressions to extract information from written text. This method has been widely applied in information retrieval, and it is used in text processing applications and research.

A regular expression is a notation used to match strings in a text. It works like the CTRL+F search feature in browsers, but it has the added bonus of allowing the use of special characters to count, exclude, and group specific strings. Like in a language, regular expressions have a set of characters with predefined functions, and these characters can be used to create search patterns. For example, the character + means one or more occurrences. The regular expression /e+/ searches for strings of one or more “e”s. In the string “Feed the Birds”, this regular expression would match “ee”.
## Task
In this project we are going to use regular expressions to search for date expressions in news texts. We are interested in two types of date expressions. The first one is simple date expressions, strings like “14 June 2019” and “Fall 2020” which represent absolute points in time and are independent of when you are reading them. The second type is deictic date expressions, dates that are relative to the current time, for example, “the day before yesterday”, “next Friday”, and “two weeks prior”.
## Input: news articles
News is a genre that makes use of dates to convey more information about when an event took place and to help the readers place future and past occurrences in time. The input dataset is a collection of news articles that discusses several topics, such as politics, tech, and business. 

Article 265 in this dataset has sentences like this:

“Pipa conducted the poll from 15 November 2004 to 3 January 2005 across 22 countries in face-to-face or telephone interviews.”
## Output: CSV file, code, and documentation
## CSV file
As mentioned before, news articles usually have a lot of time references, and we want you to search for those references in the input data. The output of the search is a CSV file with all of the dates expressions found. The file contains four columns, one column for the id of the article, one for the type of date expression found, one for the date expression itself, and one for the offset in characters from the beginning of the file to the beginning of the date expression, that is the position of the first character of the date expression in the file.

- The output is like:
- article_id, expr_type, value, char_offset
- 265.txt, date, 15 November 2004, 30
- 265.txt, date, 3 January 2005, 50


## Useful links
- [This website](https://www.w3schools.com/python/python_regex.asp) has a good overview of the library Python RegEx. It lists the library functions available and regular expression’s metacharacters along with their uses.
- [This post](https://medium.com/factory-mind/regex-tutorial-a-simple-cheatsheet-by-examples-649dc1c3f285) is very useful to look for metacharacters and their applications.
- You may want to test your regular expression before embedding them to your code. [This website](https://regex101.com/) is perfect for that. 
- You may also want to improve the readability of your code by adding comments within a regular expression. The VERBOSE mode in Python provides such functionality, as described [here](https://docs.python.org/3.5/library/re.html#re.X). 

# More information
- Book Chapter: [Chapter 2](https://web.stanford.edu/~jurafsky/slp3/2.pdf)

- Learning Objectives : Learn how to use regular expressions to extract information from text.


This is a solution to Assignment 1 for CMPUT 501 - Intro to NLP at the University of Alberta, created during the Fall 2020 semester.



## TODOs

In this file you **must**:
- [x] Fill out the team table above. Please note that CCID is **different** from your student number.
- [x] Acknowledge all resources consulted (discussions, texts, urls, etc.) while working on an assignment. Non-detailed oral discussion with others is permitted as long as any such discussion is summarized and acknowledged by all parties.
- [x] Provide clear installation and execution instructions that TAs must follow to execute your code.

## Execution
Use the following command in the current directory.

`python3 src/main.py data/dev/ output/dev.csv`

## Data

The assignment's development data can be found inside [data/dev](data/dev).

# -*- coding: utf-8 -*-

import re
import string
import itertools as it
from factcreator import factsLinksProcessing

def extract(text, fact):
    for sub in fact.substrs:
        if text.find(sub) != -1:
            return True

def processText(rawText):
    text = re.sub('<[^>]*>', '', rawText)
    text = text.lower()
#    table = string.maketrans(string.punctuation, ' '*len(string.punctuation))
    table = dict((ord(char), u' ') for char in string.punctuation)#it.chain(string.punctuation, string.whitespace))
    return text.translate(table)

def extractAll(rawText, factStorage, backFacts):
    text = processText(rawText)

    approvedFacts = set()
    for fact in factStorage:
        if extract(text, fact):
            approvedFacts.add(fact.name)

    approvedFacts = factsLinksProcessing(approvedFacts, backFacts)

    return approvedFacts

def extractSalary(salaryText):
    sr = re.findall(u'(\d+)\s*\-\s*(\d+)\s*(грн|\$|USD)', salaryText, re.U)
    if len(sr) != 0:
        return sr[0]
    sr = re.findall(u'от\s*([\d\s]+)\s*до\s*([\d\s]+)\s*(грн|\$|USD)', salaryText, re.U)
    if len(sr) != 0:
        return sr[0]
    sr = re.findall(u'([\d\s]+)\s*(грн|\$|USD)', salaryText, re.U)
    if len(sr) != 0:
        return sr[0]
    return None

# -*- coding: utf-8 -*-

import cjson as json

from factData import FactData

from jobinator.models import DBSession, Fact, FactLinks, FACT_TYPE_BOOL, FACT_TYPE_NUMBER

def loadFactLinksFromDatabase():
    return DBSession.query(FactLinks).filter(Fact.type == FACT_TYPE_BOOL)

def loadFactsFromDatabase():
    return DBSession.query(Fact).all()

def createFactStorage():
    factStorage = []
    for f in loadFactsFromDatabase():
        factStorage.append(FactData(f.name, json.decode(f.args)))
    return factStorage

def backFactLinksProcessing():
    backFacts = dict()
    for factLink in loadFactLinksFromDatabase():
        fl = json.decode(factLink.args)
        for i in fl:
            backFacts.setdefault(i, [])
            backFacts[i].append(factLink.name)
    return backFacts

def factsLinksProcessing(factSet, backFacts):
    changed = True
    while changed:
        changed = False
        temporary = set()
        for f in factSet:
            if f in backFacts:
                temporary.update(backFacts[f])

        previousLength = len(factSet)
        factSet.update(temporary)
        if previousLength != len(factSet):
            changed = True

    return factSet
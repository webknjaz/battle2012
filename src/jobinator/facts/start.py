# -*- coding: utf-8 -*-

from factcreator import createFactStorage, backFactLinksProcessing
from simpleextractor import extractAll, extractSalary, processText

from jobinator import config
from jobinator.models import DBSession, Fact, FactLinks, FactData, ScrapedData, Setting, FACT_TYPE_BOOL, FACT_TYPE_NUMBER
import transaction

import re
import cjson as json


def initializeBase(configPath, basePath):
    config.load_config(configPath, basePath)

def saveFactsToDatabase(docid, facts, intFacts):
    data = FactData()
    data.scraped_data_id = docid
    for fact in facts:
        setattr(data, fact, True)
    for name, value in intFacts:
        setattr(data, name, value)
    DBSession.add(data)
    transaction.commit()

def getLastScrappedDocId():
    lastId = DBSession.query(Setting.value).filter(Setting.key == u'lastFactorizedDocId').all()
    if len(lastId) == 0:
        DBSession.add(Setting(key = u'lastFactorizedDocId', value = u'0'))
        transaction.commit()
        return 0
    else:
        return int(lastId[0][0])

def putLastScrappedDocId(lastId):
    DBSession.query(Setting.value).filter(Setting.key == u'lastFactorizedDocId').update({u'value': unicode(lastId)})
    transaction.commit()

def parse():
    lastId = getLastScrappedDocId()
    factStorage = createFactStorage()
    backFacts = backFactLinksProcessing()
    newLastId = lastId
    for newLastId, url, rawText, title, data in DBSession.query(ScrapedData.pk, ScrapedData.url, ScrapedData.preview, ScrapedData.title, ScrapedData.data).filter(ScrapedData.pk > lastId).order_by(ScrapedData.pk):#.limit(10):
        facts = extractAll(rawText, factStorage, backFacts)
        facts.update(extractAll(title, factStorage, backFacts))
        #print url, facts

        data = json.decode(data)
        salaryFact = []
        if 'salary' in data:
            salary = extractSalary(data['salary'])
            if salary is not None:
                if len(salary) == 2:
                    try:
                        salaryCount = int(re.sub('\s*', '', salary[0], 0, re.U))
                    except ValueError, x:
                        salaryCount = 0
                    if salary[1].strip() == '$' or \
                            salary[1].strip().lower() == 'usd':
                        salaryCount *= 8
                    salaryFact.append(('salary_from', salaryCount))
                elif len(salary) == 3:
                    try:
                        salaryFrom = int(re.sub('\s*', '', salary[0], 0, re.U))
                        salaryTo = int(re.sub('\s*', '', salary[1], 0, re.U))
                    except ValueError:
                        salaryFrom = 0
                        salaryTo = 0
                    if salary[2].strip() == '$' or\
                       salary[2].strip().lower() == 'usd':
                        salaryFrom *= 8
                        salaryTo *= 8
                    salaryFact.append(('salary_from', salaryFrom))
                    salaryFact.append(('salary_to', salaryTo))

        saveFactsToDatabase(newLastId, facts, salaryFact)
    putLastScrappedDocId(newLastId)

def uploadFacts():
    import sys
    from factCodeBase import facts, factLinks

    initializeBase(sys.argv[1], sys.argv[2])
    for key, value in facts.items():
        DBSession.add(Fact(name=unicode(key), type=FACT_TYPE_BOOL, args=unicode(json.encode(value))))

    for key, value in factLinks.items():
        DBSession.add(FactLinks(name=unicode(key), args=json.encode(value)))

    transaction.commit()

def start():
    import sys
    initializeBase(sys.argv[1], sys.argv[2])
    parse()

if __name__ == '__main__':
    start()

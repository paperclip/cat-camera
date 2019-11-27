#!/bin/env python

import json

from . import findIndex

def generate_roc_data(actuallyCatResults, actuallyNotCatResults):
    actuallyCatResults.sort()
    actuallyNotCatResults.sort()
    
    results = []

    actualCatsDivisor = 0
    notCatsDivisor = 0

    for n in range(1,99):
        actualCatsDivisor = findIndex.findIndex(actuallyCatResults, n / 100, actualCatsDivisor)
        falseNegative = actualCatsDivisor / len(actuallyCatResults)
        truePositive = 1 - falseNegative
        print("+", n, actualCatsDivisor, falseNegative, truePositive)

        notCatsDivisor = findIndex.findIndex(actuallyNotCatResults, n / 100, notCatsDivisor)
        trueNegative = notCatsDivisor / len(actuallyNotCatResults)
        falsePositive = 1 - trueNegative
        print("-", n, notCatsDivisor, trueNegative, falsePositive)

        results.append((falsePositive, truePositive))

    return results

#!/bin/env python

import json

try:
    from . import findIndex
except ImportError:
    import findIndex

def generate_roc_data(actuallyCatResults, actuallyNotCatResults):
    actuallyCatResults.sort()
    actuallyNotCatResults.sort()

    divisor = 100.0
    if actuallyCatResults[-1] > 1.0 or actuallyNotCatResults[-1] > 1.0:
        print("Assuming data is percentages")
        divisor = 1.0

    results = []

    actualCatsDivisor = 0
    notCatsDivisor = 0

    for n in range(1,99):
        actualCatsDivisor = findIndex.findIndex(actuallyCatResults, n / divisor, actualCatsDivisor)
        falseNegative = actualCatsDivisor / len(actuallyCatResults)
        truePositive = 1 - falseNegative
        print("+", n, actualCatsDivisor, falseNegative, truePositive)

        notCatsDivisor = findIndex.findIndex(actuallyNotCatResults, n / divisor, notCatsDivisor)
        trueNegative = notCatsDivisor / len(actuallyNotCatResults)
        falsePositive = 1 - trueNegative
        print("-", n, notCatsDivisor, trueNegative, falsePositive)

        results.append((falsePositive, truePositive))

    return results


import json
import os
import sys

try:
    from . import generate_roc_data
except ImportError:
    import generate_roc_data


def main(argv):
    actuallyCatResults = json.load(open("actuallyCatResults.json"))
    actuallyNotCatResults = json.load(open("actuallyNotCatResults.json"))

    results = generate_roc_data.generate_roc_data(actuallyCatResults, actuallyNotCatResults)
    open("roc.json","w").write(json.dumps(results))

if __name__ == "__main__":
    sys.exit(main(sys.argv))

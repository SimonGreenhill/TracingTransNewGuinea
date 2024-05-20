import csvw

def getcsv(filename, delimiter=","):
    """Reads a CSV file"""
    with csvw.UnicodeDictReader(filename, delimiter=delimiter) as reader:
        for row in reader:
            yield(row)


def get_concepticon_label(concepticon_id, concepticon_gloss):
    concepticon_gloss = concepticon_gloss.replace(" ", "_").replace("(", "").replace(")", "")
    return "%s_%s" % (concepticon_id, concepticon_gloss)


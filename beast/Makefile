
python = ../.env/bin/python3
pypy = ../automated_cognates/pypyenv/bin/pypy

DATASETS=../automated_cognates/transnewguinea_tng_combined.infomap.nex

DETAILS = $(patsubst %.nex, %.csv, $(notdir $(DATASETS)))
NEXUS_ASC = $(patsubst %.nex, %.asc.nex, $(notdir $(DATASETS)))
NEXUS_ASCWORDS = $(patsubst %.nex, %.words.nex, $(notdir $(DATASETS)))

all: $(DETAILS) $(NEXUS_ASC) $(NEXUS_ASCWORDS) $(LOCATIONS)

%.csv: ../automated_cognates/%.nex
	$(pypy) ./get_details.py ../data/details.csv $< $@

%.asc.nex: ../automated_cognates/%.nex
	$(python) ../bin/add_ascertainment_to_nexus.py overall $< -o $@

%.words.nex: ../automated_cognates/%.nex
	$(python) ../bin/add_ascertainment_to_nexus.py words $< -o $@

## clean: removes auto-generated files
.PHONY: clean
clean:
	rm *.nex *.xml *.csv


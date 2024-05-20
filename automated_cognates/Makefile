#NOTE we use pypy here as it speeds up lingpy by about 2x

python = $(PWD)/../.env/bin/python3
pypy = ./pypyenv/bin/pypy

CLDF=../data/transnewguinea-org/cldf/cldf-metadata.json
REMAP=../data/concepts.csv
CONCEPT_SUBSET=../concepts/concepts.final.csv
IGNORE_LANGUAGES=../data/ignore.csv
SOURCES=../data/sources.csv

AUTOCOGNATES =  transnewguinea_tng.100.infomap.tsv transnewguinea_tng_combined.infomap.tsv

NEXUSES = $(patsubst %.tsv, %.nex, $(AUTOCOGNATES))

all: pypyenv $(AUTOCOGNATES) $(NEXUSES)

pypyenv:
	pypy -m venv pypyenv
	$(pypy) -m pip install --upgrade pip lingpy igraph pylotiger
	$(pypy) -m pip install -e git+https://github.com/SimonGreenhill/NexusMaker.git#egg=nexusmaker

transnewguinea.tsv:
	@$(python) ../bin/extract.py --labelsource $(SOURCES) --ignore $(IGNORE_LANGUAGES) --concepts $(CONCEPT_SUBSET) --remap $(REMAP) $(CLDF) $@

$(DATASETS): transnewguinea.tsv
	@$(python) subset.py --threshold $(word 2, $(subst ., ,$@)) $< $@ > $(patsubst %.tsv, %.log, $@)

%.check: %.tsv
	@python check.py $(CONCEPT_SUBSET) $< | tee $@

transnewguinea_tng.100.infomap.tsv: ../data/transnewguinea_tng.remapped.tsv
	@$(python) subset.py --threshold 100 $< transnewguinea_tng.100.tsv > $(patsubst %.tsv, %.log, $@)
	$(pypy) ../bin/autocognates.py --method=infomap transnewguinea_tng.100.tsv $@

transnewguinea_tng_combined.infomap.tsv: ../data/transnewguinea_tng_combined.remapped.tsv
	@$(python) subset.py --threshold 100 $< transnewguinea_tng_combined.100.tsv > $(patsubst %.tsv, %.log, $@)
	$(pypy) ../bin/autocognates.py --method=infomap transnewguinea_tng_combined.100.tsv $@

%.nex: %.tsv
	$(pypy) to_nexus.py $< $@


## clean: removes auto-generated files
.PHONY: clean
clean:
	rm -rf *.tsv *.check *.nex *.csv *.log

# debugging helper to show target. Run make print-VARNAME
print-%  : ; @echo $* = $($*)

GLOTTOLOG_VERSION=v4.7

SUBSETS = abbott1985              \
	clouse-1997                   \
	daniels2010                   \
	davies_and_comrie1985         \
	dutton1970                    \
	dutton2010                    \
	dye-et-al-1968                \
	foley2005                     \
	franklin1975                  \
	laycock1968                   \
	mcelhanon-1967                \
	mcelhanon_and_voorhoeve1970   \
	scott1978                     \
	smallhorn-2011                \
	voorhoeve-1971                \
	voorhoeve1980

TSVFILES := $(patsubst %, %.tsv, $(SUBSETS))
TNGFILES := transnewguinea_tng.remapped.tsv transnewguinea_tng_combined.remapped.tsv transnewguinea_combined.remapped.tsv

.PRECIOUS: concepts.csv ignore.csv sources.csv

all: glottolog-cldf transnewguinea-org $(TNGFILES) $(TSVFILES) details.csv

# use $(python) and $(pip)
python = $(PWD)/../.env/bin/python3
pip = $(python) -m pip

#-----------------------------------------------------------------------
# DATA SETUP
#-----------------------------------------------------------------------

## install data
transnewguinea-org:
	git clone https://github.com/lexibank/transnewguineaorg $@

glottolog-cldf:
	git clone https://github.com/glottolog/glottolog-cldf $@
	git --git-dir $@/.git checkout $(GLOTTOLOG_VERSION)

remappings.txt: transnewguinea-org concepts.csv
	@$(python) print_remappings.py > $@

ignore_tngonly.csv: ignore.csv
	cp $< $@
	@$(python) tng_only.py | grep IGNORE >> $@

transnewguinea_tng.remapped.tsv: transnewguinea-org remap.csv cognates.csv ignore_tngonly.csv sources.csv
	@$(python) ../bin/extract.py --labelsource sources.csv --ignore ignore_tngonly.csv --cognates cognates.csv --remap remap.csv --concepts concepts.csv transnewguinea-org/cldf/cldf-metadata.json $@


transnewguinea_tng_combined.remapped.tsv: transnewguinea-org remap.csv cognates.csv ignore_tngonly.csv
	@$(python) ../bin/extract.py --ignore ignore_tngonly.csv --cognates cognates.csv --remap remap.csv --concepts concepts.csv transnewguinea-org/cldf/cldf-metadata.json $@



details.csv: transnewguinea.remapped.tsv
	@$(python) details.py


# subset datasets
%.tsv: transnewguinea-org concepts.csv cognates.csv
	@$(python) ../bin/extract.py \
        --cognates cognates.csv \
        --remap concepts.csv \
         --source $(basename $(notdir $@)) \
        transnewguinea-org/cldf/cldf-metadata.json \
        $@


# debugging helper to show target. Run make print-VARNAME
print-%  : ; @echo $* = $($*)

.PHONY: clean
clean:
	rm *.tsv details.csv
	# do not delete all csv files, some are precious
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

# Accuracy analyses
ACCURACY_TSV_FILES := \
	$(patsubst %, %.lexstat.tsv, $(SUBSETS)) \
	$(patsubst %, %.sca.tsv, $(SUBSETS)) \
	$(patsubst %, %.infomap.tsv, $(SUBSETS)) \
	$(patsubst %, %.turchin.tsv, $(SUBSETS)) \
	$(patsubst %, %.edit-dist.tsv, $(SUBSETS))

ACCURACY_DIFF_FILES := $(patsubst %.tsv, %.diff, $(ACCURACY_TSV_FILES))

AMC_FILES := $(patsubst %, %.amc.csv, $(SUBSETS))

.PRECIOUS: %.tsv %.diff

all: $(ACCURACY_TSV_FILES) $(ACCURACY_DIFF_FILES) $(AMC_FILES) results.md datasets.csv figure-precision_vs_recall.png

# use $(python) and $(pip)
python = $(PWD)/../.env/bin/python3
pip = $(python) -m pip

#-----------------------------------------------------------------------
# accuracy analyses:
#-----------------------------------------------------------------------
%.amc.csv: ../data/%.tsv
	@$(python) ../bin/calculate_amc.py $< > $@

%.lexstat.tsv: ../data/%.tsv
	@$(python) ../bin/autocognates.py --method=lexstat $< $@

%.infomap.tsv: ../data/%.tsv
	@$(python) ../bin/autocognates.py --method=infomap $< $@

%.sca.tsv: ../data/%.tsv
	@$(python) ../bin/autocognates.py --method=sca $< $@

%.edit-dist.tsv: ../data/%.tsv
	@$(python) ../bin/autocognates.py --method=edit-dist $< $@

%.turchin.tsv: ../data/%.tsv
	@$(python) ../bin/autocognates.py --method=turchin $< $@

%.diff: %.tsv
	@$(python) ../bin/bcubes.py $< $@ > $(patsubst %.diff, %.log, $@)

datasets.csv: $(AMC_FILES)
	head -n 1 $< > $@
	awk 'FNR > 1' *.amc.csv >> $@

results.md: $(ACCURACY_DIFF_FILES)
	@$(python) print_results.py > $@

figure-precision_vs_recall.png: datasets.csv results.md
	Rscript figure-accuracy.R

.PHONY: clean
clean:
	rm *.tsv *.log *.diff *.md *.csv *.png

# debugging helper to show target. Run make print-VARNAME
print-%  : ; @echo $* = $($*)


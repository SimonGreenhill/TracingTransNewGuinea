
all: concepts.original.csv concepts.remapped.csv synonyms.original.txt synonyms.remapped.txt effect_of_adding_synonyms.txt

python = $(PWD)/../.env/bin/python3

concepts.original.csv: ../data/transnewguinea.tsv
	$(python) concepts.py $< swadesh200.csv $@ > $(patsubst %.csv,%.unmapped,$@)

concepts.remapped.csv: ../data/transnewguinea.remapped.tsv
	$(python) concepts.py $< swadesh200.csv $@ > $(patsubst %.csv,%.unmapped,$@)

concepts.final.csv:
	echo "create this manually from concepts.remapped.csv"

synonyms.original.txt: ../data/transnewguinea.tsv
	$(python) synonyms.py $< > $@

synonyms.remapped.txt: ../data/transnewguinea.remapped.tsv
	$(python) synonyms.py $< > $@

synonyms.original.final.txt: ../data/transnewguinea.tsv concepts.final.csv
	$(python) synonyms.py --filter concepts.final.csv $< > $@

synonyms.remapped.final.txt: ../data/transnewguinea.remapped.tsv concepts.final.csv
	$(python) synonyms.py --filter concepts.final.csv $< > $@

effect_of_adding_synonyms.txt: synonyms.original.final.txt synonyms.remapped.final.txt
	grep SYNONYMS *.txt > $@

clean:
	rm -rf concepts.original.csv concepts.remapped.csv *.txt

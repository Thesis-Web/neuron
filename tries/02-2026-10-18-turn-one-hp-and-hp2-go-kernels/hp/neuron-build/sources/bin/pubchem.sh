#!/bin/sh
# pubchem.sh Q: grounded source from NEURON-SOURCES, reached with one curl; prints the answer as plain words (first 60), nothing on failure
. /opt/neuron/bin/words.sh
get "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/$1/property/MolecularFormula,MolecularWeight/JSON" | sed 's/<[^>]*>//g' | words 60

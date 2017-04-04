/!/bin/bash
INPUT=ch12-1.csv
OLDIFS=$IFS
IFS=,
[ ! -f $INPUT ] && { ECHO "$INPUT file not found"; exit 99; }
while read english chinese
do
	curl http://fireplaceflashcards.herokuapp.com/api/words -d english=$english -d chinese=$chinese -X POST -v
done < $INPUT
IFS=$OLDIFS

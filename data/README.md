# Files:


* glottolog-cldf/ - CLDF version of glottolog data git repository clone.
* transnewguinea-org/ - TransNewGuinea.org data git repository clone.

* concepts.csv - the list of concepts that will be remapped to maximise phylogenetic signal.

* cognates.csv - this is a list of the cognate sets from transnewguinea.org.
    - these are not stored in the CLDF dataset for various reasons but need to be extracted from
      postgres:
      
         \f ','
         \a
         \o 'cognates.csv'
         SELECT lexicon_id, cognateset_id, source_id, s.slug AS source
          FROM cognates c
             LEFT JOIN sources s ON s.id = c.source_id
          WHERE 
             source_id IS NOT NULL
             AND s.slug != 'ross2014' -- this is unpublished
          ORDER BY cognateset_id
         ;
    
* print_remappings.py -
    prints the concepts that have been remapped from the public clone of transnewguinea-org
    generates remappings.txt

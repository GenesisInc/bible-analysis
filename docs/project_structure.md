# structure

    .
    ├── README.md
    ├── analysis
    │   ├── lifespans
    │   │   ├── README.md
    │   │   ├── lifespan.py
    │   │   └── results
    │   │       ├── chapter_entity_summary.csv
    │   │       ├── entities.csv
    │   │       ├── entities.json
    │   │       ├── lifespans.json
    │   │       ├── word_counts.list
    │   │       └── words.list
    │   ├── occupations
    │   │   └── results
    │   ├── science
    │   │   ├── __init__.py
    │   │   └── data_handler.py
    │   ├── sentiments
    │   │   └── results
    │   └── travel
    │       ├── __init__.py
    │       └── mapper.py
    ├── config
    │   └── book_order.py
    ├── core
    │   ├── nlp_tagger
    │   │   ├── __init__.py
    │   │   ├── bible_search.py
    │   │   ├── lifespan_tagger.py
    │   │   └── tagger.py
    │   ├── translation_loader
    │   │   ├── __init__.py
    │   │   └── translation_manager.py
    │   ├── utils
    │   │   ├── __init__.py
    │   │   ├── file_utils.py
    │   │   ├── reference_utils.py
    │   │   └── text_utils.py
    │   └── visualization
    │       └── visualization.py
    ├── data
    │   ├── Biblical_Travel_Details.csv
    │   ├── input
    │   │   ├── multi_translation.json -> ../../../bible-text/data/tmp/multi_translation.json
    │   │   ├── nwt_bible.json -> ../../../bible-text/data/tmp/nwt_bible.json
    │   │   ├── science
    │   │   │   └── facts.json
    │   │   └── travel
    │   │       └── journey_data.json
    │   ├── manual-report.csv
    │   ├── output
    │   │   ├── Enhanced_Biblical_Journeys_Map.html
    │   │   ├── asv_bible.csv
    │   │   ├── asv_bible.json
    │   │   ├── charts.md
    │   │   ├── kj21_bible.csv
    │   │   ├── kj21_bible.json
    │   │   ├── nwt_bible.csv
    │   │   ├── nwt_bible.json -> ../../../bible-text/data/tmp/nwt_bible.json
    │   │   ├── nwt_entities.csv
    │   │   ├── nwt_entities.json
    │   │   ├── ojb_bible.json
    │   │   ├── ojb_entities.csv
    │   │   ├── ojb_entities.json
    │   │   └── science
    │   │       └── charts.md
    │   ├── travel.dot
    │   └── travel.md
    ├── main.py
    ├── pyproject.toml
    ├── taskfile.yaml
    ├── test_main.py
    └── uv.lock

    21 directories, 52 files

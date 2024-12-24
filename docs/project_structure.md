# structure

.
├── README.md
├── analysis
│   ├── lifespans
│   │   ├── README.md
│   │   ├── lifespan.py
│   │   ├── main.py
│   │   ├── results
│   │   │   ├── chapter_entity_summary.csv
│   │   │   ├── entities.csv
│   │   │   ├── entities.json
│   │   │   ├── lifespans.json
│   │   │   ├── word_counts.list
│   │   │   └── words.list
│   │   ├── taskfile.yaml
│   │   └── test_main.py
│   ├── occupations
│   │   └── results
│   └── sentiments
│       └── results
├── config
│   └── book_order.py
├── core
│   ├── data_manager
│   │   └── __init__.py
│   ├── nlp_tagger
│   │   ├── __init__.py
│   │   ├── bible_search.py
│   │   └── tagger.py
│   ├── science
│   │   ├── __init__.py
│   │   ├── data_handler.py
│   │   └── facts.py
│   ├── translation_loader
│   │   ├── __init__.py
│   │   └── translation_manager.py
│   ├── travel
│   │   ├── __init__.py
│   │   ├── journey_data.py
│   │   └── mapper.py
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
│   │   └── nwt_bible.json -> ../../../bible-text/data/tmp/nwt_bible.json
│   ├── manual-report.csv
│   ├── output
│   │   ├── Enhanced_Biblical_Journeys_Map.html
│   │   └── charts.md
│   ├── travel.dot
│   └── travel.md
├── main.py
├── pyproject.toml
├── taskfile.yaml
├── test_main.py
└── uv.lock

19 directories, 43 files

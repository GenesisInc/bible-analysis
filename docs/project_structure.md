# project-structure

    .
    ├── analysis
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
    │   ├── book_order.py
    │   ├── reference_utils.py
    │   └── tagging_config.py
    ├── core
    │   ├── nlp_tagger
    │   │   ├── __init__.py
    │   │   ├── bible_search.py
    │   │   ├── entity_tagging.py
    │   │   ├── event_tagging.py
    │   │   ├── lifespan_tagging.py
    │   │   ├── occupation_tagging.py
    │   │   ├── reference_extrator.py
    │   │   └── relationship_tagging.py
    │   ├── translation_loader
    │   │   ├── __init__.py
    │   │   └── translation_manager.py
    │   ├── utils
    │   │   ├── __init__.py
    │   │   ├── file_utils.py
    │   │   ├── logger_utils.py
    │   │   ├── reference_utils.py
    │   │   ├── tagging_utils.py
    │   │   └── text_utils.py
    │   └── visualization
    │       └── visualization.py
    ├── data
    │   ├── Biblical_Travel_Details.csv
    │   ├── Enhanced_Biblical_Journeys_Map.html
    │   ├── asv_bible.csv
    │   ├── asv_bible.json
    │   ├── bible_entities.csv
    │   ├── bible_entities.json
    │   ├── charts.md
    │   ├── kj21_bible.csv
    │   ├── kj21_bible.json
    │   ├── manual-report.csv
    │   ├── multi_translation.json
    │   ├── nwt_bible.csv
    │   ├── nwt_bible.json
    │   ├── nwt_entities.csv
    │   ├── nwt_entities.json
    │   ├── ojb_bible.json
    │   ├── ojb_entities.csv
    │   ├── ojb_entities.json
    │   ├── science
    │   │   ├── charts.md
    │   │   └── facts.json
    │   ├── travel
    │   │   └── journey_data.json
    │   ├── travel.dot
    │   └── travel.md
    ├── data.old
    │   ├── Biblical_Travel_Details.csv
    │   ├── Enhanced_Biblical_Journeys_Map.html
    │   ├── asv_bible.csv
    │   ├── asv_bible.json
    │   ├── bible_entities.csv
    │   ├── bible_entities.json
    │   ├── charts.md
    │   ├── kj21_bible.csv
    │   ├── kj21_bible.json
    │   ├── manual-report.csv
    │   ├── multi_translation.json
    │   ├── nwt_bible.csv
    │   ├── nwt_bible.json
    │   ├── nwt_entities.csv
    │   ├── nwt_entities.json
    │   ├── ojb_bible.json
    │   ├── ojb_entities.csv
    │   ├── ojb_entities.json
    │   ├── science
    │   │   ├── charts.md
    │   │   └── facts.json
    │   ├── travel
    │   │   └── journey_data.json
    │   ├── travel.dot
    │   └── travel.md
    ├── logs
    │   └── bible_analysis.log
    ├── main.py
    ├── pyproject.toml
    ├── taskfile.yaml
    ├── test_main.py
    └── uv.lock
    
    20 directories, 76 files

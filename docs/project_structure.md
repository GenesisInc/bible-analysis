# project-structure

updated by user: 'rt' on: 2024-12-28 16:22

    .
    ├── analysis
    │   └── science_facts
    │       └── __init__.py
    ├── cli
    │   ├── __init__.py
    │   ├── parsers.py
    │   ├── parsers_extract.py
    │   ├── parsers_reference.py
    │   ├── parsers_science.py
    │   ├── parsers_search.py
    │   ├── parsers_tag_entities.py
    │   └── parsers_travel.py
    ├── commands
    │   ├── __init__.py
    │   ├── extract.py
    │   ├── handle_command.py
    │   ├── mapper.py
    │   ├── reference.py
    │   ├── search.py
    │   └── tag_entities.py
    ├── config
    │   ├── book_order.py
    │   ├── reference_utils.py
    │   └── tagging_config.py
    ├── core
    │   ├── tagger
    │   │   ├── __init__.py
    │   │   ├── entity_tagging.py
    │   │   ├── event_tagging.py
    │   │   ├── lifespan_tagging.py
    │   │   ├── occupation_tagging.py
    │   │   └── relationship_tagging.py
    │   ├── utils
    │   │   ├── __init__.py
    │   │   ├── file_utils.py
    │   │   ├── logger_utils.py
    │   │   ├── science_facts_utils.py
    │   │   ├── tagging_utils.py
    │   │   └── text_utils.py
    │   └── visuals
    │       └── visualizer.py
    ├── data
    │   ├── Enhanced_Biblical_Journeys_Map.html
    │   ├── charts.md
    │   ├── science
    │   │   └── charts.md
    │   ├── travel
    │   ├── travel.dot
    │   └── travel.md
    ├── logs
    │   └── bible_analysis.log
    ├── main.py
    ├── pyproject.toml
    ├── taskfile.yaml
    ├── test_main.py
    └── uv.lock
    
    13 directories, 43 files

# data structure

## input files

    1. ./data/input/multi_translation.json

    {
        "genesis": {
            "1": {
                "1": {
                    "asv": "In the beginning God created the heavens and the earth.",
                    "nog": "In the beginningElohimcreated heaven and earth.",
                    "rsvce": "In the beginning God createdthe heavens and the earth.",
                    "kj21": "In the beginning God created the heaven and the earth.",
                    "kjv": "In the beginning God created the heaven and the earth.",
                    "ojb": "In the beginning Elohim created hashomayim (the heavens, Himel) and haaretz (the earth).",
                    "nwt": "In the beginning God created the heavens and the earth."
                },
                "2": {
                    "asv": "And the earth was waste and void; and darkness was upon the face of the deep: and the Spirit of Godmoved upon the face of the waters.",
                    "nog": "The earth was formless and empty, and darkness covered the deep water. TheRuach Elohimwas hovering over the water.",
                    "rsvce": "The earth was without form and void, and darkness was upon the face of the deep; and the Spiritof God was moving over the face of the waters.",
                    "kj21": "And the earth was without form and void, and darkness was upon the face of the deep. And the Spirit of God moved upon the face of the waters.",
                    "kjv": "And the earth was without form, and void; and darkness was upon the face of the deep. And the Spirit of God moved upon the face of the waters.",
                    "ojb": "And the earth was tohu vavohu (without form, and void); and darkness was upon the face of the deep. And the Ruach Elohim was hovering upon the face of the waters.",
                    "nwt": "Now the earth was formless and desolate, and there was darkness upon the surface of the watery deep, and Gods active force was moving about over the surface of the waters."
                },
                ...
            },
        },
        "exodus": {
            "1": {
                "1": {
                },
            }
        }
    }

    2. ./data/input/nwt_bible.json

    {
        "nwt": {
            "genesis": {
                "1": {
                    "1": "In the beginning God created the heavens and the earth.",
                },
                "2": {}
            },
            "exodus": {

            }
        }
    }

## output files

    1. data/output/tmp/nwt_entities.csv

        Book,Chapter,Verse,Type,Text
        genesis,1,3,PERSON,God
        genesis,1,5,DATE,the light Day
        genesis,1,5,DATE,a first day
        genesis,1,13,DATE,a third day

    2. data/output/tmp/nwt_entities.json

    {
        "genesis": {
            "1": {
                "1": {
                    "entities": {
                        "PERSON": [ "God", "Adam" ],
                        "DATE": [],
                        "GPE": [],
                        "ORG": [],
                        "NORP": []
                    },
                    "occupations": []
                },
                "2": {
                    "entities": {
                        "PERSON": ["adam", "eve", "..." ],
                        "DATE": [4096,],
                        "GPE": ["human", ],
                        "ORG": ["man", "woman", ],
                        "NORP": []
                    },
                    "occupations": []
                },
            }
        },
        ...
    }
    
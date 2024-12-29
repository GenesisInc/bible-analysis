# data structure

updated by user: 'rt' on: 2024-12-28 16:22

## input file: data/multi_translation.json

    {
        "genesis": {
            "1": {
                "1": {
                    "asv": "In the beginning God created the heavens and the earth.",
                    "nog": "In the beginningElohimcreated heaven and earth.",
                    "rsvce": "In the beginning God createdthe heavens and the earth.",
                    "kj21": "In the beginning God created the heaven and the earth.",
                    "kjv": "In the beginning God created the heaven and the earth.",
    ...
    ...
                    "kjv": "He which testifieth these things saith, Surely I come quickly. Amen. Even so, come, Lord Jesus.",
                    "ojb": "\u201cHe who gives solemn edut to these things says, \u2018Ken! I am coming bahlt (soon)!\u2019 \u201d Omein. Come Adoneinu Yehoshua!",
                    "nwt": "The one who bears witness of these things says, Yes, I am coming quickly. Amen! Come, Lord Jesus."
                },
                "21": {
                    "asv": "The grace of the Lord Jesusbewith the saints. Amen.",
                    "nog": "The good willof the LordYeshuabe with all of you. Amen!",
                    "rsvce": "The grace of the Lord Jesus be with all the saints.Amen.",
                    "kj21": "The grace of our Lord Jesus Christ be with you all. Amen.",
                    "kjv": "The grace of our Lord Jesus Christ be with you all. Amen.",
                    "ojb": "The Chen v\u2019Chesed Hashem of Adoneinu Yehoshua be with all. Omein.",
                    "nwt": "May the undeserved kindness of the Lord Jesus be with the holy ones."
                }
            }
        }
    }

## input file: data/nwt_bible.json

    + head -n9 data/nwt_bible.json
    {
        "nwt": {
            "genesis": {
                "1": {
                    "1": "In the beginning God created the heavens and the earth.",
                    "2": "Now the earth was formless and desolate, and there was darkness upon the surface of the watery deep, and Gods active force was moving about over the surface of the waters.",
                    "3": "And God said: Let there be light. Then there was light.",
                    "4": "After that God saw that the light was good, and God began to divide the light from the darkness.",
                    "5": "God called the light Day, but the darkness he called Night. And there was evening and there was morning, a first day.",
    
    ...
    ...
    + tail -n16 data/nwt_bible.json
                    "10": "He also tells me: Do not seal up the words of the prophecy of this scroll, for the appointed time is near.",
                    "11": "Let the one who is unrighteous continue in unrighteousness, and let the filthy one continue in his filth; but let the righteous one continue in righteousness, and let the holy one continue in holiness.",
                    "12": "Look! I am coming quickly, and the reward I give is with me, to repay each one according to his work.",
                    "13": "I am the Alpha and the Omega, the first and the last, the beginning and the end.",
                    "14": "Happy are those who wash their robes, so that they may have authority to go to the trees of life and that they may gain entrance into the city through its gates.",
                    "15": "Outside are the dogs and those who practice spiritism and those who are sexually immoral and the murderers and the idolaters and everyone who loves and practices lying.",
                    "16": "I, Jesus, sent my angel to bear witness to you about these things for the congregations. I am the root and the offspring of David and the bright morning star.",
                    "17": "And the spirit and the bride keep on saying, Come! and let anyone hearing say, Come! and let anyone thirsting come; let anyone who wishes take lifes water free.",
                    "18": "I am bearing witness to everyone who hears the words of the prophecy of this scroll: If anyone makes an addition to these things, God will add to him the plagues that are written in this scroll;",
                    "19": "and if anyone takes anything away from the words of the scroll of this prophecy, God will take his portion away from the trees of life and out of the holy city, things that are written about in this scroll.",
                    "20": "The one who bears witness of these things says, Yes, I am coming quickly. Amen! Come, Lord Jesus.",
                    "21": "May the undeserved kindness of the Lord Jesus be with the holy ones."
                }
            }
        }
    }

## output data

    + mlr --json sample -k 3 data/nwt_entities.json
    [
    {
      "book": "genesis",
      "chapter": "11",
      "verse": "18",
      "type": "DATE",
      "trigger": "30 years",
      "context": "Peleg lived for 30 years and then became",
      "extras": {}
    },
    {
      "book": "job",
      "chapter": "26",
      "verse": "1",
      "type": "ORG",
      "trigger": "Job",
      "context": "Job said in reply",
      "extras": {}
    },
    {
      "book": "1 kings",
      "chapter": "22",
      "verse": "49",
      "type": "OCCUPATION",
      "trigger": "servant",
      "context": ": Let my servants go with your",
      "extras": {}
    }
    ]
    
    
    + mlr --j2c sample -k 3 data/nwt_entities.json
    book,chapter,verse,type,trigger,context,extras
    genesis,10,22,ORG,Elam,"of Shem were Elam , Asshur ,",{}
    ezra,10,36,PERSON,Eliashib,", Meremoth , Eliashib ,",{}
    numbers,35,32,OCCUPATION,priest,of the high priest .,{}
    

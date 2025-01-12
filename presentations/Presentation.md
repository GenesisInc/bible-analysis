---
author: Robert Thanulingam
date: MMMM dd, YYYY
paging: Slide %d / %d
---
<!-- markdownlint-disable MD001 MD041 -->

## testing

```bash
figlet bible   analysis
```

---

# Overview
<!-- markdownlint-disable MD001 MD005 single-h1 no-duplicate-heading no-inline-html-->

- Analyze Bible text across multiple translations.
- Explore how relevant it is to the interests of the 21st century.

For more details, see TODO.md for a curated list of topics of interest.

---

# Main Components

1. Download: Acquire and organize Bible texts.
2. Analyze: Use advanced NLP techniques for insights.
3. Serve: Share insights via a robust API server.

---

# 1. Download bible text

- Goal: Gather Bible text in structured formats (JSON/CSV).
- How?
  - Scrape or crawl websites to download various translations.
  - Repository: genesisInc/bible-text
- Tools Used: Python & Bash.

---

# 2. Analyze text

- Objective: Extract meaningful insights using Natural Language Processing (NLP).
  - Leverage spaCy for entity recognition and tagging.
- Current Capabilities:
  - Identify persons, dates, occupations, organizations, locations, and more.

## 2.1 how it works

```python
import spacy

# Load the spaCy model
nlp = spacy.load("en_core_web_sm", disable=["parser"])

# Input text for demonstration
text = "In the beginning God created the heavens and the earth."

# Process the text
doc = nlp(text)

# Print tokens with their details
print("Tokens and their details:")
for token in doc:
    print(f"{token.text} -> POS: {token.pos_}, Tag: {token.tag_}, Lemma: {token.lemma_}")

# Print named entities
print("\nNamed Entities:")
for ent in doc.ents:
    print(f"Text: {ent.text}, Label: {ent.label_}")
```

Note

1. Unless you run `uv run slides presentations/Presentation.md`, can't exec py pgm.
   1. In other words, please run the 'slides ...' from python shell.
2. '<ctrl+e>' to run above block

---

# Quick Demo

## summary

- Generate a concise summary of identified entities.
- Checkout TODO.md for the other items we need to track in the future
- Press `ctrl-e` to run

```bash
task legends
```

---

# Quick Demo

## dates

- Detect explicit and implicit date expressions (e.g., “40 years in the wilderness”).
- '<ctrl-e>' to run

```bash
task date
```

---

# Quick Demo

## persons

- Extract individual names and mentions.
- '<ctrl-e>' to run

```bash
task names
```

---

# Quick Demo

## lifespans

- Analyze individual lifespans.
- '<ctrl-e>' to run

```bash
task lifespan
```

---

# Quick Demo

## occupations

- Tag roles and jobs (e.g., shepherds, priests).
- '<ctrl-e>' to run

```bash
task occupation
```

---

# Quick Demo

## orgs

- Identify groups and organizations.
- '<ctrl-e>' to run

```bash
task org
```

---

# Quick Demo

## gpe [Geopolitical entities (places)]

- Extract references to places.
- '<ctrl-e>' to run

```bash
task gpe
```

---

# Quick Demo

## norp (Nationalities religious or political groups)

- Identify cultural or group identities.

```bash
task norp
```

## Summary

- Current progress includes identifying a subset of entities.
- Future focus areas listed in TODO.md.
  
---

# 3. Serve

- Objective: Make insights available via a fast, scalable API.
- Technology: Built with Go for efficiency and robustness.

---

## Final Slide

Thank you! Questions?

- Presentations:
  - 1. December 30th 2024 at 5:545pm (4 persons)

# Entity Model

The openTECR DB represents a re-curation of the data originally published by Goldberg
_et al._ (2016).

At the core of the openTECR data lies the curated `Measurement` entity. Each measurement
represents an attempt to quantify the apparent equilibrium constant [K'] of a
biochemical `Reaction` in a certain experimental `Condition` of the aqueous solution.
Each measurement was
curated from a `Table`, where each table
contains one or more measurements on one reaction. Each table was published as part
of the `Primary Curation` of information by Goldberg _et al._ (2016).

```mermaid
erDiagram
    Measurement {
    }
    Reaction {
    }
    Table {
    }
    primary["Primary Curation"] {
    }
    Reference {
    }

    Measurement }|--|| Reaction: "quantifies"
    Measurement }|--|| Table: "curated from"
    Table }|--|| primary: "published in"
    Reaction ||--|{ Table: "subject of"
    primary ||--|{ Reference: "curated from"
```

The above diagram shows the most important entities in the model and their
relationships. Below, we describe all entities and their attributes.

```mermaid
erDiagram
    Measurement {
        int entry_index
        float k_prime
        float temperature
        Optional[float] ionic_strength
        Optional[float] hydrogen_potential
        Optional[float] magnesium_potential
        Optional[str] method
        Optional[str] buffer
    }
    W3ID {
        str accession
    }
    id["MIRIAM Identifier"] {
        str source
        str accession
    }
    Metabolite {
        Optional[str] chemical_formula
        list[str] synonyms
    }
    Reaction {
        list[str] synonyms
    }
    Table {
        int part
        int page
        enum column
        int table_index
        Optional[bool] was_spellchecked
        Optional[str] primary_comment
        Optional[str] secondary_comment
    }
    primary["Primary Curation"] {
    }
    Reference {
        str reference_code
        Optional[int] pmid
        Optional[str] doi
    }

    Measurement ||--o| W3ID: "identified by"
    Measurement }|--|| Reaction: "quantifies"
    Measurement }|--|| Table: "curated from"
    Table }|--|| primary: "published in"
    Reaction ||--|{ Table: "subject of"
    Reaction }|--|{ Metabolite: "contains"
    Reaction ||--|{ id: "has"
    Metabolite ||--|{ id: "has"
    primary ||--|{ Reference: "curated from"
```

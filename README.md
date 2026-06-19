# Cruise Rider Safety Dashboard

Companion Streamlit dashboard for the paper:

**Advances in Automated Driving: Perceptions of Safety, Operations, and Comfort From Riders**

This repository contains a Cruise-only public-safe dashboard derived from an anonymized research rider / non-rider survey dataset. It is intentionally separate from the broader multi-dataset `rideshare-safety-rider-analysis` project so the first paper has a stable companion artifact and Streamlit deployment.

## Live App

Streamlit URL:

https://cruise-rider-safety.streamlit.app/

## Purpose

The dashboard supports exploration of rider and non-rider responses related to:

- perceived safety and trust;
- comfort and rider experience;
- vehicle behavior and operational reliability;
- late-night mobility;
- alternative modes;
- willingness to pay;
- value priorities including accessibility, service distribution, zero-emission vehicles, and transit connectivity.

## Data

The dashboard uses a public-safe derived dataset. Raw survey data and raw open-ended comments are not included.

Public-safe processing rules:

- Riders are mapped using final dropoff coordinates from the anonymized survey export.
- Non-riders are mapped using generalized survey-location coordinates.
- Raw open-ended responses are excluded from the public dashboard dataset.
- No names, emails, usernames, or direct identifiers are stored.

The current app reads the public-safe dataset from the companion research repository while this Cruise-only repository is being finalized. A static copy can also be placed at:

`data/cruise_research_rider_public_safe.csv`

## Repository Structure

```text
.
├── data/
│   └── README.md
├── docs/
│   ├── data_dictionary.md
│   ├── deployment.md
│   └── paper_context.md
├── src/
│   └── cruise_rider_dashboard.py
├── README.md
└── requirements.txt
```

## Deployment

On Streamlit Community Cloud, deploy with:

```text
Repository: williamwriggs/cruise-rider-safety-dashboard
Branch: main
Main file path: src/cruise_rider_dashboard.py
```

## Research Ethics

This repository is designed as a public-safe research companion. The underlying raw survey data should remain private unless separately reviewed and approved for release. The dashboard is intended for aggregate exploration and paper transparency, not participant identification.

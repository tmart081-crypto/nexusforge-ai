# NexusForge AI Platform (v1.0)

Enterprise multi-modal AI platform built for client **Aether Dynamics Global** as the final capstone project of the AI & Python Certification (engagement code `NF-CAP-01`).

One application, one navigation shell — text intelligence, image intelligence (BLIP), document analysis, prompt optimization, token/embedding explorers, model/pipeline explorers, a visualization dashboard, Responsible AI, and AI infrastructure.

Full spec: [docs/spec.md](docs/spec.md) (condensed from the official Capstone Project Portal — Executive Summary, Client Brief, functional/non-functional requirements, architecture, all 14 milestones, rubric).

## Status

Milestone 4 done (Text Intelligence) — see [docs/milestones.md](docs/milestones.md) for progress against the 14-milestone plan.

## Modules

| # | Area | Module |
|---|---|---|
| 01 | Home | Dashboard |
| 02 | Intelligence | Text Intelligence |
| 03 | Intelligence | Image Intelligence (BLIP) |
| 04 | Intelligence | Document Analyzer |
| 05 | Optimization | Prompt Optimizer |
| 06 | Optimization | Token Explorer |
| 07 | Optimization | Embedding Explorer |
| 08 | Explorers | Model Explorer |
| 09 | Explorers | Pipeline Explorer |
| 10 | Explorers | Visualization Dashboard |
| 11 | Governance | Responsible AI Dashboard |
| 12 | Governance | AI Infrastructure Explorer |
| 13 | Ops | Settings |
| 14 | Ops | Export Reports |
| 15 | Ops | History |

## Tech stack

- Python 3.10+
- Streamlit (UI shell)
- Hugging Face: Transformers, Tokenizers, Pipelines, Datasets, Sentence Transformers, BLIP
- NumPy, Matplotlib, TensorFlow, NLTK

## Getting started

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run main.py
```

Runs entirely on CPU; GPU is used automatically if available (see `config/device.py`).

## Project structure

```
nexusforge-ai/
├── app/                 # Streamlit UI pages (one per module)
├── services/            # Business logic, orchestrates models per module
├── models/              # Model loaders / registry wrappers
├── utils/               # Shared helpers (NumPy, viz, logging)
├── config/              # Model registry (YAML), device manager, settings
├── data/                # Sample text/images for demos (gitignored uploads)
├── tests/                # Unit tests
├── docs/                # Spec summary, architecture diagram, tech docs, user manual
├── assets/              # Diagrams, presentation slides
├── requirements.txt
├── README.md
├── .gitignore
└── main.py              # Entrypoint
```

## Architecture

Each module follows: `app/<module>.py` (UI) → `services/<module>_service.py` (logic) → `models/registry.py` (lazy-loaded HF pipeline). No AI calls are made directly from UI code.

## Responsible AI

See the in-app Responsible AI dashboard for model limitations, bias considerations, and confidence reporting per module.

## Reflection / AI assistance disclosure

This project was built with Claude Code as a coding assistant. See `docs/reflection.md` for details on where AI assistance was used and how the code was reviewed and understood.

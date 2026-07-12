# NexusForge AI Platform (v1.0)

Enterprise multi-modal AI platform built for client **Aether Dynamics Global** as the final capstone project of the AI & Python Certification (engagement code `NF-CAP-01`).

One application, one navigation shell — text intelligence, image understanding (BLIP), document analysis, prompt optimization, tokenization, embeddings, model/pipeline explorers, visualizations, Responsible AI, and AI infrastructure.

## Status

Milestone 1 in progress — project scaffold, virtual environment, and app shell. See [docs/milestones.md](docs/milestones.md) for progress against the 14-milestone plan.

## Modules

| Area | Module |
|---|---|
| Home | Dashboard |
| Text | Text Intelligence |
| Vision | Image Understanding (BLIP) |
| Documents | Document Analyzer |
| Prompts | Prompt Optimizer |
| Tokens | Tokenization Explorer |
| Embeddings | Embeddings & Similarity |
| Explorers | Model Explorer |
| Explorers | Pipeline Explorer |
| Explorers | Visualizations |
| Governance | Responsible AI |
| Infra | AI Infrastructure |
| Ops | Settings |
| Ops | History |
| Ops | Export / Reports |

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
├── config/              # Model registry, device manager, settings
├── data/                # Sample text/images for demos (gitignored uploads)
├── tests/                # Unit tests
├── docs/                # Architecture diagram, tech docs, user manual
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

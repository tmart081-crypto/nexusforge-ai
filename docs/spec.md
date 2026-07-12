# NexusForge AI Platform — Capstone Spec Summary

Condensed from the official Capstone Project Portal
(`NexusForge_Student_Kickoff_Handout(1).html`, titled "NexusForge AI ·
Capstone Project Portal"). That file is the source of truth; this doc exists
so future work doesn't require re-reading a 3800-line HTML file. If the two
ever disagree, the portal HTML wins — re-extract and update this file.

## Engagement snapshot

- Client: Aether Dynamics Global (fictional), engagement `NF-CAP-01`
- Role: Junior AI Engineer, sole contributor for v1.0
- Duration: 6 weeks full-time, ~120–160h, 14 sequential milestones
- Pass 70/100 · Merit 80 · Distinction 85+
- Automatic caps: non-runnable app ≤40, missing GitHub/README ≤55,
  notebook-dump instead of one app ≤45, undisclosed plagiarism → possible 0

## Business problem (why this exists)

ADG's teams use fragmented SaaS tools for text/image/embeddings work: no
shared model catalog, no tokenization visibility, no responsible-AI
guardrails, no audit trail, poor infra literacy for budget approvers. v1.0
consolidates all of this into one modular application that is both an
operational tool and a portfolio/demo artifact.

## Client's Definition of Done

ADG can: clone repo → venv → install → launch; run every core text/image
workflow without crashes; review RAI + infra explainer pages; export a
report and inspect history; receive architecture docs, user manual, test
report, presentation materials.

## Functional requirements — 15 modules

| # | Module | Notes |
|---|---|---|
| 01 | Dashboard | module shortcuts, recent history, system status, quick-run actions |
| 02 | Text Intelligence | summarize, translate, QA, sentiment, NER, keywords, fill-mask, generation, zero-shot, feature extraction |
| 03 | Image Intelligence | BLIP captioning, visual QA, description, confidence |
| 04 | Document Analyzer | ingest txt/md/pdf, structure/section extraction, summarize, Q&A |
| 05 | Prompt Optimizer | A/B comparison, scoring rubric, improvement suggestions |
| 06 | Token Explorer | char/word/subword/WordPiece, token IDs, vocab peek, visualization |
| 07 | Embedding Explorer | sentence embeddings, cosine similarity (NumPy), vector ops, Matplotlib viz |
| 08 | Model Explorer | catalog of HF models used, metadata, task type, load status |
| 09 | Pipeline Explorer | HF pipelines wired in, usage counts, sample runs |
| 10 | Visualization Dashboard | confidence, word frequency, embedding plots, prediction distributions, pipeline usage |
| 11 | Responsible AI Dashboard | confidence, bias warnings, ethics notes, hallucination flags, limitations |
| 12 | AI Infrastructure Explorer | GPU/CPU/Tensor Cores, inference vs training, NVIDIA, cloud, datacenters |
| 13 | Settings | model defaults, device (CPU/GPU), theme, cache paths, logging level |
| 14 | Export Reports | JSON/Markdown/PDF or HTML export |
| 15 | History | persistent local history, replay + delete |

Note: module numbering here is the portal's own order (Export=14, History=15) —
our earlier scaffold had them swapped and has since been corrected.

## Non-functional requirements (highlights, full list has 15 — NFR-01..15)

- **NFR-01** Modular structure: UI / services / models / utils / config / tests
- **NFR-02** Config via files (YAML/JSON/TOML/.env) — no hardcoded secrets/paths
- **NFR-03** Graceful error handling, user-visible messages + logs
- **NFR-05** Lazy model loading, no load-everything-at-startup, progress indicators
- **NFR-06** Runs on CPU, auto-detects GPU
- **NFR-07** Pinned requirements.txt, clean-machine install works
- **NFR-08** Automated unit tests + smoke tests for pipelines/services
- **NFR-10** No credential leakage, safe file upload handling, no arbitrary code exec from user text
- **NFR-12** Meaningful git history, .gitignore for venv/caches/weights
- **NFR-13** README, architecture diagram, tech docs, user manual, test report, slides

## Tech stack (required — must be used meaningfully, no dead imports)

Python 3.10+, venv, VS Code, Git, GitHub, pip · NumPy, Matplotlib, TensorFlow ·
transformers, tokenizers, pipelines, models, datasets, sentence-transformers,
BLIP · NLTK · Streamlit or Gradio (one primary UI).

## Architecture (reference shape)

Presentation (pages) → Application Services → AI/ML Layer (HF pipelines,
tokenizers, sentence-transformers, BLIP, TF ops, NLTK) → Computation/Viz
(NumPy, cosine similarity, stats, Matplotlib) → Cross-cutting (config,
logging, exceptions, file I/O, device manager, tests).

Suggested layout adds `assets/` (diagrams, slides) and `logs/` (gitignored)
to what we'd already built:

```
nexusforge-ai/
├── app/ services/ models/ utils/ config/ data/ tests/ docs/ assets/ logs/
├── requirements.txt  README.md  .gitignore  main.py
```

Design principles: one entrypoint/one nav shell, lazy loading, service
isolation (UI never calls pipelines directly), config-driven model IDs,
fail-soft (one bad pipeline can't crash the app), observable (logs+history+export).

## Milestones (14, sequential, no solution code given)

| # | Milestone | Est. | Key acceptance criteria |
|---|---|---|---|
| 01 | Kickoff & repo scaffold | 8–10h | cloneable repo, venv+requirements installs, entrypoint runs, ≥3 meaningful commits |
| 02 | App shell & navigation | 8–12h | all 15 modules reachable, no dead links, dashboard shows history+system-status placeholders |
| 03 | Core services & model registry | 10–14h | models load on demand only, clean error messages, load events logged, registry lists task→model mappings |
| 04 | Text Intelligence | 14–18h | every text feature produces valid output on sample input, invalid input handled gracefully, loading states shown |
| 05 | Image Intelligence (BLIP) | 10–14h | supported formats load, caption+VQA coherent on sample images, corrupt/unsupported files handled |
| 06 | Document Analyzer | 8–12h | at least TXT/MD supported (PDF preferred), Q&A references doc content, large files get clear limits |
| 07 | Token Explorer | 8–10h | same input shows multiple tokenization strategies side by side, IDs align with tokenizer, readable viz |
| 08 | Embedding Explorer & NumPy layer | 10–14h | compare ≥2 sentences w/ similarity scores, NumPy used in real calc paths (not decorative), chart renders |
| 09 | Prompt Optimizer | 8–12h | two prompts scored/compared, suggestions generated for weak prompts, results saveable to history |
| 10 | Model/Pipeline Explorer + Viz Dashboard | 10–12h | all used models appear in catalog, ≥4 distinct chart types w/ real data, pipeline usage counters update |
| 11 | Responsible AI Dashboard | 8–10h | RAI warnings appear in workflows + dashboard, limitations are task-specific not generic, export can include RAI notes |
| 12 | Infra Explorer, History, Export, Settings | 8–12h | infra module content-complete, history stores/reloads runs, export produces downloadable artifact, settings affect subsequent runs |
| 13 | Testing, hardening, TensorFlow pass | 10–14h | tests run via documented command, happy paths pass on CPU, TF used intentionally somewhere, no uncaught exceptions on demo script |
| 14 | Docs, presentation, packaging | 12–16h | all 12 deliverables present, clean install verified fresh, demo video covers end-to-end path, repo submission-ready |

Midpoint review: end of Week 3, Text + Image demo required. Final defense:
Week 6, live demo + Q&A.

## 12 final deliverables (all mandatory)

1. Working AI application  2. Complete source code  3. GitHub repository
4. Professional README  5. requirements.txt  6. Architecture diagram
7. Technical documentation  8. User manual  9. Testing report
10. Presentation slides  11. Demo video (5–12 min)  12. Reflection report

## Rubric (100 marks, pass 70)

Functionality 18 · HF/AI implementation 16 · Code quality 12 · Architecture 10
· NumPy/Matplotlib/TensorFlow 8 · Prompt engineering 6 · Responsible AI 6 ·
UI/UX 6 · Documentation 8 · Presentation/demo 5 · Git process 3 · Innovation 2.
Bonus items (RAG, vector DB, Docker, auth, cloud deploy, etc.) can add up to
+10, capped at 100 — attempt only after core scope is stable.

## What NOT to build (out of scope for v1.0)

Multi-tenant SaaS billing, fine-tuning foundation models from scratch, native
mobile apps, real-time multi-user collab, guaranteed SLA ops, paid commercial
model APIs as a hard dependency, tutorials/theory submissions.

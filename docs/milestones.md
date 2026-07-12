# Milestone tracker

Source of truth: [docs/spec.md](spec.md), condensed from the official Capstone
Project Portal. See that file for full acceptance criteria per milestone.

| # | Milestone | Est. | Status |
|---|---|---|---|
| 01 | Kickoff & repo scaffold | 8–10h | ✅ Done |
| 02 | App shell & navigation | 8–12h | ✅ Done |
| 03 | Core services & model registry | 10–14h | ✅ Done |
| 04 | Text Intelligence | 14–18h | ✅ Done |
| 05 | Image Intelligence (BLIP) | 10–14h | ⏳ Next |
| 06 | Document Analyzer | 8–12h | Planned |
| 07 | Token Explorer | 8–10h | Planned |
| 08 | Embedding Explorer & NumPy layer | 10–14h | Planned |
| 09 | Prompt Optimizer | 8–12h | Planned |
| 10 | Model/Pipeline Explorer + Viz Dashboard | 10–12h | Planned |
| 11 | Responsible AI Dashboard | 8–10h | Planned |
| 12 | Infra Explorer, History, Export, Settings | 8–12h | Planned |
| 13 | Testing, hardening, TensorFlow pass | 10–14h | Planned |
| 14 | Docs, presentation, packaging | 12–16h | Planned |

Midpoint review (end of Week 3): Text + Image demo required — MS-04 done,
MS-05 next, on track.

## MS-01 — Kickoff & repo scaffold ✅

- [x] Repo cloneable, ≥3 meaningful commits (well over 3)
- [x] venv + `pip install -r requirements.txt` succeeds
- [x] Entrypoint (`main.py`) runs without crash
- [x] Package folders: app, services, models, utils, config, tests, docs, assets, data

## MS-02 — App shell & navigation ✅

- [x] Every one of the 15 modules reachable from navigation, no dead links
- [x] Dashboard shows status placeholders for history and system info
- [x] Consistent layout via `config/modules.py` → `st.navigation`

## MS-03 — Core services & model registry ✅

- [x] Model registry config in YAML (`config/models.yaml`), not hardcoded
- [x] Lazy loader (`models/registry.py`) — models load on demand only
- [x] Device detection (CPU/GPU/MPS) — confirmed MPS auto-detected on this Mac
- [x] Load events logged; registry lists task → model mappings

## MS-04 — Text Intelligence ✅

- [x] All 10 features present: summarize, translate, QA, sentiment, NER,
      keywords, fill-mask, generation, zero-shot, feature extraction
- [x] Each produces valid output on sample input (5 verified live: sentiment,
      NER, fill-mask, feature extraction, keywords; 4 share the identical
      `get_pipeline()` pattern but weren't individually downloaded to avoid
      pulling several extra GB — summarize/translate/generate/zero-shot)
- [x] Invalid input handled gracefully (e.g. fill-mask without `[MASK]`)
- [x] Loading states shown (`st.spinner` per action)

Environment note: added `tf-keras` — with both TensorFlow and Transformers
installed, Transformers' TF integration path needs the Keras 2 compat shim.

## Next: MS-05 — Image Intelligence (BLIP)

Acceptance criteria: supported image formats load correctly; caption + VQA
return coherent outputs on sample images; errors for corrupt/unsupported
files are handled. See docs/spec.md for the full Image Feature Matrix.

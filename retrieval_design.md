# Retrieval Layer for “How do I…?” Assistant

Design the **retrieval layer** for an assistant that answers product “How do I…?” questions using:
- **Zendesk tickets** (resolved & open),
- **Customer forum posts/threads,**
- **Product training webinars** (video transcripts + slides),
- **Official product documentation.**

**Scale (12 months):** ~50M chunks across ~200 tenants.  
**Latency SLO:** P95 end-to-end ≤ **1.5 s**; **retrieval budget ≤ 250 ms**.  
**Quality:** High faithfulness with **inline citations**. Prefer recent, officially approved guidance over stale forum content.  
**Compliance:** Per-tenant isolation, ACLs, PII redaction, audit logs.  
**No coding required. You may answer verbally and/or with brief notes.**

---

## What to cover (aim for concise bullets; ~10 minutes talking)

1. **Retrieval architecture (hybrid):**  
   How you combine **BM25 (lexical)** + **vector search** and whether you add a **cross-encoder reranker**.

2. **Ingestion & chunking (structure-aware):**  
   How you parse PDFs/HTML, **video transcripts**, threads; chunk sizes/overlap; handling of **tables/code/snippets**; metadata you store (tenant, doc_id, section_path, source_type, version, updated_at, ACL).

3. **Ranking & freshness policy:**  
   How you weight **official docs vs. Zendesk vs. forums**, and how you bias **recency** without losing authoritative content.

4. **Context packing & citations:**  
   How many tokens you budget for context; per-document caps; diversity (e.g., **MMR**); citation format; “answer only from sources / abstain if insufficient”.

5. **Observability & evaluation:**  
   What you log per request; offline metrics (**Recall@k, nDCG@k**) and online signals (citation coverage, user edit rate); drift detection.

---

## Write down these concrete defaults (2–3 minutes)

| Topic | Default |
|---|---|
| Chunk size / overlap | ____ tokens / ____% |
| Embedding model / dim | __________________ |
| Vector dtype | FP32 / FP16 / int8 (pick one) |
| ANN type & key params | HNSW (`M=?`, `ef_search=?`) *or* IVF (`nlist=?`, `nprobe=?`) |
| k values | vec = ___, bm25 = ___, rerank = ___, final = ___ |
| Reranker | None / small cross-encoder / escalate on borderline |
| Context token cap | ______ tokens (reserve ___% for model output) |
| Freshness & authority weights | Docs: __, Zendesk: __, Forums: __ (+ recency decay τ=___) |

> **Memory sanity check:** Show the quick math for 50M chunks at your chosen dimension & dtype.

---

## Risks / first fixes (optional, 1 minute)

List 2–3 biggest risks and your first tuning steps when quality is poor.


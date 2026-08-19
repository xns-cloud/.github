# XNS Cloud

S3-compatible distributed storage. It speaks the S3 API, so existing S3 tooling works against it
unchanged — more at [xns.tech](https://xns.tech).

<!-- REPO-TABLE -->

## Cookbook recipes

Each is a runnable script plus the architecture behind it, in
[xns-ai-cookbooks](https://github.com/xns-cloud/xns-ai-cookbooks).

| Recipe | What it does |
|--------|--------------|
| [Multimodal RAG](https://github.com/xns-cloud/xns-ai-cookbooks/tree/main/multimodal-rag) | Video speech and frames into transcripts and vision captions, cached in a bucket, then queried. |
| [Agentic Document Parsing](https://github.com/xns-cloud/xns-ai-cookbooks/tree/main/agentic-doc-parsing) | PDFs and spreadsheets parsed locally with Docling, extracted to structured JSON, cached per document. |
| [Fine-Tune Checkpointing](https://github.com/xns-cloud/xns-ai-cookbooks/tree/main/finetune-checkpointing) | Training checkpoints pushed to a bucket and recovered on a replacement GPU worker after preemption. |
| [Agent Workspace](https://github.com/xns-cloud/xns-ai-cookbooks/tree/main/agent-workspace) | CrewAI agents exchanging artifacts through a shared bucket instead of through the prompt. |

## Where to open issues

It depends on the row above.

- **Source of truth "GitLab"** — the GitHub copy is a read-only mirror, kept in sync
  automatically. Issues, merge requests and CI live on the GitLab source; open them there.
<!-- GH-ISSUES-EXCEPTION -->
- **Source of truth "here"** — the repository is developed on GitHub. Issues and pull requests
  on the GitHub repo are the right place.

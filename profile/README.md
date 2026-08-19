# XNS Cloud

S3-compatible distributed storage. It speaks the S3 API, so existing S3 tooling works against it
unchanged — more at [xns.tech](https://xns.tech).

| Repository | What it is | Install / use | Source of truth |
|------------|------------|---------------|-----------------|
| [relayer-mcp](https://github.com/xns-cloud/relayer-mcp) | MCP server — lets an AI agent drive XNS storage directly | `npx @xns-cloud/relayer-mcp` | [GitLab](https://gitlab.com/scpcorp/relayer-mcp) |
| [langchain-xns](https://github.com/xns-cloud/langchain-xns) | LangChain integration — document loaders and a `ByteStore` over XNS | `pip install langchain-xns` | here |
| [xns-ai-cookbooks](https://github.com/xns-cloud/xns-ai-cookbooks) | Working recipes for AI pipelines on XNS | clone and run | here |
| [relayer-quickstart](https://github.com/xns-cloud/relayer-quickstart) | Docker Compose quick-start — run a Relayer on your own host | `docker compose up` | [GitLab](https://gitlab.com/scpcorp/relayer-quickstart) |
| [xns-s5cmd](https://github.com/xns-cloud/xns-s5cmd) | Parallel S3 command-line client with XNS auth | see the repo README | [GitLab](https://gitlab.com/scpcorp/xns-s5cmd) |

## Where to open issues

It depends on the row above.

- **Source of truth "GitLab"** — the GitHub copy is a read-only mirror, kept in sync
  automatically. Issues, merge requests and CI live on the GitLab source; open them there.
  `relayer-mcp` is the exception: its
  [GitHub Issues](https://github.com/xns-cloud/relayer-mcp/issues) are monitored too.
- **Source of truth "here"** — the repository is developed on GitHub. Issues and pull requests
  on the GitHub repo are the right place.

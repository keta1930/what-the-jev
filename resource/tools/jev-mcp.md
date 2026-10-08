---
title: "jev-mcp (jkudish)"
updated: 2026-10-09
---

# jev-mcp (jkudish)

**Positioning** jev-mcp is a Model Context Protocol (MCP) server by GitHub user jkudish that exposes Jev's typed judgments to coding agents and other clients that speak the protocol. It held roughly 320 stars at the time of writing and is a third-party project maintained by one developer.

**What it does** The server provides 12 Jev judgment tools — verify, screen, rerank, classify, extract, audit, review, gate, and more — mapping onto the decision points an agent meets again and again over the course of a task, from verification to gating. Requests can be routed through four carriers, TypeSafe, OpenRouter, Cloudflare, or Vercel, or pointed at any System One-compatible endpoint. A bundled agent skill teaches clients when to reach for each of the tools, so the breadth of the toolset never has to be memorized.

**Characteristics** It is distributed on npm as `@jkudish/jev-mcp`, so installing it is a standard npm install, and it runs in both stdio and HTTP modes. The 320-star figure is a snapshot from the time of writing. The tool and carrier lists likewise reflect the repository's state at that moment and may change as it evolves.

**When to use** It suits setups where a coding agent should call on Jev for recurring judgments — verification, screening, reranking, classification — in the middle of a task, and other MCP clients can connect the same way. As a third-party project it is not maintained by TypeSafe AI; tool names, carrier options, and behavior should be checked against the repository before production use, and snapshot figures should be dated when they are cited.

## Links

- [GitHub – jkudish/jev-mcp](https://github.com/jkudish/jev-mcp)

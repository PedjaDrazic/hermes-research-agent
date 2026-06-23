# Scan Sources

Concrete feeds and pages to check each run, mapped to the lanes in interests.yaml.
Customize the company/news pages to your niche. The access-pattern notes below are
general learnings that apply to any Hermes research agent.

## Source Access Notes (read these — they save you from broken scrapes)
- **HN front page, GitHub trending, HuggingFace papers** — all work reliably with `web_extract`. No browser needed. Extract each in parallel for speed.
- **X/Twitter account monitoring** — `web_search` with `site:x.com` produces unreliable or empty results for specific account handles. `web_extract` on X profile URLs frequently times out (504 / Firecrawl timeout) and should not be relied on as primary access. Preferred approaches:
  - `web_search` with a broad topic query (no `site:` filter) plus the account name — finds external coverage mentioning the account.
  - **LinkedIn search** as a reliable fallback: `web_search` with the account name + topic + "LinkedIn" or `site:linkedin.com` — consistently returns real post content for most public figures.
  - For the competitor lane, cross-reference external coverage (TechCrunch, VentureBeat, articles mentioning the account's recent posts).
  - Medium articles, Substack posts, and blogs by or about the account are more reliable than raw X scrapes.
- **Date-slug news roundups** — some AI-news sites use date-based URL slugs (e.g. `/blogs/ai-news-today-{month}-{day}-{year}`). The generic URL often 404s. Use `web_search("site:thesite.com ai news today")` to discover the latest slug before extracting.
- **JS-heavy SPA pages** (trending dashboards, prediction markets) — `web_extract` returns near-empty content because the page renders client-side. Use the browser tool instead, or fall back to a simpler source (e.g. GitHub trending directly).
- **Prediction markets (Polymarket)** — `web_extract` on generic event URLs fails. Each market has a unique URL suffix. Use `web_search("Polymarket {event description}")` to find the specific market URL, then use the browser tool (JS-heavy).
- **Reddit** — `web_extract` returns "Website Not Supported". Use `web_search("site:reddit.com {topic} {keyword}")` to surface threads, then open specific threads via the browser tool.

## Official Company / News Pages (check before third-party coverage)
Replace these with the primary sources for YOUR niche. Examples for an AI-focused agent:
- https://anthropic.com/news/ — model releases, policy, safety statements
- https://openai.com/blog/ — model releases, pricing, policy
- https://blogs.nvidia.com/ — infrastructure, benchmarks
- https://ai.meta.com/blog/ — open-source model releases
- https://blog.google/technology/ai/ — Gemini, DeepMind
- https://mistral.ai/news/ — Mistral releases

## Benchmarks & Leaderboards (adjust to your domain)
- https://www.artificialanalysis.ai/ — model benchmarks & leaderboards
- https://lmarena.ai/ — Chatbot Arena rankings
- https://huggingface.co/papers — trending ML papers + model releases

## Frameworks, Tools, Open-Source Momentum
- https://github.com/trending/python?since=weekly — trending repos
- https://ossinsight.io/blog/ — ecosystem trend analysis (blog pages extract well; the SPA trending page does not)
- https://news.ycombinator.com/ — search "agent" OR "framework" OR "tool use"
- https://www.reddit.com/r/LocalLLaMA/ — open-source model buzz (use browser tool per access notes)

## Founder / Researcher Reactions on X
- Maintain your own follow list of the voices that matter in your niche.
- Search pattern: `"hot take" OR "unpopular opinion" OR "I think"` from verified accounts in your space.

## Papers Worth Knowing (arXiv)
- https://arxiv.org/list/cs.AI/recent
- https://arxiv.org/list/cs.LG/recent
- https://huggingface.co/papers — trending papers with summaries

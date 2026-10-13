<!-- Fill from this repository's verified source and ownership records. Remove unused sections and unknown service examples; do not invent owners, credentials, environments, or capabilities. -->
# {tool-name}

{2-3 sentences: what problem this solves, why it exists here (not a pitch, assume the reader knows the domain).}

**Owner:** {team name}, `#{slack-channel}` on Slack  
**On-call:** {PagerDuty rotation name | @person | "file an issue in this repo"}

---

## Where it runs

| Environment | {Cluster / URL} | Dashboard |
|---|---|---|
| dev | {dev cluster or URL} | [{monitoring link text}]({url}) |
| staging | {staging cluster or URL} | [{monitoring link text}]({url}) |
| prod | {prod cluster or URL} | [{monitoring link text}]({url}) |

<!-- Delete environments that don't apply. Add rows for others. -->

---

## Setup

**Prerequisites:** {language version, required CLI tools, access requirements}

```bash
{clone or install command}
cd {repo-name}
{install deps command}
cp .env.example .env
```

{Where to get credentials: "Fill in `.env` from `{1Password vault path}` or ask `#{slack-channel}`."}

---

## Running

```bash
{start command}
# Expected output when healthy: "{example log line}"
```

{Optional: additional run modes, flags, or environment overrides.}

```bash
{example of a common variant command}
# e.g. TABLE=users npm run sync:once
```

---

## Known failure modes

<!-- Document the top 3-5 failure modes that have actually happened. This is the most valuable section. -->

| Symptom | Likely cause | Fix |
|---|---|---|
| {error message or symptom} | {cause} | {command or action} |
| {error message or symptom} | {cause} | {command or action} |

---

## Architecture

<!-- Delete this section for simple tools. Keep for anything with unusual design decisions. -->

{1-3 paragraphs explaining non-obvious design choices. Why this approach vs alternatives. What to know before making changes.}

---

## Documentation

{Link to the existing setup guide, architecture knowledge, runbook, requirements, and other team documents. Label restricted sources. Do not invent a library layout if this repository uses another one.}

| Task | Starting document | Audience |
| --- | --- | --- |
| {task} | {verified_document_link} | {internal_or_public} |

{If this tool prepares or generates documents, show the actual invocation and required inputs, where outputs are saved, their formats, and how to review them. Explain which files are maintained sources and which are generated. Keep private citations, source paths, and review records out of public deliverables. Remove when not applicable.}

## Contributing

{Who can contribute. PR process. How to run tests locally.}

```bash
{test command}
```

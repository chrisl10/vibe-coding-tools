# Editorial preferences (repo-radar-stinger)

This is the one file a user edits to make the skill theirs. The skill reads it at the start of every run, before the ledger. Every value below ships as a neutral default; replace the values, keep the headings.

If a heading is missing or a value is left at its default, use the default. Never infer a persona, political stance, or set of beliefs that this file does not state.

## 1. Voice skill

- Voice skill: `none`

Set this to the name of the skill that holds your writing voice, for example `<name>-voice-skill`. The skill must be installed and available in your assistant.

- When a voice skill is named and available: load it before drafting and follow its full workflow (register, length guides, calibration, and any anti-AI or punctuation rules). Its rules override the length bands and punctuation notes in this pack.
- When it is `none`, or the named skill is not available: write every option in a neutral, clear, plain voice (direct sentences, no slang, no persona, no invented first-person history) and state in the output header that no voice skill was configured, so the user knows the drafts are not voice-matched. Do not imitate a voice you have not inspected.

## 2. Beats and topics

Beats are the subject areas worth scanning. These are example defaults; replace the list with your own. Earlier entries rank higher when candidates tie.

1. Vibe coding and AI-assisted development tools (agents, IDE tooling, agent skills)
2. AI coding models, frameworks, and benchmarks
3. AI memory systems (agent memory, RAG infrastructure, vector stores, context tooling)
4. Security: newly disclosed vulnerabilities, CVE proof-of-concepts, supply-chain write-ups, security tooling
5. Anything else genuinely remarkable on the board that a builder audience would care about

Audience (who the posts are for): software builders. Replace with your own audience.

## 3. Editorial policy (optional)

The default policy is politically neutral. Edit it to record topics to avoid or emphasize; leave the defaults if you have no preference.

Defaults:

- Avoid partisan advocacy. Do not write posts whose purpose is to promote or attack a party, candidate, or movement.
- Vet every claim to the standard in `references/repo-vetting.md`. Stories critical of any person or institution are fine when the receipts hold.
- Present contested issues fairly: state the verified facts, name the opposing positions accurately, and label opinion as opinion.
- Skip celebrity gossip crossovers and personal-life stories unless they carry verified, newsworthy facts that matter to the audience.

Topics to avoid (add your own, one per line; none by default):

- (none)

Topics to emphasize (add your own, one per line; none by default):

- (none)

An entry in the avoid or emphasize lists changes which candidates the skill picks. It never relaxes the accuracy gates: no fabricated stars, capabilities, quotes, or severity.

## 4. Output and ledger

- Length bands for the three post options: micro up to 9 words, medium 10-60 words, long form 200+ words. A configured voice skill's bands override these.
- Topic ledger path: `/areas/content-post-ledger.md` in user memory. Change it only if your memory layout differs; both skills in this pack must use the same path.

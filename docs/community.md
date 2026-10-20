# Community plan (not built yet)

Wealth Tax Supporters began as a sourced database of public figures and organisations that back a wealth tax. The aim behind it is wider: to make it easy for people who share that view to find each other, wherever they are. The database is the backbone and stays as it is. This page records the decisions made so far and the plan for a community layer, so that nothing is built by accident or in the wrong order.

**Status:** nothing described below is implemented. The site shows only the public-figure database. There are no accounts, no registration and no forum.

## Decisions so far

- **Operator:** one person (the repository owner), for now. That affects what is safe to build: a service that holds personal data needs a responsible party, and it is currently an individual.
- **Name and address:** Wealth Tax Supporters, `wealthtaxsupporters.com`.
- **Hosting:** the site is a static page. The community layer will run on Cloudflare (Pages and Functions for the site and API, D1 for the database), so that it is one platform and the domain's DNS is managed in one place.
- **Not yet:** letting ordinary people add themselves, any forum, messaging between people. The current model stays: public figures and organisations only, every entry sourced.
- **Stance of the service:** supporters only. The database and the community both exist for people who back a wealth tax.

## Principles for the community layer

1. **Separate the two kinds of data.** The public-figure database lives in this repository under CC BY 4.0. Anything about ordinary members lives only in a private database, with no open licence, and is never committed to git.
2. **Opt-in, consent recorded.** Support for a wealth tax is a political opinion, which is special-category data in the UK and EU. Collect it only with explicit, logged consent, and let people delete everything.
3. **Collect as little as possible.** No real names or emails shown to others. A display name is optional. Store a hashed account identifier, not the account's contents.
4. **Coarse places only.** Show people at the level of a county or region, never a pin. Show only counts for an area until enough people are in it, so that nobody can be picked out.
5. **Public figures by default.** A filter shows public figures and organisations by default. Ordinary members appear in a separate, opt-in layer.
6. **Make contact safe.** The first version only shows counts and points people to a shared space. Messaging between members, if it ever exists, goes through the site and never exposes an account.

## Proving a stance (when registration is built)

The idea is that a person shows they hold the view in a public post that is reasonably theirs:
1. They sign in with an account on an open platform (OAuth), which shows they control it.
2. The site gives them a short text and a one-time code. They post it publicly and paste the link.
3. The site fetches the post and checks that the code is there and that the author matches the signed-in account.

This is practical for Bluesky, Mastodon and Reddit, whose public APIs are open. X and Facebook restrict or charge for post access, so they would come later. People who cannot post publicly (for work or safety reasons) are left out, which is an accepted trade-off.

## Stages

1. **Now:** rename, domain, Cloudflare hosting, this plan, the draft database schema (`infra/d1/schema.sql`). Nothing live.
2. **A "find others" page:** counts of supporters per area from the database, plus a link to an existing community space. No accounts. This tests whether anyone wants it.
3. **Registration:** sign-in, a stance post, consent, a coarse location, an opt-in layer. Only after the legal checklist below is done.
4. **A forum or messaging:** only if there is demand and someone to moderate it. A hosted forum or an existing platform is likelier than building one.

## Before any ordinary person can register

- A privacy policy and terms, and a contact address for requests (Cloudflare Email Routing can provide one).
- A named controller, and a decision on whether to set up an association or non-profit.
- Whether registering with the data-protection authority is required where the operator is based.
- An age limit, a deletion process, a retention period and a breach plan.
- Rate limits and abuse reporting, so the layer cannot be scraped or brigaded.
- A moderation plan, if anything like a forum is added.

## Where things live

| Thing | Where |
|---|---|
| Public-figure database | `data/<iso2>/` (CC BY 4.0) |
| Site | `site/`, built by `scripts/build_site.py` |
| Hosting, API, database (future) | Cloudflare: see `infra/README.md` |
| Community data (future) | Cloudflare D1 only. Never in this repository |

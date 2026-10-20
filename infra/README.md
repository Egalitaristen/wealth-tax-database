# Cloudflare setup

How `wealthtaxsupporters.com` is hosted. The site is static today. This setup also gets the domain, hosting and an (empty) database ready for the community layer described in `docs/community.md`. Nothing here collects any user data.

## 1. Put the domain on Cloudflare

The domain is registered at GoDaddy. A new registration cannot be transferred to another registrar for 60 days, and moving it early may forfeit GoDaddy's multi-year promotion. You do not need to transfer it. Point its nameservers at Cloudflare instead:

1. Cloudflare dashboard → **Add a domain** → `wealthtaxsupporters.com` → Free plan. Cloudflare shows two nameservers.
2. GoDaddy → the domain → **DNS** → **Nameservers** → **Change** → "I'll use my own nameservers" → enter the two Cloudflare ones.
3. Wait until Cloudflare shows the domain as **Active** (minutes to a few hours).
4. Optional, later: transfer the registration to Cloudflare once the 60 days have passed and the GoDaddy term no longer matters.

## 2. Host the site on Cloudflare

The site is deployed from the maintainer's machine as a Cloudflare Worker with static assets. That is what Cloudflare Pages has become. Nothing builds on GitHub.

1. Install Node.js and run `npx wrangler login` once.
2. In Cloudflare DNS, delete any records on `wealthtaxsupporters.com` and `www` left over from GoDaddy (parking `A` records, the `www` CNAME). Custom domains cannot be attached while other records hold those names.
3. Run `python scripts/deploy.py`. It builds `_site/` and runs `wrangler deploy` with the settings in `wrangler.jsonc`:
   - the static assets
   - the single-page fallback for clean URLs
   - the custom domains `wealthtaxsupporters.com` and `www.wealthtaxsupporters.com`, with DNS records and certificates created by Cloudflare
4. Turn GitHub Pages off in the repository settings so the old address stops serving a stale copy.

Deploy again whenever `main` changes. The `validate` workflow on GitHub still checks pull requests.

## 3. Email for requests (needed before any registration)

Cloudflare dashboard → **Email** → **Email Routing** → create an address such as `contact@wealthtaxsupporters.com` that forwards to your own inbox. Use it for correction and removal requests and, later, the privacy policy.

## 4. The database (when you are ready)

Install the CLI and sign in: `npx wrangler login`.

```bash
npx wrangler d1 create wts-community
cp infra/wrangler.toml.example wrangler.toml     # then fill in the database_id and uncomment the d1 block
npx wrangler d1 execute wts-community --remote --file infra/d1/schema.sql
```

Set the secrets for the API (never commit them):

```bash
npx wrangler pages secret put HASH_KEY
npx wrangler pages secret put SESSION_SECRET
```

Nothing reads the database yet. Do not open registration until the checklist in `docs/community.md` is done.

## Rules for this folder

- No secrets, no `.dev.vars`, no database dumps in git. `.gitignore` covers the usual names.
- Community data lives only in D1. The public-figure database stays in `data/` under CC BY 4.0.

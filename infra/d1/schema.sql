-- DRAFT. Not deployed, and nothing in this repository reads it.
-- Community data lives only in Cloudflare D1 and is never committed to git. See docs/community.md.
-- Designed for: opt-in members, a public post that proves a stance, coarse places, logged consent and real deletion.

CREATE TABLE members (
  id              TEXT PRIMARY KEY,                -- random id (UUID), unrelated to any account
  created_at      TEXT NOT NULL,                   -- ISO 8601
  status          TEXT NOT NULL DEFAULT 'pending'  -- pending | verified | suspended
                  CHECK (status IN ('pending', 'verified', 'suspended')),
  display_name    TEXT,                            -- optional pseudonym; never a required real name
  country         TEXT NOT NULL,                   -- ISO 3166-1 alpha-2
  area_path       TEXT,                            -- coarse place, e.g. 'United Kingdom > Wales > Conwy'; never finer than a county
  visibility      TEXT NOT NULL DEFAULT 'hidden'   -- hidden | counted (in area totals only) | listed (shown by display name)
                  CHECK (visibility IN ('hidden', 'counted', 'listed')),
  consent_version TEXT NOT NULL,                   -- version of the privacy text they agreed to
  consent_at      TEXT NOT NULL,
  verified_at     TEXT
);

-- The account used to prove the stance. Only a keyed hash of the platform's user id is stored.
CREATE TABLE identities (
  member_id    TEXT NOT NULL REFERENCES members(id) ON DELETE CASCADE,
  platform     TEXT NOT NULL CHECK (platform IN ('bluesky', 'mastodon', 'reddit', 'x', 'facebook')),
  subject_hash TEXT NOT NULL,                      -- HMAC of the platform user id; not reversible without the server key
  handle       TEXT,                               -- stored only if the member chooses to be listed with it
  UNIQUE (platform, subject_hash)
);

-- A public post that states the person's stance, with a one-time code.
CREATE TABLE verifications (
  id           TEXT PRIMARY KEY,
  member_id    TEXT NOT NULL REFERENCES members(id) ON DELETE CASCADE,
  platform     TEXT NOT NULL,
  code         TEXT NOT NULL,
  post_url     TEXT,
  requested_at TEXT NOT NULL,
  checked_at   TEXT,
  result       TEXT CHECK (result IN ('ok', 'not_found', 'author_mismatch', 'expired'))
);

CREATE TABLE consent_log (
  member_id       TEXT NOT NULL,                   -- kept without a foreign key so the log can outlive the member
  consent_version TEXT NOT NULL,
  action          TEXT NOT NULL CHECK (action IN ('given', 'withdrawn')),
  at              TEXT NOT NULL
);

CREATE TABLE reports (
  id          TEXT PRIMARY KEY,
  target_type TEXT NOT NULL CHECK (target_type IN ('member', 'post')),
  target_id   TEXT NOT NULL,
  reason      TEXT NOT NULL,
  created_at  TEXT NOT NULL,
  status      TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'actioned', 'dismissed'))
);

-- Deleting a member removes their rows (ON DELETE CASCADE) and any posts; the consent_log keeps only ids and dates.
CREATE INDEX idx_members_area ON members (country, area_path, status, visibility);

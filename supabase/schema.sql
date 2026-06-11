-- Enum for post status
CREATE TYPE post_status AS ENUM ('draft', 'published');

-- Posts table
CREATE TABLE posts (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title_marathi   TEXT NOT NULL,
    title_english   TEXT,
    body_marathi    TEXT NOT NULL DEFAULT '',
    body_english    TEXT,
    slug            TEXT UNIQUE NOT NULL,
    status          post_status NOT NULL DEFAULT 'draft',
    published_at    TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Post images table
CREATE TABLE post_images (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id         UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    storage_url     TEXT NOT NULL,
    page_order      INTEGER NOT NULL DEFAULT 0,
    ocr_raw_text    TEXT,
    ocr_confidence  FLOAT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Auto-update updated_at on posts whenever a row changes
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER posts_updated_at
    BEFORE UPDATE ON posts
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

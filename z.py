'''docker run --name Python_proj_db \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -p 5432:5432 \
  -d postgres




docker exec -it Python_proj_db psql -U postgres





CREATE DATABASE items_storage;
\c items_storage;






-- tasks (все задачи)
CREATE TABLE tasks (
  id              SERIAL PRIMARY KEY,
  title           VARCHAR(255) NOT NULL,
  details         TEXT,
  tags            TEXT[] DEFAULT '{}',   -- список тегов
  telegram_id     VARCHAR(64),
  deadline        TIMESTAMPTZ,
  completed       BOOLEAN DEFAULT FALSE,
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- reminders (отдельные напоминания)
CREATE TABLE reminders (
  id              SERIAL PRIMARY KEY,
  title           VARCHAR(255) NOT NULL,
  details         TEXT,
  tags            TEXT[] DEFAULT '{}',
  telegram_id     VARCHAR(64),
  scheduled_at    TIMESTAMPTZ,
  sent            BOOLEAN DEFAULT FALSE,
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- tags (справочник тегов, если нужен)
CREATE TABLE tags (
  name        VARCHAR(100) PRIMARY KEY,
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

'''
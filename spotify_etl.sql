DROP TABLE IF EXISTS "track" CASCADE;
DROP TABLE IF EXISTS "album" CASCADE;

DROP TABLE IF EXISTS "artist" CASCADE;

DROP TABLE IF EXISTS "artist_track" CASCADE;

DROP TABLE IF EXISTS "artist_album" CASCADE;

DROP TABLE IF EXISTS "artist_genre" CASCADE;
DROP TABLE IF EXISTS "track_album" CASCADE;





CREATE TABLE "track" (
  "track_id" text PRIMARY KEY,
  "track_name" text,
  "track_url" text,
  "duration_ms" integer,
  "release_date" timestamp,
  "is_single" BOOLEAN,
  "explicit" boolean
);

CREATE TABLE "album" (
  "album_id" text PRIMARY KEY,
  "album_name" text,
  "release_date" timestamp,
  "album_url" text,
  "total_tracks" integer,
  "type" text,
  "image_640_url" text,
  "image_300_url" text,
  "image_64_url" text
);

CREATE TABLE "artist" (
  "artist_id" text PRIMARY KEY,
  "name" text,
  "url" text,
  "image_640_url" text,
  "image_320_url" text,
  "image_160_url" text
);

CREATE TABLE "artist_track" (
  "artist_id" text,
  "track_id" text
);

CREATE TABLE "artist_album" (
  "artist_id" text,
  "album_id" text
);

CREATE TABLE "artist_genre" (
  "artist_id" text,
  "genre" text
);

CREATE TABLE "track_album" (
  "track_id" text,
  "album_id" text
);

ALTER TABLE "artist_track" ADD FOREIGN KEY ("artist_id") REFERENCES "artist" ("artist_id");

ALTER TABLE "artist_album" ADD FOREIGN KEY ("artist_id") REFERENCES "artist" ("artist_id");

ALTER TABLE "artist_track" ADD FOREIGN KEY ("track_id") REFERENCES "track" ("track_id");

ALTER TABLE "artist_album" ADD FOREIGN KEY ("album_id") REFERENCES "album" ("album_id");

ALTER TABLE "artist_genre" ADD FOREIGN KEY ("artist_id") REFERENCES "artist" ("artist_id");

ALTER TABLE "track_album" ADD FOREIGN KEY ("track_id") REFERENCES "track" ("track_id");

ALTER TABLE "track_album" ADD FOREIGN KEY ("album_id") REFERENCES "album" ("album_id");

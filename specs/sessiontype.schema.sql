CREATE TABLE "SessionType" (
    "id" VARCHAR,
    "title" VARCHAR,
    "purpose" VARCHAR,
    "run_spec" VARCHAR,
    "extends" VARCHAR,
    "nudges" VARCHAR[],
    "context_policy" VARCHAR,
    "access_policy" VARCHAR,
    "output_policy" VARCHAR,
    "cadence_policy" VARCHAR
);

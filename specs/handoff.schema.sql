CREATE TABLE "Handoff" (
    "id" VARCHAR,
    "title" VARCHAR,
    "created_at" TIMESTAMPTZ,
    "status" VARCHAR,
    "created_by_run" VARCHAR,
    "target_session_type" VARCHAR,
    "state" VARCHAR,
    "next_action" VARCHAR,
    "references" VARCHAR[],
    "continued_by_run" VARCHAR,
    "archived_at" TIMESTAMPTZ,
    "resolution" VARCHAR
);

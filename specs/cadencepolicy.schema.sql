CREATE TABLE "CadencePolicy" (
    "id" VARCHAR,
    "title" VARCHAR,
    "on_demand" BOOLEAN,
    "event_triggers" VARCHAR[],
    "interval_seconds" BIGINT,
    "threshold_metric" VARCHAR,
    "threshold_gte" BIGINT,
    "cooldown_seconds" BIGINT,
    "max_delay_seconds" BIGINT,
    "priority" BIGINT,
    "max_parallel" BIGINT,
    "max_runs_per_hour" BIGINT,
    "handoff_compatible" BOOLEAN
);

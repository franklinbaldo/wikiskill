CREATE TABLE "RunOutcome" (
    "id" VARCHAR,
    "run" VARCHAR,
    "result_state" VARCHAR,
    "summary" VARCHAR,
    "next_move" VARCHAR,
    "goals_advanced" VARCHAR[],
    "evidence" VARCHAR[],
    "checks" VARCHAR[],
    "experiences_recorded" VARCHAR[]
);

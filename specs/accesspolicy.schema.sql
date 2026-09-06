CREATE TABLE "AccessPolicy" (
    "id" VARCHAR,
    "title" VARCHAR,
    "mode" VARCHAR,
    "repositories" VARCHAR[],
    "paths" VARCHAR[],
    "connectors" VARCHAR[],
    "instructions" VARCHAR[]
);

DROP TABLE if exists madlibs;
CREATE TABLE madlibs (
    id INTEGER PRIMARY KEY autoincrement,
    bus_name TEXT NOT NULL,
    bus_type TEXT NOT NULL,
    market_type TEXT NOT NULL,
    job_be_done TEXT NOT NULL,
    rev_model TEXT NOT NULL
);
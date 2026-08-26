PRAGMA foreign_keys = ON;

CREATE TABLE subjects (
    subject_id TEXT PRIMARY KEY,
    project TEXT NOT NULL CHECK (project IN ('prj1', 'prj2', 'prj3')),
    condition TEXT NOT NULL CHECK (condition IN ('melanoma', 'carcinoma', 'healthy')),
    age INTEGER NOT NULL,
    sex TEXT NOT NULL CHECK (sex IN ('M', 'F')),
    treatment TEXT NOT NULL CHECK (treatment IN ('miraclib', 'phauximab', 'none')),
    response TEXT CHECK (response IN ('yes', 'no'))
);

CREATE TABLE samples (
    sample_id TEXT PRIMARY KEY,
    subject_id TEXT NOT NULL,
    sample_type TEXT NOT NULL CHECK (sample_type IN ('PBMC', 'WB')),
    time_from_treatment_start INTEGER NOT NULL,
    b_cell INTEGER NOT NULL,
    cd8_t_cell INTEGER NOT NULL,
    cd4_t_cell INTEGER NOT NULL,
    nk_cell INTEGER NOT NULL,
    monocyte INTEGER NOT NULL,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE
);

CREATE INDEX idx_subjects_filtering ON subjects (condition, treatment, response);
CREATE INDEX idx_samples_lookup ON samples (subject_id, time_from_treatment_start);

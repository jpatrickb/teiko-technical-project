# Notes

Five Populations (values in each are counts):
- `b_cell`
- `cd8_t_cell`
- `cd4_t_cell`
- `nk_cell`
- `monocyte`

Metadata:
- Project:
  - `prj1`
  - `prj2`
  - `prj3`
- Subject:
  - `sbj000`-`sbj3499`
- Condition
  - `melanoma`
  - `carcinoma`
  - `healthy`
- Age
  - 50-79
- Sex
  - M
  - F
- Treatment
  - `miraclib`
  - `phauximab`
  - `none`
- Response
  - `yes`
  - `no`
  - `nan` (shows up as blank in the CSV, `nan` in pandas)
- Sample (3 samples per subject, taken 0, 7, and 14 days/units of time after treatment began)
  - `sample00000`-`sample10499`
- Sample Type (`sample_type`)
  - `PBMC`
  - `WB`
- Time from treatment start
  - 0
  - 7
  - 14


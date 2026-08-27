# Teiko Cell Count Analysis Project
*Author: Patrick Beal*

First off, I want to say to whoever is reading this that I really loved this project! Even though I've loved my current position, I enjoyed this project much more than the type of work I've been doing, so I would love to further explore the possibility of working at Teiko. 

## Quickstart

To run this app or reproduce the results, you can use the makefile:

```bash
make setup && make pipeline && make dashboard
```

(If you're running this in GitHub Codespaces, the `localhost` link that streamlit provides you should open up just fine)

Otherwise, if you prefer to run each step manually, follow these steps to run using `uv` (my favorite package/project manager):

```bash
# Get uv
pip install --quiet uv

# get requirements
uv sync

# Load data, run analysis, and open dashboard
uv run load_data.py
uv run analysis.py
uv run streamlit run dashboard.py
```

(Test in github codespace before adding instructions/notes about that)

## DB Setup

I chose to set up a database with two separate tables (`subjects` and `samples`) because the dataset is compromised of 3500 individuals (subjects) who each had three samples taken from them.
Storing each of these in one table means that much of the subject data that is irrelevant to some of the later analysis will be duplicated inefficiently, so two tables allows us to reduce the total size of the dataset, while still allowing us to query the information we need efficiently. 
Also, I used pandas to manually examine the data to identify empty values, unique values, and ranges, so that we can enforce specific values (including not null) on each column in the database to ensure that the data remains clean as we port it into the database, or if we were to add more data.

As we scale in number of projects and samples, this setup is far more efficient than the long format the CSV came in, because we reduce redundant data drastically. If future projects require more metadata than just the ID, then it would be worth breaking that into a third table, which would further reduce redundant data. I also created indexes for common queries that would allow the database to scale as the number of samples grow, because we don't have to check every row for entries matching a given condition, so queries will be much more efficient.

## Code Structure

I have split my code into three distinct python modules, each carrying one primary purpose:
- **`load_data.py`** — This is the file that loads the data from the CSV and writes it to the database. Runs once, and we never read the CSV again
- **`analysis.py`** — Runs the analysis to return the results for each of the problems described. Saves results to CSV (or text, in the case of the average number of b cells)
- **`dashboard.py`** — Creates a streamlit dashboard, loading in the CSV files with the results of the analysis for interactive viewing.

Because the project is quite small and the `load_data.py` file was supposed to be in the project root, I decided to keep the other two files (`analysis.py` and `dashboard.py`) in the project root as well. If there were more files, and they could be grouped by functionality or services, then I would break down into multiple directories for better organization and systemetization of the code. 

I chose to keep the analysis all contained in one file because it was a brief analysis, and even with minimal overlap between the functions the file is still short even with all three analysis functions (plus a function to save the outputs).

Similarly, the streamlit dashboard is pretty minimal, and just shows the dataframes of the outputs, so it was more simple to do in one file than to break up into different components across files.

## Dashboard

You can view my active dashboard on [Streamlit](https://teiko-technical-project-jpatrickb.streamlit.app/) at https://teiko-technical-project-jpatrickb.streamlit.app/.

Thank you!
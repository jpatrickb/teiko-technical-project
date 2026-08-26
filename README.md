# 

## Part 1: Data Management

### DB Setup

I chose to set up a database with two separate tables (`subjects` and `samples`) because the dataset is compromised of 3500 individuals (subjects) who each had three samples taken from them.
Storing each of these in one table means that much of the subject data that is irrelevant to some of the later analysis will be duplicated inefficiently, so two tables allows us to reduce the total size of the dataset, while still allowing us to query the information we need efficiently.



## 
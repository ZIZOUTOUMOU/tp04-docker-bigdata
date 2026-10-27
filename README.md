# TP04 - Containerization and Big Data Environment Deployment Using Docker

Module: Big Data Analytics - Master 2 AI & Data Science - University of Eloued - 2026/2027

Docker Hub image: https://hub.docker.com/r/zizoutoumou/tp04-analysis (tag v1)

## What this project does
A Dockerized Python (pandas) version of the TP03 analysis of the Kaggle dataset
"eCommerce behavior data from multi-category store" (October and November 2019, 14 GB).
The CSV files are read in chunks of 1-2 million rows and are mounted into the container
at run time. They are not stored in the image or in this repository.

## Full report
Open TP04_report.html (all tasks, screenshots and answers to the questions).

## Dataset
Download 2019-Oct.csv and 2019-Nov.csv from Kaggle and place them in the data/ folder.
data/sample.csv (first 100,000 rows of November) is included for a quick test.

## Run it
docker pull zizoutoumou/tp04-analysis:v1

Quick test on the sample:
docker run --rm -v "${PWD}/data:/app/data:ro" zizoutoumou/tp04-analysis:v1

Full November file:
docker run --rm -e DATA_FILE=2019-Nov.csv -v "${PWD}/data:/app/data:ro" zizoutoumou/tp04-analysis:v1

With Docker Compose (full November file):
docker compose up --build
docker compose down

## Results (full dataset)
| | October | November |
|---|---|---|
| Rows | 42,448,764 | 67,501,979 |
| Unique users | 3,021,435 | 3,695,107 |
| Purchases | 742,773 | 916,930 |
| Revenue | 229.93 M USD | 275.19 M USD |
| Conversion | 1.75 % | 1.36 % |

## Notes
- Duplicates are removed inside each chunk, not across the whole file.
- The sample.csv file is a real extract of the November data.

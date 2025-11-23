# Space Launch Data Collection and Processing

Data acquisition and preprocessing pipeline for collecting historical rocket launch data from the Space Devs Launch Library 2 API, for DSCI 511 group term project at Drexel University.  

## Description

This project collects and processes comprehensive historical data on rocket launches using the Space Devs Launch Library 2 API. (It should be noted this project does not analyze any data.) The team extracted over 7,300 launch records spanning from 1957 to present, focusing on three main data categories: rocket specifications, launch details, and mission parameters. Each team member cleaned a specific subset of parameters, which were then merged into a unified dataset. The final dataset includes information on launch vehicles, manufacturers, launch sites, mission types, orbits, and launch outcomes, ready for future analysis.

## Distribution & Access

### Data Source Rights
Our dataset uses the **Launch Library 2 API** (https://ll.thespacedevs.com/), which provides public space launch data for research and educational purposes.

- **Source:** The Space Devs Launch Library 2
- **License:** Public API, no documented restrictions for educational use
- **Our work:** Data collection, cleaning, integration, and documentation
- **Attribution:** Dataset credits Launch Library 2 API as source

### How to Use This Dataset

**Load the data:**
```python
import pandas as pd
df = pd.read_csv('data/merged_launch_data.tsv', sep='\t')
```

**Quick overview:**
```python
print(f"Total launches: {len(df)}")
print(f"Date range: {df['Launch Date'].min()} to {df['Launch Date'].max()}")
print(f"Attributes: {len(df.columns)}")
```

### Dataset Contents
- **merged_launch_data.tsv** - Complete dataset (7,333 launches, 39 attributes)
- **clean_rocket_data.tsv** - Rocket specifications (15 attributes)
- **clean_launch_data.tsv** - Launch details (16 attributes)
- **clean_mission_data.tsv** - Mission parameters (10 attributes)

### Dataset Overview

Quick statistics about the collected data:

| Metric | Value |
|--------|-------|
| Total Launches | 7,333 |
| Time Span | 1957-2024 |
| Countries | 47 |
| Unique Rockets | 450+ |
| Total Attributes | 39 |
| File Size | 2.1 MB |

### Reproducing Our Collection
All collection and cleaning code is provided in this repository:
1. Run `Space_Launch_Acquisition_Pagination.ipynb` to collect data
2. Run individual cleaning notebooks for each parameter set
3. Run `Merge_3_Cleaned_DataFrames.ipynb` to integrate

**Note:** Full collection takes ~5-6 hours due to API rate limiting (15 requests/hour)

### Extending the Dataset
To collect launches since our last update:
```python
import requests

# Get latest launches
url = "https://ll.thespacedevs.com/2.2.0/launch/?limit=100"
response = requests.get(url)
new_data = response.json()['results']
```

### Data Quality
- Historical launches (pre-2000s) have incomplete technical specifications
- Missing values are documented in cleaning notebooks
- Launch IDs preserved for verification against API

## Getting Started

### Dependencies

* Python 3.8 or higher
* Required Python packages:
  * pandas
  * requests
  * json (built-in)
  * datetime (built-in)
  * dateutil
  * pprint (built-in)
* Google Colab or Jupyter Notebook environment
* Google Drive account (for file storage in Colab)
* GitHub

### Installing

1. Clone the repository to your local machine or Google Drive
```
git clone https://github.com/Rybus07/space-legends-data.git
```

2. Install required packages (if running locally):
```
pip install pandas requests python-dateutil
```

3. If using Google Colab, mount your Google Drive:
```python
from google.colab import drive
drive.mount('/content/drive')
```

4. Update file paths in notebooks to match your directory structure

5. Note: Space Devs Launch Library 2 API does not require an API Access Key

### Executing Program

The project consists of three main phases:

**Phase 1: Data Collection**
* Set TEST_MODE flag to False for full collection (5-6 hours due to rate limiting)
* Enter collector_name for metadata of the collection and the output filename
* Run `Space_Launch_Acquisition_Pagination.ipynb` to collect raw launch data from API
* Output: `raw_baseline_launches_[collector_name].json`

**Phase 2: Data Cleaning**
* Run cleaning notebooks for each data category:
  * `Data extraction - rocket.ipynb` - Extracts rocket parameters
  * `DSCI_511_Launch_parameters.ipynb` - Extracts launch parameters
  * `Data Extraction - Mission parameters.ipynb` - Extracts mission parameters
* Output: Three TSV files (clean_rocket_data.tsv, clean_launch_data.tsv, clean_mission_data.tsv)

**Phase 3: Data Merging**
* Run `Merge_3_Cleaned_DataFrames.ipynb` to combine all cleaned data
* Output: `merged_launch_data.tsv` - Final dataset ready for analysis

**Important:** Update file paths in each notebook to match your directory structure before running.

## Help

**Common Issues:**

* **FileNotFoundError**: Update file paths in notebooks to match your directory structure
* **API Rate Limiting**: The Space Devs API allows 15 requests/hour. The pagination code includes automatic pausing.
* **Missing Values After Merge**: Normal - not all launches have complete data in the API
* **Google Drive Mount Issues**: Re-run the drive.mount() cell in Colab
* **Google Colab Session Timeout**: Files saved to Colab's temporary storage will be lost after session timeout. Save important files to Google Drive to prevent data loss.
* **Size of JSON**: Size of the file after full collection (of more than 7,000 launches) is more than 341MB. The file will need to be saved in Google Drive or zipped for GitHub. 

For questions about the project, contact team members (see Authors section).

## Authors

DSCI 511 Project Group 7

* Jillian Kunze - jk3987@drexel.edu 
* Innocent Gumunyu - ig384@drexel.edu
* Ryan Peters - rap369@drexel.edu
* Phillip Roman - pjr322@drexel.edu

## Version History

* 1.0 (November 2025)
    * Initial release - Complete data collection and preprocessing pipeline
    * 7,333 launches collected and cleaned
    * Three-way merge functionality implemented

## License

This project is for educational purposes as part of DSCI 511 coursework at Drexel University.

Data sourced from [The Space Devs Launch Library 2 API](https://thespacedevs.com/llapi).


## Acknowledgments

* [The Space Devs](https://thespacedevs.com/) - Launch Library 2 API
* [Space Devs API Documentation](https://ll.thespacedevs.com/docs/)
* [Stack Overflow pagination example](https://stackoverflow.com/questions/56206038/how-to-loop-through-paginated-api-using-python)
* DSCI 511 course materials and instructor and TAs
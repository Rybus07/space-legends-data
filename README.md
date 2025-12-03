# Space Launch Data Collection and Processing

Data acquisition and preprocessing pipeline for collecting historical rocket launch data from the Space Devs [Launch Library 2 API](https://thespacedevs.com/llapi), for DSCI 511 group term project at Drexel University.  

## Description

This project acquires and pre-processes comprehensive historical data on rocket launches using the Space Devs Launch Library 2 API. The team extracted over 7,300 launch records spanning from 1957 to the present with code found in `01_Acquisition.ipynb`, focusing on three main categories of data: rocket specifications, launch information, and mission parameters. Each team member cleaned a specific subset of parameters, which were then merged into a unified dataset (with code found in the `Production Code` folder). The final dataset (`merged_data.tsv` within the `data/cleaned data` folder) is a TSV that includes information on launch vehicles, manufacturers, launch sites, mission types, orbits, and launch outcomes, ready for future analysis. The data dictionary <mark>(add where this is located when we have it)</mark> specifies more details about each column in the TSV.

## Distribution & Access

Our dataset is publicly available on GitHub and available for any interested party to download as a TSV, or to recreate themselves using our acquisition and cleaning code.

### Data Source Rights
Our dataset uses the **Launch Library 2 API**, which provides public space launch data for research and educational purposes.

- **Source:** The Space Devs [Launch Library 2 API](https://ll.thespacedevs.com/)
- **License:** Public API with [entire database freely available to all](https://thespacedevs.com/llapi), no documented restrictions for educational use
- **Our work:** Data collection, cleaning, integration, and documentation
- **Attribution:** Dataset credits Launch Library 2 API as source

### How to Use This Dataset

**Load the data:**

Adjust file pathing as appropriate for your workflow; for all code included in this repository, no adjustments to file pathing should be required.

```python
import pandas as pd
df = pd.read_csv('data/cleaned data/merged_data.tsv', sep='\t')
```

**Quick overview:**
```python
print(f"Total launches: {len(df)}")
print(f"Date range: {df['Launch Date'].min()} to {df['Launch Date'].max()}")
print(f"Attributes: {len(df.columns)}")
```

### Dataset Contents

Within `data/cleaned data` folder:

- **merged_data.tsv** - Complete dataset (7,336 launches, 39 attributes)
- **clean_rocket_data.tsv** - Rocket specifications (15 attributes)
- **clean_launch_data.tsv** - Launch details (16 attributes)
- **clean_mission_data.tsv** - Mission parameters (10 attributes)

The data dictionary <mark>(add location/more detail once this is finished)</mark> contains detailed information about each column in `merged_launch_data.tsv`, including data type and units when applicable.

More information, tables, figures, and code to interact with the final dataset are available in `Production Code/03_Merge/ipynb`.

### Dataset Overview

Quick statistics about the collected data:

| Metric | Value |
|--------|-------|
| Total Launches | 7,336 |
| Time Span | 1957-2025 |
| Countries | 47 |
| Unique Rockets | 450+ |
| Total Attributes | 39 |
| File Size | 4.6 MB |

### Reproducing Our Collection
All collection and cleaning code is provided in this repository in the `Production Code` folder (see **Getting Started** for more detailed instructions):
1. Run `01_Acquisition.ipynb` to collect data
2. Run individual cleaning notebooks for each parameter set:
    * `02a_Rocket_Extraction.ipynb` - Extracts rocket parameters
    * `02b_Launch_Extraction.ipynb` - Extracts launch parameters
    * `02c_Mission_Extraction.ipynb` - Extracts mission parameters
4. Run `03_Merge.ipynb` to integrate

**Note:** Full collection takes ~5-6 hours due to API rate limiting (15 requests/hour, with a maximum of 100 launches/request)

### Extending the Dataset
To collect recent launches that may have occured since our last update: 

```python
import requests

# Get 100 latest launches
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
* Google Colab or Jupyter Notebook environment; if using Colab, requires Google Drive account for file storage

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

4. All code should be able to run locally in-place without rearranging directory structure. If running in Google Colab or if a dfifferent directory organization is desired, update code and file pathing as needed.

### Executing Program

The project consists of three main phases:

**Phase 1: Data Collection**
* Open `01_Acquisition.ipynb` in `Production Code` folder
* Set TEST_MODE flag to False for full collection (5-6 hours due to rate limiting)
* Run notebook to collect raw launch data from API
* Note: Space Devs Launch Library 2 API does not require an API key
* Output: `raw_baseline_launches_Group7.json` saved to `data/` folder

**Phase 2: Data Cleaning**
* Open cleaning notebooks in `Production Code` folder:
  * `02a_Rocket_Extraction.ipynb` - Extracts rocket parameters
  * `02b_Launch_Extraction.ipynb` - Extracts launch parameters
  * `02c_Mission_Extraction.ipynb` - Extracts mission parameters
* Run each notebook to generate cleaned parameter files
* Output: Three TSV files (`clean_rocket_data.tsv`, `clean_launch_data.tsv`, `clean_mission_data.tsv`) saved to `data/cleaned data` folder

**Phase 3: Data Merging**
* In `Production Code` folder, run `03_Merge.ipynb` to combine all cleaned data
* Output: `merged_data.tsv` saved to `data/cleaned` folder - Final dataset ready for analysis

### **4. GitHub File Structure:**
```
space-legends-data/
├── Production Code/
│   ├── 01_Acquisition.ipynb
│   ├── 02a_Rocket_Extraction.ipynb
│   ├── 02b_Launch_Extraction.ipynb
│   ├── 02c_Mission_Extraction.ipynb
│   └── 03_Merge.ipynb
├── Project materials/
│   ├── Presentation.pdf
│   ├── Project_Proposal.ipynb
│   └── Data_Dictionary
├── data/
│   ├── cleaned data/
│   │   ├── clean_rocket_data.tsv
│   │   ├── clean_launch_data.tsv
│   │   └── clean_mission_data.tsv
│   ├── raw data/
│   │   └── raw_baseline_launches_Group7.json.zip
│   └── merged_data.tsv
├── testing notebooks/
│   └── [various testing notebooks]
├── .gitignore
├── README.md
└── requirements.txt
```
## Challenges, Limitations, and Alternatives

The final dataset contains nulls in 21 out of 39 columns; these are items that were missing in the original API calls to Launch Library 2. A potential approach that we explored to filling some of these null values was to web scrape for this information from Wikipedia or the [Next Spaceflight](https://nextspaceflight.com/launches/) website. <mark>(add additional information about what we accomplished here, where to find relevant testing notebooks)</mark>

An early limitation we faced in this project was the rate limit of 15 calls/hour from the Launch Library 2 API. We ultimately decided to utilize pagination and a sleep timer to acquire the entire dataset over the span of 5-6 hours, as shown in `01_Acquisition.ipynb`. However, we also considered filtering by time to make the API calls, so that the user could, e.g. acquire all the launches for a single year at once. The code developed for this approach can be found under `Testing Notebooks` in `API call by year - test 1.ipynb` and `API test for 5 years data Interval.ipynb`. <mark>Add anything additional we want to say about filtering/API calls here.</mark>

<mark>Add any additional challenges/limitations here; make sure to revisit what we thought the dataset development would take as compared to the actual work involved and obstacles encountered</mark>

## Help

**Common Issues:**

* **FileNotFoundError**: Update file paths in notebooks to match your directory structure if different than provided
* **API Rate Limiting**: The Space Devs API allows 15 requests/hour. The pagination code includes automatic pausing.
* **Missing Values After Merge**: Normal - not all launches have complete data in the API
* **Google Drive Mount Issues**: Re-run the drive.mount() cell in Colab
* **Google Colab Session Timeout**: Files saved to Colab's temporary storage will be lost after session timeout. Save important files to Google Drive to prevent data loss.
* **Size of JSON**: Size of the file after full collection (of more than 7,000 launches) is more than 341MB. The file will need to be saved in Google Drive or zipped for GitHub. 

For questions about the project, contact team members (see Authors section).

## Authors

DSCI 511 Project Group 7

* [Jillian Kunze](https://github.com/Jmkunze) - jk3987@drexel.edu 
* [Innocent Gumunyu](https://github.com/InnocentGumunyu) - ig384@drexel.edu
* [Ryan Peters](https://github.com/Rybus07) - rap369@drexel.edu
* [Phillip Roman](https://github.com/PhillipJRoman) - pjr322@drexel.edu

## Version History

* 1.0 (November 2025)
    * Initial release - Complete data collection and preprocessing pipeline
    * 7,336 launches collected and cleaned
    * Three-way merge functionality implemented

## License

This project is for educational purposes as part of DSCI 511 coursework at Drexel University.

Data sourced from [The Space Devs Launch Library 2 API](https://thespacedevs.com/llapi).


## Acknowledgments

* [The Space Devs](https://thespacedevs.com/) - Launch Library 2 API
* [Space Devs API Documentation](https://ll.thespacedevs.com/docs/)
* [Stack Overflow pagination example](https://stackoverflow.com/questions/56206038/how-to-loop-through-paginated-api-using-python)
* DSCI 511 course materials and instructor and TAs

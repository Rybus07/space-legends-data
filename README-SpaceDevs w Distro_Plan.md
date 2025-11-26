# Space Launch Data Collection and Processing

Data acquisition and preprocessing pipeline for collecting historical rocket launch data from the Space Devs [Launch Library 2 API](https://thespacedevs.com/llapi), for DSCI 511 group term project at Drexel University.  

## Description

This project aquires and pre-processes comprehensive historical data on rocket launches using the Space Devs Launch Library 2 API. The team extracted over 7,300 launch records spanning from 1957 to the present with code found in the `Data Acquisition` folder, focusing on three main categories of data: rocket specifications, launch information, and mission parameters. Each team member cleaned a specific subset of parameters, which were then merged into a unified dataset (with code found in the `Data Cleaning and Merge` folder). The final dataset <mark>(add where this is located when we have it)</mark> is a TSV that includes information on launch vehicles, manufacturers, launch sites, mission types, orbits, and launch outcomes, ready for future analysis. The data dictionary <mark>(add where this is located when we have it)</mark> specifies more details about each column in the TSV.

## Distribution & Access

Our dataset is publically available on GitHub and available for any interested party to download as a TSV, or to recreate themselves using our acquisition and cleaning code.

### Data Source Rights
Our dataset uses the **Launch Library 2 API**, which provides public space launch data for research and educational purposes.

- **Source:** The Space Devs [Launch Library 2 API](https://ll.thespacedevs.com/)
- **License:** Public API with [entire database freely available to all](https://thespacedevs.com/llapi), no documented restrictions for educational use
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

### Dataset Contents <mark>(add which folder each is stored in)</mark>
- **merged_launch_data.tsv** - Complete dataset <mark>(7,336 launches, 39 attributes) (check this once finalized)</mark>
- **clean_rocket_data.tsv** - Rocket specifications (15 attributes)
- **clean_launch_data.tsv** - Launch details (16 attributes)
- **clean_mission_data.tsv** - Mission parameters (10 attributes)

The data dictionary <mark>(add location/more detail once this is finished)</mark> contains detailed information about each column in `merged_launch_data.tsv`, including data type and units when applicable.

### Dataset Overview <mark>(update once dataset finalized)</mark>

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
All collection and cleaning code is provided in this repository (see **Getting Started** for more detailed instructions):
1. Run `Space_Launch_Acquisition_Pagination.ipynb` to collect data
2. Run individual cleaning notebooks for each parameter set
  * `Rocket_Parameters_Extraction.ipynb` - Extracts rocket parameters
  * `Launch_Parameters_Extraction.ipynb` - Extracts launch parameters
  * `Mission_Parameters_Extraction.ipynb` - Extracts mission parameters
4. Run `Merge_3_Cleaned_DataFrames.ipynb` to integrate

**Note:** Full collection takes ~5-6 hours due to API rate limiting (15 requests/hour, with maximum of 100 launches/request)

### Extending the Dataset
To collect launches since our last update: <mark>(do we want to add something that looks at the date of the last request?)</mark>
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

4. If needed, update file paths in notebooks to match your directory structure <mark>(was specified in class that everything should be able to be run as-is without updating file paths or moving folders, so we should make sure that we set things up that way and note that here)</mark>

### Executing Program

The program consists of three main phases:

**Phase 1: Data Collection**
* Open `Space_Launch_Acquisition_Pagination.ipynb` in `Data Acquisition` folder
* Set TEST_MODE flag to False for full collection (5-6 hours due to rate limiting)
* Run `Space_Launch_Acquisition_Pagination.ipynb` to collect raw launch data from API (note: Space Devs Launch Library 2 API does not require an API Access Key)
* Output: `raw_baseline_launches_Group7.json`

**Phase 2: Data Cleaning**
* Run cleaning notebooks for each data category, located in `Data Cleaning and Merge` folder:
  * `Rocket_Parameters_Extraction.ipynb` - Extracts rocket parameters
  * `Launch_Parameters_Extraction.ipynb` - Extracts launch parameters
  * `Mission_Parameters_Extraction.ipynb` - Extracts mission parameters
* Output: Three TSV files (`clean_rocket_data.tsv`, `clean_launch_data.tsv`, `clean_mission_data.tsv`) <mark>(do we want to also include these in the data extraction folder?)</mark>

**Phase 3: Data Merging**
* In 'Data Cleaning and Merge` folder, run `Merge_3_Cleaned_DataFrames.ipynb` to combine all cleaned data
* Output: `merged_launch_data.tsv` - Final dataset ready for analysis

**Important:** Update file paths in each notebook to match your directory structure before running. <mark>(again, ideally the user should not have to do this - update this text accordingly once we've made this change)</mark>

```

---

### **4. Submission Zip File Structure:**
```
project_submission.zip
├── data/
│   ├── raw_baseline_launches_Group7.json
│   ├── clean_rocket_data.tsv
│   ├── clean_launch_data.tsv
│   ├── clean_mission_data.tsv
│   └── merged_launch_data.tsv
├── notebooks/
│   ├── Space_Launch_Acquisition_Pagination.ipynb
│   ├── Data_extraction_rocket.ipynb
│   ├── DSCI_511_Launch_parameters.ipynb
│   ├── Data_Extraction_Mission_parameters.ipynb
│   └── Merge_3_Cleaned_DataFrames.ipynb
└── README.md

## Challenges, Limitations, and Alternatives

The final dataset contains nulls in <mark>#</mark> out of <mark>#</mark> columns; these are items that were missing in the original API calls to Launch Library 2. A potential approach that we explored to filling some of these null values was to web scrape for this information from Wikipedia or the [Next Spaceflight](https://nextspaceflight.com/launches/) website. <mark>(add additional information about what we accomplished here, where to find relevant notebook)</mark>

An early limitation that we faced in this project was the rate limit of 15 calls/hour from the Launch Library 2 API. We ultimately decided to utilize pagination and a sleep timer to aquire the entire dataset over the span of 5-6 hours, as shown in `Space_Launch_Acquisition_Pagination.ipynb` in the `Data Acquisition` folder. However, we also considered filtering by time to make the API calls, so that the user could e.g. acquire all the launches for a single year at once. The code developed for this approach can be found under `Testing Notebooks` in `API call by year - test 1.ipynb` and `API test for 5 years data Interval.ipynb`. <mark>Add anything additional we want to say about filtering/API calls here.</mark>

<mark>Add any additional challenges/limitations here</mark>

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
    * 7,336 <mark>(check against final)</mark> launches collected and cleaned
    * Three-way merge functionality implemented

## License

This project is for educational purposes as part of DSCI 511 coursework at Drexel University.

Data sourced from [The Space Devs Launch Library 2 API](https://thespacedevs.com/llapi).


## Acknowledgments

* [The Space Devs](https://thespacedevs.com/) - Launch Library 2 API
* [Space Devs API Documentation](https://ll.thespacedevs.com/docs/)
* [Stack Overflow pagination example](https://stackoverflow.com/questions/56206038/how-to-loop-through-paginated-api-using-python)
* DSCI 511 course materials and instructor and TAs

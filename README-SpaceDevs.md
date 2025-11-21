# Space Launch Data Collection and Processing

Data acquisition and preprocessing pipeline for collecting historical rocket launch data from the Space Devs Launch Library 2 API, for DSCI 511 group term project at Drexel University.  

## Description

This project collects and processes comprehensive historical data on rocket launches using the Space Devs Launch Library 2 API. (It should be noted this project does not analyze any data.) The team extracted over 7,300 launch records spanning from 1957 to present, focusing on three main data categories: rocket specifications, launch details, and mission parameters. Each team member cleaned a specific subset of parameters, which were then merged into a unified dataset. The final dataset includes information on launch vehicles, manufacturers, launch sites, mission types, orbits, and launch outcomes, ready for future analysis.

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
* Run `DSCI_511_project_test_notebook.ipynb` to collect raw launch data from API
* Output: `raw_baseline_launches_[collector_name].json`

**Phase 2: Data Cleaning**
* Run cleaning notebooks for each data category:
  * `Data extraction - rocket.ipynb` - Extracts rocket parameters
  * `DSCI_511_Mission_parameters_v1.ipynb` - Extracts mission parameters
  * `DSCI_511_Launch_parameters.ipynb` - Extracts launch parameters (in progress)
* Output: Three TSV files (rocket_data.tsv, launch_data.tsv, clean_mission_data.tsv)

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
# SkillCorner X PySport Analytics Cup
This repository contains the submission template for the SkillCorner X PySport Analytics Cup **Analyst Track**. 
Your submission for the **Analyst Track** should be on the `main` branch of your own fork of this repository.

Find the Analytics Cup [**dataset**](https://github.com/SkillCorner/opendata/tree/master/data) and [**tutorials**](https://github.com/SkillCorner/opendata/tree/master/resources) on the [**SkillCorner Open Data Repository**](https://github.com/SkillCorner/opendata).

## Submitting
Make sure your `main` branch contains:

1. A single Jupyter Notebook in the root of this repository called `submission.ipynb`
    - This Juypter Notebook can not contain more than 2000 words.
    - All other code should also be contained in this repository, but should be imported into the notebook from the `src` folder.


or,


1. A single Python file in the root of this repository called `main.py`
    - This file should not contain more than 2000 words.
    - All other code should also be contained in this repository, but should be imported into the notebook from the `src` folder.

or, 


1. A publicly accessible web app or website written in a language of your choice (e.g. Javascript)

    - Your code should follow a clear and well defined structure.
    - All other code should also be contained in this repository.
    - The URL to the webapp should be included at the bottom of the read me under **URL to Web App / Website**


2. An abstract of maximum 300 words that follows the **Analyst Track Abstract Template**.
3. Add a URL to a screen recording video of maximum 60 seconds that shows your work. Add it under the **Video URL** Section below. (Use YouTube, or any other site to share this video).
4. Submit your GitHub repository on the [Analytics Cup Pretalx page](https://pretalx.pysport.org)

Finally:
- Make sure your GitHub repository does **not** contain big data files. The tracking data should be loaded directly from the [Analytics Cup Data GitHub Repository](https://github.com/SkillCorner/opendata). For more information on how to load the data directly from GitHub please see this [Jupyter Notebook](https://github.com/SkillCorner/opendata/blob/master/resources/getting-started-skc-tracking-kloppy.ipynb).
- Make sure the `submission.ipynb` notebook runs on a clean environment, or
- Provide clear and concise instructions how to run the `main.py` (e.g. `streamlit run main.py`) if applicable in the **Run Instructions** Section below.
- Providing a URL to a publically accessible webapp or website with a running version of your submission is mandatory when choosing to submit in a different language then Python, it is encouraged, but optional when submitting in Python.

_⚠️ Not adhering to these submission rules and the [**Analytics Cup Rules**](https://pysport.org/analytics-cup/rules) may result in a point deduction or disqualification._

---

## Analyst Track Abstract Template (max. 300 words)

#### Introduction
The Player Movement Intelligence Dashboard provides coaches and analysts with an interactive tool to visualize and quantify individual player movement patterns during matches. Using SkillCorner tracking data, this application transforms raw positional data into actionable insights through heat maps, sprint analysis, and performance metrics.

#### Usecase(s)
This tool enables several key use cases:
- **Player Performance Analysis**: Evaluate individual work rate, positioning, and sprint intensity across different match situations
- **Tactical Assessment**: Understand how players utilize space both with and without the ball
- **Comparison & Benchmarking**: Compare movement patterns between players in similar positions
- **Training Feedback**: Provide visual evidence of player movement to support coaching conversations
- **Recruitment**: Assess potential signings through objective movement data

#### Potential Audience
- **First Team Coaches**: Tactical preparation and in-game decision making
- **Performance Analysts**: Detailed post-match analysis and reporting
- **Sports Scientists**: Workload monitoring and physical performance tracking
- **Recruitment Teams**: Objective evaluation of player movement profiles
- **Individual Players**: Self-analysis and performance feedback

---

## Video URL
[YOUR YOUTUBE/LOOM URL HERE]

---

## Run Instructions
```bash
uv sync   # Install dependencies
streamlit run app.py  # Run the Streamlit app
```
The Streamlit app takes its sweet time—2-3 minutes per match. Good thing patience is a skill, right?

---

## [Optional] URL to Web App / Website
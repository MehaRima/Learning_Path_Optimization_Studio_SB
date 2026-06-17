# Learning Path Optimization Studio

## Overview

The **Learning Path Optimization Studio** is a Streamlit-based learning analytics application designed to analyze learner journeys, identify progression patterns, segment learners, and recommend next learning actions.

The core question behind the project is:

> What should a learner do next, based on their current progress and learning pathway?

This project is different from a student performance prediction project. It does not primarily ask whether a learner will fail. Instead, it focuses on learning progression, pathway design, learner segments, and next-step recommendations.

---

## Why This Project Exists

Learning data often contains signals about module completion, engagement, scores, time spent, attempts, and topic exposure. These signals can be used not only to evaluate outcomes but also to support better learning journeys.

This app helps explore:

- which modules attract participation,
- where completion weakens,
- how learner groups differ,
- and which next modules may be useful.

---

## Current Capabilities

### Learner Activity Upload and Demo Data

The app supports:

- CSV upload for learner activity data,
- synthetic demo learner records,
- time-window filtering,
- topic-level focus filtering.

### Learning Path Map

The path map summarizes module participation, average score, and completion behavior.

This helps identify:

- highly active modules,
- low-completion modules,
- difficult modules,
- possible pathway bottlenecks.

### Learner Segmentation

The system uses K-Means clustering to group learners based on:

- modules seen,
- average score,
- completion rate,
- total time.

This helps identify different learning profiles without reducing the project to a simple pass/fail prediction task.

### Recommendation Studio

The recommendation section suggests next modules based on learner progress and pathway position.

The purpose is practical learning support rather than generic prediction.

### Intervention Notes

The app identifies learners with low engagement signals and provides practical intervention ideas.

---

## Design Choice

This project intentionally emphasizes **learning pathway optimization** rather than academic risk prediction.

That design choice makes the project distinct from traditional student performance prediction. The focus is on journey design, learner progression, and recommended next actions.

---

## Technology Stack

- Python
- Streamlit
- Pandas
- Plotly
- Scikit-Learn
- K-Means Clustering
- StandardScaler

---

## Example Use Cases

- Learning pathway analysis
- Guided project sequencing
- Learner support planning
- Module-level learning analytics
- Course progression review
- Adaptive learning prototype design

---

## Recommended Dataset Columns

The app works best with fields similar to:

- learner ID
- activity date
- module
- topic
- score
- completion status
- time spent
- attempts

Synthetic demo data is included so the project can be explored even without an external dataset.

---

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Future Enhancements

Possible improvements include:

- collaborative filtering,
- sequence-aware recommendation logic,
- learner pathway graphs,
- prerequisite mapping,
- adaptive intervention rules,
- module similarity scores,
- learning outcome alignment.

---

## Project fit

This project demonstrates how analytics can move beyond prediction and support a more useful question:

> What learning action should come next?

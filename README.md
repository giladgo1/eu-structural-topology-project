# European Strategy Atlas

An interactive learning tool for exploring how European countries achieve success through different structural pathways.

## Live Application

https://eu-strategy-atlas.streamlit.app

---

## Project Overview

European Strategy Atlas was developed as a Data Analytics Capstone Project to help non-experts explore complex public-policy and economic systems through data.

The goal is not to rank countries or identify a single "best" model. Instead, the Atlas helps users understand how different countries balance competing priorities, navigate tradeoffs, and follow different pathways toward similar outcomes.

The application transforms public European datasets into an interactive learning journey where users can:

* Explore structural strengths and constraints
* Compare countries in context
* Investigate tradeoffs between strategic dimensions
* Test alternative investment strategies
* Examine resilience under disruption
* Learn how different pathways shape outcomes

A central idea of the project is that countries can achieve success through different mechanisms. Similar outcomes do not necessarily imply similar strategies, and rankings alone rarely explain how change occurs.

The Atlas was designed as an educational tool for systems thinking, strategic exploration, and evidence-based learning.

---

## Core Questions

The project is built around five questions:

1. Where is a country today?
2. How did it get there?
3. What tradeoffs shape its outcomes?
4. Which strategic choices are available?
5. How resilient is the system under disruption?

---

## Learning Journey

The application guides users through a structured learning process:

### P0 — Landing

Introduction to the Atlas, its purpose, and the exploration journey.

### P1 — Country Explorer

Understand a country's structural position, strengths, constraints, evolution, and investment profile.

### P2 — Tradeoff Explorer

Investigate relationships, tensions, and tradeoffs between strategic dimensions.

### P3 — Strategic Choices

Build and test alternative investment strategies and observe their structural consequences.

### P4 — Challenge Mode

Evaluate resilience under external disruptions such as crises and shocks.

### P5 — Reflection

Summarize key lessons and learning outcomes from the exploration journey.

### P6 — How It Was Made

Explore the methodology, assumptions, data sources, validation process, and application architecture.

---

## Dataset

### Coverage

* 27 European Union countries
* 2014–2025
* 19 public indicators
* Multiple normalization approaches
* Structural and dynamic analysis layers

### Source

* Eurostat


### Example Indicators

* Education
* Education Spending
* Research & Development
* ICT Specialists
* Renewable Energy
* Environmental Spending
* Emissions
* Social Protection
* Health Spending
* Defense Spending
* Public Debt
* Unemployment
* Income Inequality

---

## Methodology

The project translates individual indicators into seven structural dimensions:

* Human Capital
* Innovation Capacity
* Sustainability Capacity
* Social Cohesion
* Fiscal Flexibility
* Security Reprioritization
* Adaptive Transformation

Countries are evaluated using normalized EU-relative indicators and analyzed through multiple perspectives including:

* Structural position
* Dynamic evolution
* Tradeoff relationships
* Strategic pathways
* Resilience under disruption

Countries are also grouped into structural families that help provide context for interpretation.

---

## Key Insights

* Different countries achieve success through different pathways.
* Rankings explain where countries are, not how they got there.
* Structural context changes the interpretation of performance.
* Similar outcomes can emerge from different mechanisms.
* Families help explain where countries are.
* Pathways help explain how countries change.
* Static position and dynamic transformation are not the same thing.
* Tradeoffs are often context-dependent rather than universally good or bad.

---

## Technology

* Python
* Pandas
* NumPy
* Plotly
* Streamlit
* Git
* GitHub
* Streamlit Community Cloud

---

## Repository Structure

```text
data/
notebooks/
streamlit_app/
docs/
reports/
```

---

## Local Installation

```bash
git clone https://github.com/giladgo1/eu-structural-topology-project.git

cd eu-structural-topology-project

pip install -r requirements.txt

streamlit run streamlit_app/streamlit_app.py
```

---

## Disclaimer

European Strategy Atlas is an educational and exploratory project developed as a Data Analytics Capstone Project.

The application is designed to support learning, exploration, and discussion. It does not provide policy recommendations, forecasts, investment advice, or causal claims.

All analyses are based on publicly available data and should be interpreted as exploratory rather than prescriptive.

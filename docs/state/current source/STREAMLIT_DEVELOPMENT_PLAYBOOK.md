# STREAMLIT DEVELOPMENT PLAYBOOK

## Derived From P1 Country Explorer Development

### Purpose

This document captures the lessons learned, workflow improvements, design rules, architecture patterns, and implementation strategy discovered during the development of Page 1.

The goal is:

```text
Build P2–P5 significantly faster and with less rework than P1.
```

This document becomes the implementation reference for all future Streamlit pages.

---

# Core Principle

The objective is NOT:

```text
Build pages.
```

The objective is:

```text
Build a reusable exploration framework.
```

P1 was the prototype.

Future pages should reuse:

* architecture patterns
* typography
* navigation
* component structure
* card systems
* styling conventions
* development workflow

rather than rebuilding them.

---

# Most Important Discovery

P1 was slow because development often followed:

```text
Content
↓
Layout
↓
CSS
↓
Layout Fixes
↓
Architecture Fixes
```

Future pages should follow:

```text
Architecture
↓
Frame
↓
Typography
↓
Reusable Components
↓
Content
↓
Data
↓
Polish
```

---

# P1 Lessons Learned

## Architecture First

Always validate:

```text
Architecture
↓
Feature Coverage
↓
User Journey
↓
Visual Design
↓
Polish
```

Never reverse this order.

---

## Full Block Replacement Rule

When changing:

* columns
* layouts
* nested containers
* Streamlit sections

use:

```text
Full Section Replacement
```

Never provide insertion fragments.

This avoids:

* indentation errors
* misplaced content
* layout corruption

---

## Compress Whitespace, Not Learning

Reduce:

* spacing
* card height
* redundant visual elements

Never remove:

* interpretation
* educational guidance
* context
* exploration prompts

---

## Screenshot-Driven Review

Most successful improvements followed:

```text
Screenshot
↓
Critique
↓
Redesign
↓
Implement
```

rather than:

```text
Code
↓
Guess
↓
Patch
```

Always review visually before redesigning.

---

## Build Frame First

One of the most important discoveries.

Future pages should be developed in the following order:

### Phase 1

Build:

```text
Header
Navigation
Main Content Area
Mission Area
Footer
```

with placeholder boxes only.

No charts.

No data.

No styling refinement.

---

### Phase 2

Add:

```text
Section Titles
Section Containers
Card Containers
```

Still no data.

---

### Phase 3

Add:

```text
Charts
Cards
Interactions
```

---

### Phase 4

Add:

```text
Real Data
```

---

### Phase 5

Apply:

```text
Polish
```

This approach should eliminate most layout drift and scrolling issues.

---

# P1 Readability Review

## Main Findings

### Headers Too Light

Current light-grey headers are difficult to read.

Rule:

```text
Section Titles
= White

Card Titles
= Near White

Labels
= Grey
```

---

### Body Text Too Small

Many cards require zooming.

Rule:

Increase body text globally.

Never fix readability card-by-card.

---

### Graph Readability Insufficient

Users must immediately understand:

```text
What is being shown?
What is the baseline?
What are the units?
```

without reading documentation.

---

# Graph Standards

## Radar Charts

Always show:

```text
Relative to EU Average
(EU = 0)
```

Users should never need to infer the baseline.

---

## Units

Every graph must explicitly state:

```text
Dimension Index

EU Relative Score

Percent

Z-Score
```

or equivalent.

No hidden units.

---

## Evolution Charts

Required:

* yearly grid
* larger labels
* larger axis text
* visible units

---

## Legends

Avoid separate legend boxes.

Preferred:

```text
Germany
```

shown in Germany color.

```text
EU Average
```

shown in EU color.

Cleaner and more compact.

---

# Information Architecture Standards

## Number Investigation Questions

Use:

```text
Question 1

Question 2

Question 3
```

Creates exploration flow.

---

## Number Insights

Use:

```text
Insight 1

Insight 2

Insight 3
```

Creates learning progression.

---

## Use Bullets

Avoid large paragraphs.

Preferred:

```text
Key Insights

• Observation
• Observation
• Observation
```

and:

```text
Next Exploration

• Option A
• Option B
• Option C
```

---

# Color Semantics

Use consistent meaning.

## Positive

```text
Green
```

Used for:

* strengths
* advantages

---

## Caution

```text
Amber
```

Used for:

* constraints
* tradeoffs

---

## Risk

```text
Red
```

Used for:

* vulnerabilities
* warning indicators

---

## Neutral

```text
Blue / Grey
```

Used for:

* informational content
* references

---

# Vocabulary Standards

Use consistent terminology.

Preferred:

```text
Advantage
Constraint
```

Avoid mixing:

```text
Weakness
Gap
Challenge
Risk
```

unless meaningfully different.

---

# Navigation System

## Future Navigation Panel

Navigation should answer:

```text
Where am I in the application?
```

and:

```text
Where am I on this page?
```

Example:

```text
Application

P1 Explorer ✓
P2 Investigator ○
P3 Strategist ○
P4 Challenger ○
P5 Reflector ○
```

and:

```text
Current Page

01 Question ✓
02 Evidence ●
03 Interpretation ○
04 Insight ○
05 Next Step ○
```

---

# Mission Log

## Discovery

Current Mission Log is not a true log.

It behaves more like:

```text
Status Panel
```

than:

```text
Journey Memory
```

---

## MVP Direction

Keep:

```text
Current Context
Current Insight
Next Step
```

visible.

---

## Future Direction

Mission Log should evolve into:

```text
Cross-Page Memory
```

tracking:

```text
Country Selected
Tradeoff Explored
Mission Selected
Challenge Tested
Insights Generated
```

throughout the journey.

---

## Recommended Structure

Right-side memory panel:

```text
Current Country
Current Mission
Latest Insight
Recommended Next Step
```

Expandable drawer:

```text
Full Journey History
```

---

# Shared Components

## Extract

```text
atlas_header.py

atlas_footer.py

page_frame.py

navigation_panel.py

mission_log.py

cards.py

typography.py
```

---

## Do Not Extract Yet

These remain page-specific:

```text
KPI Ribbon

Snapshot Ribbon

Radar Layout

Comparison Layout
```

---

# Future Page Build Workflow

For every page:

## Step 1

Build frame only.

Screenshot.

Review.

---

## Step 2

Build sections only.

Screenshot.

Review.

---

## Step 3

Add charts.

Screenshot.

Review.

---

## Step 4

Add data.

Screenshot.

Review.

---

## Step 5

Apply polish.

---

# P1 Stabilization Wave

Before P2:

## Pass 1

Typography

---

## Pass 2

Graph Readability

---

## Pass 3

Color Consistency

---

## Pass 4

Information Density

---

## Pass 5

Footer Redesign

---

## Pass 6

Navigation & Mission Log Review

---

# Success Metric

The purpose of this playbook is measurable:

```text
P2 development time
<
50% of P1 development time
```

If P2 requires similar effort to P1, then the lessons from P1 were not successfully captured.

The objective is not simply to finish the application.

The objective is to create a reusable exploration framework that accelerates all future pages.

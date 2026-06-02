# 08_EXPLORATION_ATLAS_DESIGN_SYSTEM_V2.md

# European Strategy Atlas — Exploration Architecture V2

## Purpose

This document supersedes the dashboard-oriented visual grammar defined in:

```text
07_visual_grammar_and_design_system.md
```

The purpose of V2 is to document the evolution of the application into a:

```text
Guided Exploration Atlas
```

rather than a traditional dashboard.

This document becomes the active design reference for future mockups and Streamlit implementation.

---

# Core Philosophy

The application is:

```text
European Strategy Atlas
+
Guided Exploration
+
Captain's Log
```

The application is NOT:

```text
Business Dashboard
```

The application is NOT:

```text
Policy Simulator
```

The application is NOT:

```text
Video Game
```

The goal is educational exploration.

Users should feel:

```text
Curiosity
Discovery
Learning
Experimentation
Reflection
```

throughout the journey.

---

# User Journey Model

The entire application follows:

```text
Question
↓
Evidence
↓
Observation
↓
Interpretation
↓
Next Question
```

This pattern should appear repeatedly across all pages.

---

# Global UX Principles

## Principle 1 — Context Is Always Visible

Users should never ask:

```text
Where am I?
```

Every page contains a sticky context ribbon.

---

## Sticky Context Ribbon

Always visible.

Contains:

```text
Country
Reference
Family
Archetype
Current Mission
```

Examples:

```text
Germany

Innovation Core Family

Industrial Innovation Core

Reference:
Family Average

Mission:
Green Transition
```

---

## Principle 2 — Learning Is Always Visible

Users should never ask:

```text
What did I already learn?
```

---

# Mission Log

Persistent exploration notebook.

Contains:

```text
Investigations
Strategies
Challenges
Insights
Suggested Next Steps
```

Mission Log evolves throughout the journey.

Mission Log becomes the foundation of Page 5.

---

## Principle 3 — Navigation Is Always Visible

Users should never ask:

```text
Where am I in the journey?
```

---

# Section Navigator

Persistent left-side journey map.

Uses:

```text
✓ Completed

● Current

○ Upcoming
```

Current section updates automatically based on scroll position.

---

# Principle 4 — Scroll-Based Discovery

The application is NOT a dashboard.

The application is a guided exploration experience.

Each page is divided into sequential exploration sections.

Users learn by progressing through sections.

---

# Principle 5 — One Cognitive Question Per Section

Every major section should answer ONE question.

Examples:

Page 1:

```text
Who is Germany?
```

Page 2:

```text
What pattern appears?
```

Page 3:

```text
What future would you pursue?
```

Page 4:

```text
Can your strategy survive disruption?
```

Page 5:

```text
What did I learn?
```

Avoid mixing multiple major questions into a single section.

---

# Principle 6 — Every Section Ends With Direction

Every major section must end with:

```text
What did I learn?
```

and

```text
What should I explore next?
```

This is a core navigation mechanism.

The user should be continuously pulled forward.

---

# Principle 7 — Input And Output Stay Together

Never separate:

```text
User Input
```

from:

```text
Observed Result
```

by more than one section.

Examples:

Page 3:

```text
Mission Selection
↓
Sliders
↓
Impact
↓
AI Interpretation
```

Page 4:

```text
Challenge
↓
Response Sliders
↓
Impact
↓
Resilience
```

---

# Principle 8 — AI Has A Defined Role

AI summaries should never appear randomly.

Every AI card follows:

```text
Observation
↓
Interpretation
↓
Suggested Direction
```

AI helps explain.

AI does not replace exploration.

---

# Page Roles

## Page 1

```text
Explorer
```

User learns:

```text
Who is this country?
```

---

## Page 2

```text
Investigator
```

User learns:

```text
Why does this pattern exist?
```

---

## Page 3

```text
Strategic Decision Maker
```

User learns:

```text
What future would I pursue?
```

---

## Page 4

```text
Crisis Manager
```

User learns:

```text
Can this strategy survive disruption?
```

---

## Page 5

```text
Reflective Learner
```

User learns:

```text
What did I discover?
```

---

# Page 1 — Country Explorer

Required Features:

```text
Country Selector
Reference Selector
Absolute / Relative Toggle
Country Snapshot Ribbon
Archetype Card
Family Card
Hero Evolution Chart
Country Comparison
AI Summary
Mission Log
Section Navigator
Next Exploration Cards
```

---

# Page 2 — Structural Investigation

Required Features:

```text
Curated Tradeoff Cards
Advanced Relationship Dropdown
Hero Scatter Plot
Country Highlight
Trajectory Overlay
Family Overlay
Evidence Levels
Interesting Exceptions
Family Behaviour
AI Summary
Mission Log
Section Navigator
Next Exploration Cards
```

Rule:

```text
One Hero Chart
```

All other elements support understanding that chart.

---

# Page 3 — Strategic Decision Room

Required Features:

```text
Strategic Tensions
Mission Selection
Priority Sliders
Country Marker
Reference Marker
Strategy Marker
Total = 100%
Impact Cards
AI Summary
Mission Log
Challenge Teaser
```

Flow:

```text
Understand Tensions
↓
Choose Mission
↓
Adjust Priorities
↓
Observe Consequences
↓
Interpret
↓
Challenge
```

Important:

User builds ONE strategy.

User does NOT compare prebuilt strategies.

---

# Page 4 — Challenge & Adaptation

Required Features:

```text
Challenge Selection
Scenario Briefing
Challenge Signals
Response Sliders
Before / After / Delta
Resilience Assessment
Main Strength
Main Vulnerability
Adaptation Actions
Return To Strategy Editor
AI Summary
Strategy Timeline
Mission Log
Suggested Next Exploration
Educational Disclaimer
Reflection Handoff
```

Flow:

```text
Choose Challenge
↓
Understand Scenario
↓
Test Response
↓
Observe Impact
↓
Assess Resilience
↓
Learn
↓
Reflect
```

---

# Page 5 — Reflect & Learn

Required Features:

```text
Journey Timeline
Mission Log Summary
Key Learnings
Patterns & Insights
AI Reflection Summary
Suggested Exploration
Export Options
Restart Options
Educational Disclaimer
```

Purpose:

```text
Mission Debrief
```

not:

```text
Final Dashboard
```

---

# Design Governance Rules

## Architecture Before Visuals

Visual design must NEVER override approved architecture.

Validation order:

```text
1. Architecture

2. Feature Coverage

3. User Journey

4. Visual Design
```

---

## Feature Preservation Rule

Approved features must not disappear during visual iteration.

Any removed feature requires explicit discussion.

---

## Retro Lesson

One of the primary lessons from the capstone design process:

```text
Architecture-first constraints must be enforced before visual generation.

Visual quality must not be evaluated before feature completeness is verified.
```

---

# Current Status

```text
P0 LOCKED

P1 LOCKED

P2 LOCKED

P3 LOCKED (Architecture)

P4 LOCKED

P5 LOCKED
```

Future visual iterations must be validated against this document before approval.

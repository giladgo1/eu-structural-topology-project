# WORKFLOW RETRO & COLLABORATION GUIDE

## Architecture Freeze Retrospective — May 2026

---

# Purpose

This document captures workflow lessons, collaboration principles, continuity risks, and process improvements discovered during the architecture freeze phase of the capstone project.

The goal is to prevent:

* architecture drift
* context loss
* repeated discussions
* documentation gaps
* AI-generated scope expansion
* project reconstruction failures

This document focuses on:

```text
How we work
```

rather than:

```text
What we build
```

---

# Preferred Working Style

The project works best under the following workflow:

```text
PLAN
↓
DISCUSS
↓
MARKDOWN
↓
DEVIL'S ADVOCATE
↓
APPROVE
↓
IMPLEMENT
↓
VALIDATE
↓
DOCUMENT
↓
GIT CHECKPOINT
```

The following practices consistently improved outcomes:

* one step at a time
* markdown before implementation
* architecture before code
* review before freeze
* explicit approvals
* iterative refinement
* documentation before moving forward

---

# What Worked Well

## Architecture Before Implementation

Freezing architecture before coding significantly reduced rework.

---

## Registry-Driven Design

Moving logic into registries improved:

* transparency
* maintainability
* explainability
* future extensibility

---

## Devil's Advocate Reviews

Critical reviews frequently revealed:

* hidden assumptions
* scope creep
* weak evidence
* over-engineering risks

---

## Git Checkpoints

Architecture freezes combined with Git commits provided reliable recovery points.

---

## State File Reconstruction

The creation of authoritative state documents dramatically improved continuity.

---

## Dashboard Separation

Separating:

```text
Observe
```

from:

```text
Experiment
```

simplified architecture and improved educational clarity.

---

# Major Workflow Failures

## WF-01 — Architecture Evolved Faster Than Documentation

Architecture decisions were often finalized before supporting resources were updated.

Result:

* outdated masterplan
* incomplete state files
* missing assumptions

Lesson:

Every architecture freeze must trigger documentation updates.

---

## WF-02 — Decisions Remained Inside Chats

Many important decisions were discussed but never exported.

Result:

* repeated discussions
* duplicated work
* uncertainty about approved decisions

Lesson:

Major decisions must be documented.

---

## WF-03 — Chat Handover Felt Like Restarting The Project

New chats frequently behaved as if no previous work existed.

Result:

* repeated explanations
* repeated architecture debates
* loss of momentum
* user frustration

Root Cause:

Project knowledge existed primarily inside conversations rather than authoritative resources.

Lesson:

Future chats should reconstruct from project resources before proposing changes.

---

## WF-04 — AI Forgot Frozen Plans

Previously approved architecture was sometimes ignored or replaced by newly generated alternatives.

Examples:

* dashboard redesigns after freeze
* reintroduction of rejected features
* alternative structures replacing approved ones

Lesson:

Frozen decisions are constraints.

They are not suggestions.

---

## WF-05 — Mockups Before Architecture

Visual design was generated before architecture stabilization.

Result:

* incorrect feature coverage
* missing MVP requirements
* wasted effort

Lesson:

Architecture freeze before visual generation.

---

## WF-06 — Complexity Expanded Faster Than Evidence

The project repeatedly drifted toward larger systems than the available evidence could support.

Examples:

* recursive ecosystems
* simulation layers
* recommendation engines
* forecasting concepts

Lesson:

Evidence before complexity.

---

## WF-07 — Repeated Reinvention

Several concepts were redesigned multiple times despite acceptable existing solutions.

Examples:

* outputs
* resilience definitions
* family logic
* dashboard roles

Lesson:

Clearly separate:

* open questions
* frozen decisions

---

## WF-08 — State Resources Became Unsynchronized

Masterplan, notebooks, state files, and conversations evolved independently.

Result:

No single source accurately reflected project reality.

Lesson:

Project State becomes the operational source of truth.

---

## WF-09 — Solution Generation Before Problem Validation

Solutions were sometimes proposed before validating that a real problem existed.

Lesson:

```text
Problem
↓
Evidence
↓
Decision
↓
Solution
```

not:

```text
Solution
↓
Justification
```

---

## WF-10 — Resource Discovery Became Difficult

Important information became scattered across:

* chats
* notebooks
* markdown files
* Word documents
* Git history

Lesson:

Maintain a small number of authoritative documents.

---

# Architecture Lessons

## AL-01

```text
Static Position
≠
Dynamic Capability
```

One of the most important conceptual discoveries.

---

## AL-02

Structural families often explain more variation than archetypes alone.

---

## AL-03

Tradeoffs are frequently weaker and more context-dependent than initially expected.

---

## AL-04

Current spending does not necessarily reflect current capacity.

Historical investment, lag effects, and structural inertia matter.

---

## AL-05

Family context significantly influences observed relationships.

---

## AL-06

Educational value often increases when complexity is reduced.

---

# AI Collaboration Lessons

AI performs best when:

* architecture is frozen
* constraints are explicit
* assumptions are documented
* priorities are known

AI performs poorly when:

* scope is ambiguous
* resources are outdated
* frozen decisions are unavailable
* architecture boundaries are unclear

---

# Required Safeguards

To reduce continuity failures:

* state files
* assumptions notebooks
* feature matrices
* Git checkpoints
* architecture freezes
* retrospective reviews

should be maintained throughout the project.

---

# Documentation Rules

After every major architecture decision update:

* MASTER_PROJECT_STATE
* MASTERPLAN ADDENDUM
* ASSUMPTIONS NOTEBOOK
* FEATURE PRIORITY MATRIX

before implementation continues.

---

# Git Rules

Create checkpoints after:

* Architecture Freeze
* Dashboard Freeze
* Sandbox Freeze
* Registry Freeze
* MVP Freeze

---

# Chat Handover Rules

Future chats should reconstruct the project in the following order:

1. MASTER_PROJECT_STATE
2. MASTERPLAN + Addendum
3. ASSUMPTIONS NOTEBOOK
4. FEATURE_PRIORITY_MATRIX
5. Current Notebook Status

Only then should implementation continue.

# HANDOVER GENERATION INSTRUCTIONS

When the user asks:

```text
Prepare handover
Create next chat prompt
Export current state
Continue in new chat
```

the assistant should NOT simply summarize the current conversation.

The assistant should generate a structured handover package.

---

## Required Handover Structure

### 1. Current Status

Summarize:

* current phase
* completed work
* frozen decisions
* current notebook
* current architecture status

---

### 2. Immediate Next Task

Clearly state:

```text
What should happen next.
```

Avoid generic recommendations.

State the exact next approved task.

---

### 3. Required Resources

List resources the new chat should read.

Examples:

* MASTER_PROJECT_STATE
* MASTERPLAN + Addendum
* ASSUMPTIONS_NOTEBOOK
* WORKFLOW_RETRO
* FEATURE_PRIORITY_MATRIX

Only include resources relevant to the next task.

---

### 4. Required Uploads

Explicitly request any files needed before continuing.

Examples:

```text
Please upload:

country_structural_summary_v2_dimensions.csv

structural_family_metadata.csv

sandbox_response_matrix_v1.csv
```

The assistant should identify missing resources rather than assuming availability.

---

### 5. Frozen Decisions

List architecture elements that should not be reopened.

Examples:

* dashboard separation
* family framework
* output framework
* sandbox architecture
* MVP scope

---

### 6. Open Questions

List only unresolved issues.

Do NOT reopen resolved decisions.

---

### 7. User Workflow Preferences

Always remind the new chat:

* one step at a time
* markdown before implementation
* wait for approval
* devil's advocate before freeze
* architecture before visuals
* evidence before complexity

---

### 8. Reconstruction Verification

The new chat should begin by:

1. confirming reconstruction,
2. summarizing current understanding,
3. identifying the next task,
4. asking for missing resources,
5. waiting for approval.

The new chat should NOT immediately start proposing architecture changes.

---

## Handover Quality Rule

A handover is successful if the new chat can continue productive work within 5 minutes without repeating architecture discussions or requiring project re-explanation.

If the handover would require the user to re-explain the project, the handover is incomplete.

---

# Reconstruction Rule

No single resource contains the entire project.

Accurate reconstruction requires:

```text
MASTERPLAN
+
PROJECT STATE
+
ASSUMPTIONS NOTEBOOK
+
FEATURE PRIORITY MATRIX
+
CURRENT NOTEBOOK STATUS
```

---

# Final Principle

The biggest risk to the project was not technical failure.

The biggest risks were:

* architecture drift
* context loss
* repeated discussions
* forgotten decisions
* continuity failures

Future work should prioritize decision preservation and continuity before introducing additional functionality.

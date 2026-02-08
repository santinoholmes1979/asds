\# Aircraft Sustainment Decision Support (ASDS)



\*\*Explainable AI for aircraft readiness, downtime prediction, and sustainment decision-making\*\*



---



\## Executive Summary



ASDS is an \*\*offline-first, explainable AI decision-support system\*\* that predicts near-term aircraft downtime and translates those predictions into \*\*actionable readiness briefs\*\* for commanders and sustainment leaders.



Rather than predicting failures in isolation, ASDS forecasts \*\*14-day aircraft downtime (hours)\*\* and explains the operational and logistics drivers behind that risk using \*\*SHAP-based explainability\*\*.



The system is designed to operate in \*\*disconnected or classified environments\*\*, with cloud-based GenAI as an optional narrative layer—not a dependency.



---



\## What Problem This Solves



Traditional predictive maintenance answers:

> \*“Will a component fail?”\*



ASDS answers:

> \*\*“How much readiness risk exists, why does it exist, and what should leadership do about it?”\*\*



This reframes maintenance analytics into \*\*operational decision support\*\*.



---



\## Core Capabilities



\### 🔹 Predictive Downtime Modeling

\- Predicts \*\*next 14-day aircraft downtime (hours)\*\*

\- Regression model (LightGBM)

\- Compares operational-only vs. logistics-augmented models

\- Selects best model empirically



\### 🔹 Explainability by Design

\- Every prediction is locally explainable via \*\*SHAP\*\*

\- Identifies which factors increased or reduced downtime

\- Enables auditability and human trust



\### 🔹 Decision-Ready Outputs

\- \*\*Aircraft-level briefs\*\*

&nbsp; - Predicted downtime

&nbsp; - Risk level (LOW / MODERATE / ELEVATED)

&nbsp; - Top contributing drivers (± hours)

\- \*\*Fleet-level rollup\*\*

&nbsp; - Stoplight executive summary (GREEN / AMBER / RED)

&nbsp; - Top-risk aircraft

&nbsp; - Base-level readiness aggregation

&nbsp; - Rule-based recommended actions



---



\## System Architecture






# ASDS – AI Sustainment Decision Support System

ASDS is an AI-enabled decision-support platform that models how aerospace and defense organizations use data to predict system failures, prioritize maintenance, and optimize mission readiness.

The system uses machine learning to forecast aircraft downtime, applies explainable AI (SHAP) to justify predictions, and produces decision-ready outputs for operators and leadership.

ASDS demonstrates how raw operational data can be transformed into mission-relevant insights that support sustainment planning and readiness decisions in constrained or disconnected environments.

ASDS demonstrates how raw operational data can be transformed into mission-relevant insights that support sustainment planning and readiness decisions in constrained or disconnected environments.

ASDS models how AI systems can support sustainment operations by transforming telemetry and model outputs into decision-ready insights for operators and leadership.


---


## What This System Does

- Predicts aircraft/component downtime using machine learning models
- Estimates short-term mission readiness across a simulated fleet
- Provides explainable AI outputs (SHAP) to justify predictions
- Generates decision-ready insights for maintenance prioritization
- Simulates operational use in disconnected or resource-constrained environments


---


## Why This Matters

Modern defense systems require data-driven decision-making to maintain operational readiness.

ASDS demonstrates how AI can be used to:

- Anticipate failures before they impact operations
- Improve sustainment efficiency
- Support mission readiness planning
- Provide explainable insights to human decision-makers

This approach aligns with real-world aerospace and defense challenges, where system availability directly impacts operational availability and mission effectiveness.


---


## Key Features

- AI-driven aircraft downtime prediction  
- Fleet-level mission readiness estimation  
- Explainable AI using SHAP for transparent decision-making  
- Generation of mission-oriented maintenance briefs  
- Designed for use in constrained or disconnected environments  

---


## System Architecture

1. Data Ingestion  
   Simulated aircraft operational and maintenance data

2. Feature Engineering  
   Aggregation of usage patterns, failure indicators, and system stress metrics

3. Machine Learning Model  
   Predicts likelihood of downtime within a defined time horizon

4. Explainability Layer  
   SHAP-based analysis to identify key drivers of predicted failures

5. Decision Support Output  
   Fleet readiness summaries and recommended maintenance actions


---


## Platform Screenshots

### AI-Generated Mission Brief (Elevated Risk)
![Mission Brief Elevated](asds/screenshots/mission_brief_elevated_risk.png)

This output demonstrates how ASDS translates model predictions and SHAP-based explainability into mission-relevant insights, highlighting elevated risk conditions and key operational drivers.

---

### Explainable AI (SHAP Attribution)
![SHAP Analysis](asds/screenshots/shap_explainability.png)

ASDS incorporates explainable AI to identify the primary factors driving predicted downtime, enabling transparent and defensible decision-making.

---

### AI-Generated Mission Brief (Low Risk Scenario)
![Mission Brief Low](asds/screenshots/mission_brief_low_risk.png)

The system captures variability across operating conditions, providing context-aware outputs that reflect both elevated and reduced risk scenarios across the fleet.
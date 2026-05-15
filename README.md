EngineFlow AI — Engineering Workflow & Resource Optimization System
An AI-powered engineering management platform built to improve developer productivity, task allocation efficiency, and project visibility for software teams.

What This System Does
This platform solves key challenges in modern software development:

Lack of structured workflows when using AI
Poor visibility into developer productivity and code quality
Inefficient task allocation across team members
Inability to measure how effectively AI is being used


Features
1. SDLC Workflow Engine
Structured phases: Planning → Development → Testing → Feedback. Tasks are tracked across each stage with real time visibility.
2. Smart Task Allocation Engine
Automatically assigns tasks to the best developer based on:

Current workload (25%)
Past performance score (25%)
Efficiency score (20%)
Skill compatibility (20%)
AI efficiency via commit activity (10%)

3. AI Task Breakdown
Uses Groq LLM (Llama 3) to break high level tasks into actionable subtasks. Every AI interaction is logged with effectiveness scores.
4. Developer Analytics
Tracks per developer:

Workload and performance scores
Efficiency ratings
Commits and sessions
Code quality and test coverage
Average task completion time

5. Management Dashboard
Real time dashboard showing:

Project progress
Team productivity
Resource utilization
Risk and bottleneck detection
AI contribution metrics


Tech Stack
LayerTechnologyFrontendStreamlitBackendPythonDatabaseSQLite via SQLAlchemyAIGroq API (Llama 3.3 70B)ChartsPlotlyDataPandas

Database Schema
Four tables:

developers — stores team members with skills, workload, performance, commits, sessions
tasks — stores all tasks with status, stage, time tracking, code quality, test coverage
ai_logs — logs every AI interaction with prompt, response, and effectiveness score
projects — tracks project level progress and status


AI Integration Strategy
AI is used as a collaborative tool at every stage of the SDLC:
StageAI RolePlanningBreaks down high level requirements into subtasksDevelopmentAllocation engine uses AI efficiency scores to assign tasksTestingTracks test coverage and code quality per developerFeedbackLogs and analyzes all AI interactions for effectiveness
The system uses the Groq API with the Llama 3.3 70B model for fast, free, and accurate task breakdown. Every prompt and response is stored in the ai_logs table for full auditability.

How To Run

Clone the repository: git clone https://github.com/aryanms2003/engineering-workflow-ai.git
Install dependencies: pip install -r requirements.txt
Create a .env file and add: GROQ_API_KEY=your_groq_api_key_here
Seed the database: python seed_data.py
Run the app: streamlit run app.py


Sample Dataset
The system comes with pre-loaded sample data:

15 developers with varied skills, workloads, and performance scores
30 tasks across all SDLC stages
5 active projects with progress tracking


Project Structure

app.py — Main Streamlit application
database.py — Database setup and table creation
allocation.py — Task allocation scoring algorithm
ai_helper.py — Groq AI API integration
seed_data.py — Sample dataset generator
requirements.txt — Python dependencies


Developed By
Aryan Manish Singh

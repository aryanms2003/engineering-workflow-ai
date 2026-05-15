import pandas as pd
from sqlalchemy import text
from database import engine

def get_best_developer(task_skills_required):
    """
    Scores each developer based on:
    - Workload (lower is better)        → 30% weight
    - Performance score (higher better) → 30% weight
    - Efficiency score (higher better)  → 20% weight
    - Skill match                       → 20% weight
    """
    with engine.connect() as conn:
        devs = pd.read_sql("SELECT * FROM developers", conn)

    scores = []
    for _, dev in devs.iterrows():
        dev_skills = dev['skills'].split(',')
        required   = task_skills_required.split(',')

        # Skill match score (0 to 1)
        match = len(set(dev_skills) & set(required)) / max(len(required), 1)

        # Workload score — lower workload = higher score
        workload_score = (100 - dev['workload']) / 100

        # Performance score — normalized to 0-1
        perf_score = dev['performance_score'] / 10

        # Efficiency score — normalized to 0-1
        efficiency_score = dev['efficiency_score'] / 100

        # Final weighted score
        final = (
            (0.30 * workload_score) +
            (0.30 * perf_score) +
            (0.20 * efficiency_score) +
            (0.20 * match)
        )

        scores.append({
            "developer":        dev['name'],
            "id":               dev['id'],
            "score":            round(final, 3),
            "workload":         f"{dev['workload']}%",
            "performance":      f"{dev['performance_score']}/10",
            "efficiency":       f"{dev['efficiency_score']}%",
            "skill_match":      f"{int(match * 100)}%",
            "tasks_completed":  dev['tasks_completed'],
            "avg_task_time":    f"{dev['avg_task_time']}h"
        })

    return sorted(scores, key=lambda x: x['score'], reverse=True)
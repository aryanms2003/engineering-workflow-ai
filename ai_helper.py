from groq import Groq
from database import engine
from sqlalchemy import text
import os
client = Groq(api_key=os.environ.get("GROQ_API_KEY", "your-groq-api-key-here"))

def breakdown_task(task_description):
    prompt = f"""
    You are an experienced software engineering manager.
    Break this software development task into 4-6 smaller, 
    actionable subtasks that a developer can work on independently.
    
    Task: {task_description}
    
    For each subtask include:
    - A clear title
    - Which SDLC stage it belongs to (planning/development/testing/feedback)
    - Estimated hours (realistic)
    
    Format each subtask exactly like this:
    1. [Title] | Stage: [stage] | Est: [X] hours
    
    Return ONLY the numbered list, nothing else.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )

    result = response.choices[0].message.content

    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO ai_logs (prompt, response, ai_effectiveness)
            VALUES (:p, :r, :eff)"""),
            {
                "p":   prompt,
                "r":   result,
                "eff": round(len(result.split('\n')) / 6 * 10, 1)
            })
        conn.commit()

    return result
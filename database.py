from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///project.db")

def create_tables():
    with engine.connect() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS developers (
            id INTEGER PRIMARY KEY,
            name TEXT,
            skills TEXT,
            workload INTEGER,
            performance_score FLOAT,
            efficiency_score FLOAT,
            tasks_completed INTEGER,
            avg_task_time FLOAT,
            commits INTEGER,
            sessions INTEGER
        )"""))

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT,
            description TEXT,
            status TEXT,
            stage TEXT,
            assigned_to INTEGER,
            time_spent FLOAT,
            estimated_time FLOAT,
            priority TEXT,
            code_quality_score FLOAT,
            test_coverage FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )"""))

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS ai_logs (
            id INTEGER PRIMARY KEY,
            task_id INTEGER,
            prompt TEXT,
            response TEXT,
            ai_effectiveness FLOAT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )"""))

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY,
            name TEXT,
            description TEXT,
            progress INTEGER,
            status TEXT,
            start_date TEXT,
            end_date TEXT
        )"""))
        conn.commit()

create_tables()
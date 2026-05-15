from sqlalchemy import text
from database import engine

def seed():
    developers = [
        (1,  "Aryan",   "python,sql",          40, 8.5, 87.0, 12, 3.2, 145, 38),
        (2,  "Priya",   "react,javascript",     60, 7.2, 74.0, 8,  4.1, 98,  25),
        (3,  "Rohan",   "python,ml",            30, 9.0, 92.0, 15, 2.8, 178, 45),
        (4,  "Sneha",   "sql,excel",            70, 6.8, 65.0, 6,  5.0, 67,  18),
        (5,  "Karan",   "react,python",         50, 8.0, 81.0, 10, 3.5, 120, 32),
        (6,  "Meera",   "java,spring",          45, 7.8, 79.0, 9,  3.8, 110, 28),
        (7,  "Vikram",  "devops,docker",        55, 8.2, 83.0, 11, 3.1, 134, 35),
        (8,  "Ananya",  "python,django",        35, 8.7, 89.0, 13, 2.9, 156, 41),
        (9,  "Rahul",   "javascript,node",      65, 7.0, 71.0, 7,  4.5, 89,  22),
        (10, "Pooja",   "sql,python",           25, 9.2, 94.0, 16, 2.5, 189, 48),
        (11, "Amit",    "react,typescript",     80, 6.5, 60.0, 5,  5.5, 56,  15),
        (12, "Divya",   "ml,tensorflow",        40, 8.4, 86.0, 12, 3.0, 143, 37),
        (13, "Suresh",  "java,microservices",   60, 7.5, 76.0, 8,  4.0, 102, 26),
        (14, "Nisha",   "devops,kubernetes",    50, 8.1, 82.0, 10, 3.3, 128, 33),
        (15, "Aakash",  "python,fastapi",       70, 7.3, 73.0, 7,  4.2, 91,  23),
    ]

    tasks = [
        (1,  "Build login API",         "Create REST API for login",           "done",        "development", 1,  4.5, 5.0,  "high",   8.5, 85.0),
        (2,  "Dashboard UI",            "Build analytics dashboard",           "in_progress", "development", 2,  2.0, 6.0,  "high",   7.0, 70.0),
        (3,  "DB optimization",         "Optimize slow queries",               "todo",        "planning",    3,  0.0, 4.0,  "medium", 0.0, 0.0),
        (4,  "Write unit tests",        "Cover auth module",                   "todo",        "testing",     4,  0.0, 3.0,  "low",    0.0, 0.0),
        (5,  "ML model",                "Predict task completion time",        "in_progress", "development", 3,  5.0, 8.0,  "high",   8.0, 75.0),
        (6,  "API documentation",       "Document all REST endpoints",         "done",        "feedback",    5,  3.0, 3.0,  "medium", 9.0, 90.0),
        (7,  "Setup CI/CD",             "Configure Github Actions pipeline",   "in_progress", "development", 7,  4.0, 6.0,  "high",   7.5, 80.0),
        (8,  "User authentication",     "Implement JWT auth",                  "done",        "development", 1,  6.0, 6.0,  "high",   8.8, 88.0),
        (9,  "Frontend routing",        "Setup React Router",                  "todo",        "planning",    2,  0.0, 2.0,  "medium", 0.0, 0.0),
        (10, "Data pipeline",           "Build ETL pipeline for analytics",    "in_progress", "development", 8,  3.5, 7.0,  "high",   7.8, 72.0),
        (11, "Load testing",            "Run k6 load tests on APIs",           "todo",        "testing",     9,  0.0, 4.0,  "medium", 0.0, 0.0),
        (12, "Mobile responsiveness",   "Fix UI on mobile screens",            "done",        "feedback",    5,  2.0, 2.0,  "low",    8.2, 82.0),
        (13, "Payment integration",     "Integrate Razorpay API",              "in_progress", "development", 6,  5.0, 8.0,  "high",   7.0, 68.0),
        (14, "Email notifications",     "Setup email service",                 "todo",        "planning",    10, 0.0, 3.0,  "medium", 0.0, 0.0),
        (15, "Code review process",     "Define PR review guidelines",         "done",        "feedback",    14, 1.5, 2.0,  "low",    9.5, 95.0),
        (16, "Search functionality",    "Implement elastic search",            "todo",        "planning",    12, 0.0, 6.0,  "high",   0.0, 0.0),
        (17, "Cache layer",             "Add Redis caching",                   "in_progress", "development", 7,  2.0, 4.0,  "medium", 7.2, 70.0),
        (18, "Error handling",          "Global error handler middleware",     "done",        "development", 8,  3.0, 3.0,  "medium", 8.6, 86.0),
        (19, "Integration tests",       "End to end test suite",               "todo",        "testing",     11, 0.0, 5.0,  "high",   0.0, 0.0),
        (20, "Performance monitoring",  "Setup Grafana dashboards",            "in_progress", "development", 14, 4.0, 6.0,  "high",   7.5, 75.0),
        (21, "User profile module",     "Build profile edit functionality",    "done",        "feedback",    2,  4.0, 4.0,  "medium", 8.0, 80.0),
        (22, "File upload service",     "S3 integration for file uploads",     "todo",        "planning",    8,  0.0, 4.0,  "medium", 0.0, 0.0),
        (23, "Role based access",       "Admin and user role separation",      "in_progress", "development", 1,  3.0, 5.0,  "high",   7.8, 78.0),
        (24, "Audit logging",           "Log all user actions",                "todo",        "planning",    10, 0.0, 3.0,  "low",    0.0, 0.0),
        (25, "Dark mode UI",            "Add dark mode toggle",                "done",        "feedback",    5,  2.5, 3.0,  "low",    8.4, 84.0),
        (26, "GraphQL API",             "Migrate REST to GraphQL",             "todo",        "planning",    13, 0.0, 10.0, "high",   0.0, 0.0),
        (27, "Notification service",    "Push notifications via Firebase",     "in_progress", "development", 9,  3.0, 5.0,  "medium", 7.0, 65.0),
        (28, "Backup automation",       "Daily DB backup scripts",             "done",        "development", 7,  2.0, 2.0,  "medium", 9.0, 90.0),
        (29, "Security audit",          "Penetration testing",                 "todo",        "testing",     15, 0.0, 6.0,  "high",   0.0, 0.0),
        (30, "Deployment docs",         "Write deployment runbook",            "done",        "feedback",    14, 3.0, 3.0,  "low",    9.2, 92.0),
    ]

    projects = [
        (1, "Customer Portal",    "B2C web application",         65, "active",   "2025-01-01", "2025-06-30"),
        (2, "Internal Dashboard", "Analytics platform",          40, "active",   "2025-02-01", "2025-07-31"),
        (3, "Mobile App",         "React Native mobile app",     20, "planning", "2025-03-01", "2025-09-30"),
        (4, "API Gateway",        "Microservices API layer",      80, "active",   "2024-11-01", "2025-04-30"),
        (5, "ML Pipeline",        "Data science infrastructure", 55, "active",   "2025-01-15", "2025-08-15"),
    ]

    with engine.connect() as conn:
        conn.execute(text("DELETE FROM developers"))
        conn.execute(text("DELETE FROM tasks"))
        conn.execute(text("DELETE FROM projects"))
        conn.execute(text("DELETE FROM ai_logs"))

        for d in developers:
            conn.execute(text("""
                INSERT INTO developers VALUES
                (:id,:name,:skills,:workload,:perf,:eff,:completed,:avgtime,:commits,:sessions)"""),
                {"id":d[0],"name":d[1],"skills":d[2],"workload":d[3],
                 "perf":d[4],"eff":d[5],"completed":d[6],"avgtime":d[7],
                 "commits":d[8],"sessions":d[9]})

        for t in tasks:
            conn.execute(text("""
                INSERT INTO tasks VALUES
                (:id,:title,:desc,:status,:stage,:assigned,:time,:est,:priority,:cq,:tc,CURRENT_TIMESTAMP)"""),
                {"id":t[0],"title":t[1],"desc":t[2],"status":t[3],"stage":t[4],
                 "assigned":t[5],"time":t[6],"est":t[7],"priority":t[8],"cq":t[9],"tc":t[10]})

        for p in projects:
            conn.execute(text("""
                INSERT INTO projects VALUES
                (:id,:name,:desc,:progress,:status,:start,:end)"""),
                {"id":p[0],"name":p[1],"desc":p[2],"progress":p[3],
                 "status":p[4],"start":p[5],"end":p[6]})

        conn.commit()
    print("Database seeded successfully!")

seed()
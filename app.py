import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import text
from database import engine, create_tables
from allocation import get_best_developer
from ai_helper import breakdown_task

create_tables()

# ── Custom Styling ──────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .metric-card {
        background: linear-gradient(135deg, #1e2130, #252a3a);
        border-radius: 12px;
        padding: 20px;
        border-left: 4px solid #4f8ef7;
        margin-bottom: 10px;
    }
    .risk-card {
        background: linear-gradient(135deg, #2a1a1a, #3a2020);
        border-radius: 12px;
        padding: 15px;
        border-left: 4px solid #ff4b4b;
        margin-bottom: 10px;
    }
    .stage-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
    }
    h1, h2, h3 { color: #ffffff; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ─────────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/fluency/96/source-code.png", width=60)
st.sidebar.title("EngineFlow AI")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigate", [
    "📊 Dashboard",
    "🔄 SDLC Workflow",
    "📋 Task Board",
    "🤖 AI Task Breakdown",
    "👥 Developer Analytics",
    "⚡ Allocate Task",
    "🤖 AI Usage Insights"
])

# ── Load Data Helper ─────────────────────────────────────────
def load_data():
    with engine.connect() as conn:
        tasks = pd.read_sql("SELECT * FROM tasks", conn)
        devs  = pd.read_sql("SELECT * FROM developers", conn)
        projects = pd.read_sql("SELECT * FROM projects", conn)
        ai_logs  = pd.read_sql("SELECT * FROM ai_logs", conn)
    return tasks, devs, projects, ai_logs

# ════════════════════════════════════════════════════════════
# PAGE 1: DASHBOARD
# ════════════════════════════════════════════════════════════
if page == "📊 Dashboard":
    st.title("📊 Engineering Management Dashboard")
    st.markdown("Real-time overview of your engineering team")

    tasks, devs, projects, ai_logs = load_data()

    # KPI Row
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Tasks",     len(tasks))
    col2.metric("Completed",       len(tasks[tasks.status == "done"]))
    col3.metric("In Progress",     len(tasks[tasks.status == "in_progress"]))
    col4.metric("Team Size",       len(devs))
    col5.metric("Active Projects", len(projects[projects.status == "active"]))

    st.markdown("---")

    # Row 2 — Charts
    col1, col2 = st.columns(2)

    with col1:
        fig = px.pie(tasks, names="status",
                     title="Task Status Breakdown",
                     color_discrete_sequence=["#4f8ef7","#f7a94f","#4ff7a9"])
        fig.update_layout(paper_bgcolor="#1e2130", font_color="white")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(tasks, x="stage", color="status",
                     title="Tasks by SDLC Stage",
                     color_discrete_sequence=["#4f8ef7","#f7a94f","#4ff7a9","#f74f4f"])
        fig.update_layout(paper_bgcolor="#1e2130", font_color="white")
        st.plotly_chart(fig, use_container_width=True)

    # Row 3 — Project Progress
    st.subheader("📁 Project Progress")
    for _, p in projects.iterrows():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{p['name']}** — {p['description']}")
            st.progress(p['progress'] / 100)
        with col2:
            st.metric("Progress", f"{p['progress']}%")

    # Row 4 — Risk & Bottlenecks
    st.markdown("---")
    st.subheader("⚠️ Risks & Bottlenecks")

    overloaded = devs[devs['workload'] > 65]
    if not overloaded.empty:
        for _, d in overloaded.iterrows():
            st.markdown(f"""
            <div class="risk-card">
                ⚠️ <b>{d['name']}</b> is overloaded — workload at <b>{d['workload']}%</b>
            </div>""", unsafe_allow_html=True)
    else:
        st.success("No bottlenecks detected — team workload is balanced!")

    high_priority_stuck = tasks[(tasks.priority == "high") & (tasks.status == "todo")]
    if not high_priority_stuck.empty:
        st.warning(f"{len(high_priority_stuck)} high priority tasks are not yet started!")
        st.dataframe(high_priority_stuck[['title','priority','stage']])

# ════════════════════════════════════════════════════════════
# PAGE 2: SDLC WORKFLOW
# ════════════════════════════════════════════════════════════
elif page == "🔄 SDLC Workflow":
    st.title("🔄 Software Development Lifecycle")
    st.markdown("Track tasks across all development stages")

    tasks, devs, _, _ = load_data()

    stages = ["planning", "development", "testing", "feedback"]
    colors = {"planning": "#4f8ef7", "development": "#f7a94f",
              "testing": "#a94ff7",  "feedback": "#4ff7a9"}
    icons  = {"planning": "📝", "development": "⚙️",
              "testing": "🧪",  "feedback": "💬"}

    cols = st.columns([1.2, 1.5, 1.2, 1.2])
    for i, stage in enumerate(stages):
        stage_tasks = tasks[tasks.stage == stage]
        with cols[i]:
            st.markdown(f"### {icons[stage]} {stage.capitalize()}")
            st.markdown(f"**{len(stage_tasks)} tasks**")
            st.markdown("---")
            for _, t in stage_tasks.iterrows():
                color = "#4ff7a9" if t['status'] == "done" else \
                        "#f7a94f" if t['status'] == "in_progress" else "#4f8ef7"
                st.markdown(f"""
                <div style="background:#1e2130;border-left:6px solid {color};
                     padding:12px;border-radius:12px;margin-bottom:8px">
                    <b>{t['title']}</b><br>
                    <small>Priority: {t['priority']} | Time: {t['time_spent']}h</small>
                </div>""", unsafe_allow_html=True)

    # Stage completion metrics
    st.markdown("---")
    st.subheader("Stage Completion Rate")
    stage_data = []
    for stage in stages:
        stage_tasks = tasks[tasks.stage == stage]
        done = len(stage_tasks[stage_tasks.status == "done"])
        total = len(stage_tasks)
        rate = round((done / total * 100) if total > 0 else 0, 1)
        stage_data.append({"Stage": stage.capitalize(), "Completion %": rate})

    fig = px.bar(pd.DataFrame(stage_data), x="Stage", y="Completion %",
                 color="Completion %", color_continuous_scale="teal",
                 title="Completion Rate by Stage")
    fig.update_layout(paper_bgcolor="#1e2130", font_color="white")
    st.plotly_chart(fig, use_container_width=True)

# ════════════════════════════════════════════════════════════
# PAGE 3: TASK BOARD
# ════════════════════════════════════════════════════════════
elif page == "📋 Task Board":
    st.title("📋 Task Board")

    tasks, devs, _, _ = load_data()

    # Merge developer names
    tasks = tasks.merge(devs[['id','name']], left_on='assigned_to',
                        right_on='id', how='left')
    tasks['assigned_name'] = tasks['name'].fillna("Unassigned")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("📋 To Do")
        filtered = tasks[tasks.status == "todo"]
        st.caption(f"{len(filtered)} tasks")
        for _, t in filtered.iterrows():
            st.markdown(f"""
            <div style="background:#1e2130;border-left:3px solid #4f8ef7;
                 padding:12px;border-radius:8px;margin-bottom:8px">
                <b>{t['title']}</b><br>
                <small>👤 {t['assigned_name']} | 🎯 {t['priority']} | ⏱ Est: {t['estimated_time']}h</small>
            </div>""", unsafe_allow_html=True)

    with col2:
        st.subheader("⚙️ In Progress")
        filtered = tasks[tasks.status == "in_progress"]
        st.caption(f"{len(filtered)} tasks")
        for _, t in filtered.iterrows():
            progress = int((t['time_spent'] / t['estimated_time'] * 100)
                          if t['estimated_time'] > 0 else 0)
            st.markdown(f"""
            <div style="background:#1e2130;border-left:3px solid #f7a94f;
                 padding:12px;border-radius:8px;margin-bottom:8px">
                <b>{t['title']}</b><br>
                <small>👤 {t['assigned_name']} | ⏱ {t['time_spent']}h / {t['estimated_time']}h ({progress}%)</small>
            </div>""", unsafe_allow_html=True)

    with col3:
        st.subheader("✅ Done")
        filtered = tasks[tasks.status == "done"]
        st.caption(f"{len(filtered)} tasks")
        for _, t in filtered.iterrows():
            st.markdown(f"""
            <div style="background:#1e2130;border-left:3px solid #4ff7a9;
                 padding:12px;border-radius:8px;margin-bottom:8px">
                <b>{t['title']}</b><br>
                <small>👤 {t['assigned_name']} | ✨ Quality: {t['code_quality_score']}/10 | 🧪 Coverage: {t['test_coverage']}%</small>
            </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# PAGE 4: AI TASK BREAKDOWN
# ════════════════════════════════════════════════════════════
elif page == "🤖 AI Task Breakdown":
    st.title("🤖 AI Task Breakdown")
    st.markdown("Describe a high level task — Claude will break it into subtasks")

    task_input = st.text_area("Describe your task", height=100,
                               placeholder="e.g. Build a user authentication system with OAuth")

    if st.button("✨ Break Down with AI", type="primary"):
        if task_input.strip():
            with st.spinner("Claude is thinking..."):
                result = breakdown_task(task_input)
            st.success("Here are your subtasks:")
            st.markdown(result)
            st.info("These subtasks have been logged to the AI usage database.")
        else:
            st.warning("Please enter a task description first.")

# ════════════════════════════════════════════════════════════
# PAGE 5: DEVELOPER ANALYTICS
# ════════════════════════════════════════════════════════════
elif page == "👥 Developer Analytics":
    st.title("👥 Developer Analytics")

    tasks, devs, _, _ = load_data()

    # Top metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Avg Performance", f"{devs['performance_score'].mean():.1f}/10")
    col2.metric("Avg Efficiency",  f"{devs['efficiency_score'].mean():.1f}%")
    col3.metric("Avg Workload",    f"{devs['workload'].mean():.1f}%")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(devs.sort_values("performance_score", ascending=True),
                     x="performance_score", y="name", orientation="h",
                     title="Performance Score by Developer",
                     color="performance_score",
                     color_continuous_scale="blues")
        fig.update_layout(paper_bgcolor="#1e2130", font_color="white")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(devs.sort_values("workload", ascending=True),
                     x="workload", y="name", orientation="h",
                     title="Current Workload (%)",
                     color="workload",
                     color_continuous_scale="reds")
        fig.update_layout(paper_bgcolor="#1e2130", font_color="white")
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        fig = px.scatter(devs, x="workload", y="performance_score",
                         size="tasks_completed", color="efficiency_score",
                         hover_name="name",
                         title="Workload vs Performance",
                         color_continuous_scale="viridis")
        fig.update_layout(paper_bgcolor="#1e2130", font_color="white")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(devs.sort_values("efficiency_score", ascending=True),
                     x="efficiency_score", y="name", orientation="h",
                     title="Efficiency Score (%)",
                     color="efficiency_score",
                     color_continuous_scale="greens")
        fig.update_layout(paper_bgcolor="#1e2130", font_color="white")
        st.plotly_chart(fig, use_container_width=True)

    # Average code quality per developer
    st.markdown("---")
    st.subheader("Code Quality & Output per Developer")

    with engine.connect() as conn:
        quality_df = pd.read_sql("""
            SELECT d.name, 
                   ROUND(AVG(t.code_quality_score), 2) as avg_quality,
                   ROUND(AVG(t.test_coverage), 2) as avg_coverage,
                   COUNT(t.id) as total_tasks
            FROM developers d
            LEFT JOIN tasks t ON d.id = t.assigned_to
            WHERE t.code_quality_score > 0
            GROUP BY d.name
            ORDER BY avg_quality DESC
        """, conn)

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(quality_df, x="name", y="avg_quality",
                     title="Avg Code Quality Score per Developer",
                     color="avg_quality",
                     color_continuous_scale="blues")
        fig.update_layout(paper_bgcolor="#1e2130", font_color="white")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(quality_df, x="name", y="avg_coverage",
                     title="Avg Test Coverage % per Developer",
                     color="avg_coverage",
                     color_continuous_scale="greens")
        fig.update_layout(paper_bgcolor="#1e2130", font_color="white")
        st.plotly_chart(fig, use_container_width=True)

    # Full developer table
    available_cols = [c for c in ['name','skills','workload','performance_score',
                    'efficiency_score','tasks_completed','avg_task_time',
                    'commits','sessions'] if c in devs.columns]
    st.dataframe(devs[available_cols].rename(columns={
        'name': 'Developer', 'skills': 'Skills',
        'workload': 'Workload %', 'performance_score': 'Performance',
        'efficiency_score': 'Efficiency %', 'tasks_completed': 'Tasks Done',
        'avg_task_time': 'Avg Hours/Task', 'commits': 'Commits',
        'sessions': 'Sessions'
    }), use_container_width=True)

# ════════════════════════════════════════════════════════════
# PAGE 6: ALLOCATE TASK
# ════════════════════════════════════════════════════════════
elif page == "⚡ Allocate Task":
    st.title("⚡ Smart Task Allocation")
    st.markdown("AI-powered developer matching based on skills, workload and performance")

    col1, col2 = st.columns(2)
    with col1:
        task_name     = st.text_input("Task Title")
        task_desc     = st.text_area("Task Description", height=100)
        estimated_hrs = st.number_input("Estimated Hours", min_value=1, max_value=40, value=4)
    with col2:
        skills_needed = st.text_input("Skills Required (comma separated)",
                                       placeholder="python,sql")
        priority      = st.selectbox("Priority", ["high", "medium", "low"])
        stage         = st.selectbox("SDLC Stage",
                                      ["planning","development","testing","feedback"])

    if st.button("🔍 Find Best Developer", type="primary"):
        if skills_needed.strip():
            results = get_best_developer(skills_needed)
            best    = results[0]

            st.success(f"✅ Best match: **{best['developer']}** — Score: {best['score']}")

            col1, col2, col3 = st.columns(3)
            col1.metric("Match Score",  best['score'])
            col2.metric("Skill Match",  best['skill_match'])
            col3.metric("Workload",     f"{best['workload']}")

            st.subheader("Full Developer Ranking")
            st.dataframe(pd.DataFrame(results).drop(columns=['id']),
                         use_container_width=True)

            if task_name and st.button("✅ Confirm & Assign Task"):
                with engine.connect() as conn:
                    conn.execute(text("""
                        INSERT INTO tasks
                        (title,description,status,stage,assigned_to,
                         time_spent,estimated_time,priority,code_quality_score,test_coverage)
                        VALUES (:t,:d,'todo',:stage,:a,0,:est,:p,0,0)"""),
                        {"t":task_name,"d":task_desc,"stage":stage,
                         "a":best['id'],"est":estimated_hrs,"p":priority})
                    conn.execute(text(
                        "UPDATE developers SET workload = MIN(100, workload+10) WHERE id=:id"),
                        {"id":best['id']})
                    conn.commit()
                st.success(f"Task assigned to {best['developer']}!")
        else:
            st.warning("Please enter required skills.")

# ════════════════════════════════════════════════════════════
# PAGE 7: AI USAGE INSIGHTS
# ════════════════════════════════════════════════════════════
elif page == "🤖 AI Usage Insights":
    st.title("🤖 AI Usage & Contribution")
    st.markdown("Track how AI is being used across the development workflow")

    tasks, devs, _, ai_logs = load_data()

    # AI contribution metrics
    total_tasks   = len(tasks)
    ai_assisted   = len(ai_logs)
    ai_percentage = round((ai_assisted / total_tasks * 100) if total_tasks > 0 else 0, 1)
    avg_commits   = round(devs['commits'].mean(), 1)
    avg_sessions  = round(devs['sessions'].mean(), 1)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total AI Interactions",  ai_assisted)
    col2.metric("AI Task Coverage",       f"{ai_percentage}%")
    col3.metric("Avg Commits per Dev",    avg_commits)
    col4.metric("Avg Sessions per Dev",   avg_sessions)

    st.markdown("---")

    # Commits vs Sessions scatter
    col1, col2 = st.columns(2)
    with col1:
        fig = px.scatter(devs, x="sessions", y="commits",
                         size="efficiency_score",
                         hover_name="name",
                         title="Commits vs Sessions per Developer",
                         color="efficiency_score",
                         color_continuous_scale="viridis")
        fig.update_layout(paper_bgcolor="#1e2130", font_color="white")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(devs.sort_values("commits", ascending=False),
                     x="name", y="commits",
                     title="Total Commits per Developer",
                     color="commits",
                     color_continuous_scale="blues")
        fig.update_layout(paper_bgcolor="#1e2130", font_color="white")
        st.plotly_chart(fig, use_container_width=True)

    # AI contribution summary
    st.markdown("---")
    st.subheader("AI Contribution to Development")

    done_tasks     = len(tasks[tasks.status == "done"])
    completion_rate = round((done_tasks / total_tasks * 100) if total_tasks > 0 else 0, 1)

    col1, col2, col3 = st.columns(3)
    col1.metric("Tasks Completed",    done_tasks)
    col2.metric("Completion Rate",    f"{completion_rate}%")
    col3.metric("AI Interactions",    ai_assisted)

    st.markdown("### How AI is Used in This System")
    st.markdown("""
    | Stage | AI Role |
    |---|---|
    | Planning | Breaks down high level tasks into subtasks |
    | Development | Suggests skill matched developers via allocation engine |
    | Testing | Tracks test coverage and code quality per developer |
    | Feedback | Logs all AI interactions for effectiveness analysis |
    """)

    if not ai_logs.empty:
        st.markdown("---")
        st.subheader("Recent AI Interactions")
        for _, log in ai_logs.tail(5).iterrows():
            with st.expander(f"Interaction — {log['timestamp']}"):
                st.markdown(f"**Prompt:** {log['prompt'][:200]}...")
                st.markdown(f"**Response:** {log['response'][:300]}...")
                st.markdown(f"**Effectiveness Score:** {log['ai_effectiveness']}")
    else:
        st.info("No AI interactions yet. Use the AI Task Breakdown page to generate some!")
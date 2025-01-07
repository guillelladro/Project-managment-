from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px

# Define the start date and calculate durations
project_start = datetime(2024, 11, 4)
tasks = [
    {"Task": "Requirement gathering", "Start": project_start, "End": project_start + timedelta(weeks=2)},
    {"Task": "WBS development", "Start": project_start + timedelta(weeks=2), "End": project_start + timedelta(weeks=3)},
    {"Task": "API integration", "Start": project_start + timedelta(weeks=3), "End": project_start + timedelta(weeks=6)},
    {"Task": "Data handling", "Start": project_start + timedelta(weeks=3), "End": project_start + timedelta(weeks=6)},
    {"Task": "UI/UX design", "Start": project_start + timedelta(weeks=4), "End": project_start + timedelta(weeks=7)},
    {"Task": "Accessibility features", "Start": project_start + timedelta(weeks=4), "End": project_start + timedelta(weeks=7)},
    {"Task": "Unit testing", "Start": project_start + timedelta(weeks=7), "End": project_start + timedelta(weeks=9)},
    {"Task": "Integration testing", "Start": project_start + timedelta(weeks=7), "End": project_start + timedelta(weeks=9)},
    {"Task": "Deployment", "Start": project_start + timedelta(weeks=9), "End": project_start + timedelta(weeks=10)},
]

# Create a DataFrame
df = pd.DataFrame(tasks)

# Convert dates to strings for better formatting
df["Start"] = df["Start"].dt.strftime('%Y-%m-%d')
df["End"] = df["End"].dt.strftime('%Y-%m-%d')

# Create Gantt chart
fig = px.timeline(df, x_start="Start", x_end="End", y="Task", title="Project Gantt Chart", color="Task")
fig.update_yaxes(categoryorder="total ascending")
fig.update_layout(xaxis_title="Timeline", yaxis_title="Tasks", showlegend=False)

fig.show()
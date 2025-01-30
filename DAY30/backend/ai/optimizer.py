import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

class TaskOptimizer:
    def __init__(self, db_session):
        self.db_session = db_session

    def fetch_task_data(self):
        query = "SELECT id, title, priority, estimated_time, deadline FROM tasks WHERE completed = 0"
        return pd.read_sql(query, self.db_session.bind)

    def train_model(self, task_data):
        X = task_data[["priority", "estimated_time"]].values
        y = task_data["deadline"].apply(lambda d: (d - datetime.now()).total_seconds()).values
        model = LinearRegression()
        model.fit(X, y)
        return model

    def optimize_schedule(self):
        task_data = self.fetch_task_data()
        if task_data.empty:
            return []

        model = self.train_model(task_data)
        task_data["priority_score"] = model.predict(task_data[["priority", "estimated_time"]])
        task_data = task_data.sort_values("priority_score", ascending=False)
        
        return task_data[["id", "title", "priority", "estimated_time", "deadline"]].to_dict(orient="records")

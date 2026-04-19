import pandas as pd
from database.db_connection import get_connection
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load user activity data from database
def load_user_data():
    conn = get_connection()

    query = """
    SELECT 
        user_id,
        COUNT(*) AS total_searches,
        MAX(search_date) AS last_activity
    FROM search_logs
    GROUP BY user_id;
    """

    df = pd.read_sql(query, conn)
    conn.close()

    # Convert last_activity to datetime
    df["last_activity"] = pd.to_datetime(df["last_activity"])

    # Calculate number of inactive days
    df["days_inactive"] = (pd.Timestamp.now() - df["last_activity"]).dt.days

    # Create churn label
    df["churn"] = df["days_inactive"].apply(lambda x: 1 if x > 15 else 0)
    
    return df

def train_churn_model(df):
    X = df[["total_searches", "days_inactive"]]
    y = df["churn"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    return model, X_test, y_test


def predict_churn(model, df):
    X = df[["total_searches", "days_inactive"]]
    df["predicted_churn"] = model.predict(X)

    return df


df = load_user_data()
model, X_test, y_test = train_churn_model(df)
df = predict_churn(model, df)

print(df[["user_id", "total_searches", "days_inactive", "churn", "predicted_churn"]])

df.to_csv("churn_results.csv", index=False)
print("Churn results exported successfully")
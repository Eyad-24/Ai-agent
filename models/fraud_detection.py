import pandas as pd
from database.db_connection import get_connection
from sklearn.ensemble import IsolationForest

conn = get_connection()

query = """
SELECT trans_id, amount
FROM public.transactions;
"""

df = pd.read_sql(query, conn)

# Apply Isolation Forest
model = IsolationForest(contamination=0.3, random_state=42)

df["fraud"] = model.fit_predict(df[["amount"]])

# Convert predictions
df["fraud"] = df["fraud"].apply(lambda x: 1 if x == -1 else 0)

print(df)
conn.close()

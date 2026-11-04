import pandas as pd
import psycopg2
from database.db_connection import get_connection

from prophet import Prophet
import matplotlib.pyplot as plt

conn = get_connection()

# Query transaction data
query = """
SELECT trans_date, amount
FROM public.transactions
ORDER BY trans_date;
"""

df = pd.read_sql(query, conn)
conn.close()

# Rename columns for Prophet
df.columns = ["ds", "y"]

# Convert date column
df["ds"] = pd.to_datetime(df["ds"])

# Create model
model = Prophet()

# Train model
model.fit(df)

# Create future dates (next 5 days)
future = model.make_future_dataframe(periods=5)

# Predict
forecast = model.predict(future)

# Show forecast table
print(forecast[["ds", "yhat"]])

# Plot results
model.plot(forecast)
plt.show()

# Save forecast results to CSV
forecast[['ds', 'yhat']].to_csv('forecast.csv', index=False)



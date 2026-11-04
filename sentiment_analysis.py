import psycopg2
from database.db_connection import get_connection
from textblob import TextBlob

conn = get_connection()

# Read reviews
cur = conn.cursor()
cur.execute("SELECT review_id, review_text FROM public.reviews;")
reviews = cur.fetchall()

# Analyze sentiment
for review_id, review_text in reviews:
    polarity = TextBlob(review_text).sentiment.polarity

    if polarity > 0:
        sentiment = "Positive"
    elif polarity < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    cur.execute(
        "UPDATE public.reviews SET sentiment = %s WHERE review_id = %s;",
        (sentiment, review_id)
    )
    print(f"Review ID: {review_id} | Sentiment: {sentiment}")

conn.commit()
cur.close()
conn.close()
print("Sentiment analysis completed successfully.")
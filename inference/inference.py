from openai import OpenAI

from database.database import Database
client = OpenAI()

def infer(ticker: str, sheets: list[str], force=False) -> str:
  db = Database.get_instance()
  if not force and db.inference_is_cached(ticker):
    inference = db.get_inference(ticker)
    return inference

  prompt = ''.join(sheets)
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are a financial analyst provided with historical 10K consolidated balance sheet filings for a company. Generate insight on the trend of assets compared to liabilities."},
      {"role": "user", "content": prompt}
    ]
  )

  db.cache_inference(ticker, completion.choices[0].message.content)

  return completion.choices[0].message.content
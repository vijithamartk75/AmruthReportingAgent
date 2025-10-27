from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from database import engine
import re

app = FastAPI(title="Sales Analytics & AI Agent")

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Welcome to Sales Analytics API!"}

@app.get("/sales/by-date")
def get_sales_by_date(date: str = Query(..., description="Date in YYYY-MM-DD format")):
    query = text("""
        SELECT COUNT(*) AS invoice_count, SUM(NetAmt) AS total_sales
        FROM Invtotal
        WHERE 
            CAST(InvDt AS DATE) = CAST(:date AS DATE)
            AND (Cancelled = 0 OR Cancelled IS NULL);
    """)
    try:
        with engine.connect() as conn:
            result = conn.execute(query, {"date": date}).fetchone()
            return {
                "date": date,
                "invoice_count": result.invoice_count if result.invoice_count else 0,
                "total_sales": float(result.total_sales or 0)
            }
    except Exception as e:
        return {"error": str(e)}

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    text_input = body.get("text", "").lower().strip()
    date_match = re.search(r"\d{4}-\d{2}-\d{2}", text_input)

    try:
        with engine.connect() as conn:
            if "today" in text_input:
                query = text("""
                    SELECT COUNT(*) AS invoice_count, SUM(NetAmt) AS total_sales
                    FROM Invtotal
                    WHERE CAST(InvDt AS DATE) = CAST(GETDATE() AS DATE)
                    AND (Cancelled = 0 OR Cancelled IS NULL);
                """)
                result = conn.execute(query).fetchone()
                return {
                    "reply": f"Today's invoices: {result.invoice_count or 0}, total sales: ₹{float(result.total_sales or 0):,.2f}"
                }

            elif date_match:
                date = date_match.group(0)
                query = text("""
                    SELECT COUNT(*) AS invoice_count, SUM(NetAmt) AS total_sales
                    FROM Invtotal
                    WHERE CAST(InvDt AS DATE) = CAST(:date AS DATE)
                    AND (Cancelled = 0 OR Cancelled IS NULL);
                """)
                result = conn.execute(query, {"date": date}).fetchone()
                return {
                    "reply": f"On {date}, invoices: {result.invoice_count or 0}, total sales: ₹{float(result.total_sales or 0):,.2f}"
                }

            elif "last 7 days" in text_input or "weekly" in text_input:
                query = text("""
                    SELECT COUNT(*) AS invoice_count, SUM(NetAmt) AS total_sales
                    FROM Invtotal
                    WHERE InvDt >= CAST(DATEADD(DAY, -7, GETDATE()) AS DATE)
                    AND (Cancelled = 0 OR Cancelled IS NULL);
                """)
                result = conn.execute(query).fetchone()
                return {
                    "reply": f"In the last 7 days: {result.invoice_count or 0} invoices, total sales: ₹{float(result.total_sales or 0):,.2f}"
                }

            else:
                return {
                    "reply": "I can help you with sales data. Try asking: "
                             "'sales today', 'sales on 2025-12-18', or 'sales in last 7 days'."
                }

    except Exception as e:
        return {"reply": f"Error occurred: {str(e)}"}

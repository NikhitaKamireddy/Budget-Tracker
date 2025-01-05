from flask import Flask, render_template, request, redirect
import pandas as pd
import os

app = Flask(__name__)

# File to store budget data
BUDGET_FILE = "budget_data.csv"

# Initialize file if not exists
if not os.path.exists(BUDGET_FILE):
    df = pd.DataFrame(columns=["Date", "Description", "Amount"])
    df.to_csv(BUDGET_FILE, index=False)

@app.route("/")
def index():
    df = pd.read_csv(BUDGET_FILE)
    total = df["Amount"].sum()
    return render_template("index.html", data=df.to_dict(orient="records"), total=total)

@app.route("/add", methods=["POST"])
def add_entry():
    date = request.form["date"]
    description = request.form["description"]
    amount = float(request.form["amount"])

    df = pd.read_csv(BUDGET_FILE)
    df = df.append({"Date": date, "Description": description, "Amount": amount}, ignore_index=True)
    df.to_csv(BUDGET_FILE, index=False)

    return redirect("/")

@app.route("/clear")
def clear_entries():
    pd.DataFrame(columns=["Date", "Description", "Amount"]).to_csv(BUDGET_FILE, index=False)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

from app import app
from flask import render_template, request, redirect,url_for,flash


@app.route("/admin/dashboard")
def admin():
  return render_template('admin/dashboard.html')

@app.route("/admin/profile")
def adminProfile():
  return render_template('admin/profile.html')

@app.route("/admin/home")
def home():
  return f"<h1>home</h1>"
from flask import Blueprint, render_template, redirect
from . import db
from flask_login import login_required, current_user

main = Blueprint("main", __name__)

@main.route("/")
def index():
	if current_user and current_user.is_authenticated:
		return redirect("/dash/dashboard/")
	else:
		return render_template("login.html")


@main.route("/profile")
@login_required
def profile():
	return render_template("profile.html", name=current_user.name)
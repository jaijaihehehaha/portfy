from flask import Blueprint, render_template, current_app, abort
from ..models import User


public_bp = Blueprint('public', __name__, url_prefix='')


@public_bp.route('/')
def index():
    return render_template('public/index.html')


@public_bp.route('/p/<username>')
def public_portfolio(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404)
    projects = user.projects
    return render_template('public/portfolio_clean.html', user=user, projects=projects, settings=user.settings)
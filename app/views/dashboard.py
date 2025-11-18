from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file
from .. import db
from flask_login import login_required, current_user
from ..models import Project, User, PortfolioSettings
from datetime import datetime
import os


dash_bp = Blueprint('dash', __name__, url_prefix='/dashboard')


@dash_bp.route('/')
@login_required
def dashboard():
    return render_template(
        "dashboard/index.html",
        projects=current_user.projects,
        settings=current_user.settings
    )

@dash_bp.route('/project/new', methods=['POST'])
@login_required
def new_project():
    title = request.form['title']
    description = request.form.get('description')
    github_url = request.form.get('github_url')
    tags = request.form.get('tags')

    project = Project(
        user_id=current_user.id,
        title=title,
        description=description,
        github_url=github_url,
        tags=tags
    )
    db.session.add(project)
    db.session.commit()
    flash('Project added!', 'success')
    return redirect(url_for('dash.dashboard'))


@dash_bp.route('/delete/<int:project_id>', methods=['POST'])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        flash('Not authorized', 'danger')
        return redirect(url_for('dash.dashboard'))

    db.session.delete(project)
    db.session.commit()
    flash('Project deleted', 'info')
    return redirect(url_for('dash.dashboard'))


@dash_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        theme = request.form.get('theme') or 'clean'
        accent = request.form.get('accent_color') or '#1f2937'
        if not current_user.settings:
            s = PortfolioSettings(user_id=current_user.id, theme=theme, accent_color=accent)
            db.session.add(s)
        else:
            current_user.settings.theme = theme
            current_user.settings.accent_color = accent
        db.session.commit()
        print("Theme saved:", settings.theme)
        print("Accent:", settings.accent_color)
        flash('Settings saved', 'success')
        return redirect(url_for('dash.settings'))
    return render_template('dashboard/settings.html', settings=current_user.settings)


@dash_bp.route('/export', methods=['POST'])
@login_required
def export_portfolio():
    # Get user projects
    projects = Project.query.filter_by(user_id=current_user.id).order_by(Project.order_index).all()

    # Render the portfolio HTML using a template
    portfolio_html = render_template('export/portfolio.html', user=current_user, projects=projects)

    # Save to a temporary file
    export_dir = os.path.join(os.getcwd(), 'exports')
    os.makedirs(export_dir, exist_ok=True)
    filename = f"{current_user.username}_portfolio_{datetime.now().strftime('%Y%m%d%H%M%S')}.html"
    filepath = os.path.join(export_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(portfolio_html)

    # Send file for download
    return send_file(filepath, as_attachment=True)

@dash_bp.route("/update-settings", methods=["POST"])
@login_required
def update_settings():
    # Create settings row if user doesn't have one yet
    if not current_user.settings:
        settings = PortfolioSettings(user_id=current_user.id)
        db.session.add(settings)
        db.session.commit()

    current_user.settings.theme = request.form["theme"]
    current_user.settings.accent_color = request.form["accent_color"]
    db.session.commit()

    flash("Theme updated!", "success")
    return redirect(url_for("dash.dashboard"))

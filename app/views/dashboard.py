from flask import Blueprint, render_template, redirect, url_for, flash, request
from .. import db
from flask_login import login_required, current_user


dash_bp = Blueprint('dash', __name__, url_prefix='/dashboard')


@dash_bp.route('/')
@login_required
def dashboard():
    projects = Project.query.filter_by(user_id=current_user.id).order_by(Project.order_index).all()
    settings = current_user.settings
    return render_template('dashboard/index.html', projects=projects, settings=settings)


@dash_bp.route('/project/new', methods=['POST'])
@login_required
def new_project():
    title = request.form.get('title')
    description = request.form.get('description')
    github = request.form.get('github_url')
    tags = request.form.get('tags')
    project = Project(user_id=current_user.id, title=title, description=description, github_url=github, tags=tags)
    db.session.add(project)
    db.session.commit()
    flash('Project added', 'success')
    return redirect(url_for('dash.dashboard'))


@dash_bp.route('/project/delete/<int:project_id>', methods=['POST'])
@login_required
def delete_project(project_id):
    proj = Project.query.filter_by(id=project_id, user_id=current_user.id).first_or_404()
    db.session.delete(proj)
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
        flash('Settings saved', 'success')
        return redirect(url_for('dash.settings'))
    return render_template('dashboard/settings.html', settings=current_user.settings)


@dash_bp.route('/export', methods=['POST'])
@login_required
def export_portfolio():
# Simple export: render public template and save HTML to a file in 'exports/<username>.html'
    from flask import current_app
    import os
    rendered = render_template('public/portfolio_clean.html', user=current_user, projects=current_user.projects, settings=current_user.settings)
    export_dir = os.path.join(current_app.root_path, '..', 'exports')
    os.makedirs(export_dir, exist_ok=True)
    filepath = os.path.join(export_dir, f'{current_user.username}.html')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(rendered)
    flash(f'Exported to {filepath}', 'success')
    return redirect(url_for('dash.dashboard'))
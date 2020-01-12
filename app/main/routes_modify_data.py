"""
import json
import re

from flask import render_template, flash, redirect, url_for
from flask import request
from flask_login import login_required

from app import current_app, db
from app.main import bp
from app.main.forms import UserForm, PaperForm
from app.models import User, Paper, Comment
from datetime import datetime


@bp.route('/modify_user/<user_id>', methods=['GET', 'POST'])
@login_required
def modify_user(user_id):
    user = User.query.filter_by(id=user_id).first()

    data_form = dict(name=user.name,
                     email=user.email,
                     phone=user.phone)

    form = UserForm(data=data_form)

    if form.validate_on_submit():

        user.name = form.name.data
        user.email = form.email.data
        user.phone = form.phone.data

        db.session.add(user)
        db.session.commit()

        flash('Your user has been modified.')
        return redirect(url_for('main.see_user', user_id=user_id))

    return render_template('insert_data.html', title='Modify user', form=form, header='Modify user')

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@bp.route('/modify_paper/<paper_id>', methods=['GET', 'POST'])
@login_required
def modify_paper(paper_id):
    paper = Paper.query.filter_by(id=paper_id).first()

    data_form = dict(title=paper.title,
                     description=paper.description,
                     due_date=paper.due_date,
                     status=paper.status,
                     user=paper.user)

    form = TaskForm(data=data_form)

    if form.validate_on_submit():
        paper.title = form.title.data
        paper.description = form.description.data
        paper.updated = datetime.now()
        paper.due_date = form.due_date.data
        paper.status = form.status.data
        paper.user = form.user.data

        db.session.add(paper)
        db.session.commit()

        flash('Your task has been modified.')
        return redirect(url_for('main.see_task', task_id=task_id))

    return render_template('insert_data.html', title='Modify task', form=form, header='Modify task')
"""
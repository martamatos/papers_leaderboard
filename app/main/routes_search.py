from flask import render_template, flash, redirect, url_for
from flask_login import login_required

from sqlalchemy import or_
from app import db
from app.main import bp
from app.main.forms import SearchForm
from app.models import User, Paper
from app.utils.parsers import parse_input_list


@bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()

    if form.validate_on_submit():
        empty = False
        data = None

        if form.data_type.data == 'task':
            data = Paper.query.filter(or_(Paper.title.like(f'%{form.search_text.data}%'),
                                         Paper.description.like(f'%{form.search_text.data}%'))).all()

        elif form.data_type.data == 'user':
            data = User.query.filter(User.name.like(f'%{form.search_text.data}%')).all()

        if not data:
            empty = True

        return render_template('search_results.html', title='Search results', data=data,
                               empty=empty, data_type=form.data_type.data,
                               search_text=form.search_text.data, header='Search results')

    return render_template('insert_data.html', title='Search', form=form, header='Search')


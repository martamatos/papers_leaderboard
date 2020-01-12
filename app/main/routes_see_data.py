from flask import Markup
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required

from app import current_app, db
from app.main import bp
from app.main.forms import ModifyDataForm

from app.models import User, Paper, Comment


@bp.route('/see_user_leaderboard')
#@login_required
def see_user_leaderboard():
    tab_status = {"users": "active", "papers": "#"}
    header = Markup("<th>Papers read</th> \
                    <th>Name</th> \
                    <th>Email</th>")

    # enzyme_header = Enzyme.__table__.columns.keys()
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.id.asc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.see_user_leaderboard', page=users.next_num) \
        if users.has_next else None
    prev_url = url_for('main.see_user_leaderboard', page=users.prev_num) \
        if users.has_prev else None
    return render_template("see_data.html", title='See user leaderboard', data=users.items,
                           data_type='user', tab_status=tab_status, header=header,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/see_user/<user_id>', methods=['GET', 'POST'])
@login_required
def see_user(user_id):
    user = User.query.filter_by(id=user_id).first()

    data = []
    data_nested = []

    data.append({'field_name': 'Name', 'data': user.name})
    data.append({'field_name': 'Email', 'data': user.email})

    # papers
    # comments

    form = ModifyDataForm()
    if form.validate_on_submit():
        return redirect(url_for('main.modify_user', user_id=user_id))

    return render_template("see_data_element.html", title='See user', data_name=user.name, data_type='user',
                           data_list=data, data_list_nested=data_nested, form=form)


@bp.route('/see_paper_leaderboard')
#@login_required
def see_paper_leaderboard():
    tab_status = {"users": "#", "papers": "active"}
    header = Markup("<th>Read</th> \
                    <th>Title</th> \
                    <th>First author</th> \
                    <th>Last author</th> \
                    <th>DOI</th> \
                    <th>Rating</th>")

    # enzyme_header = Enzyme.__table__.columns.keys()
    page = request.args.get('page', 1, type=int)
    papers = Paper.query.order_by(Paper.id.asc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.see_paper_leaderboard', page=papers.next_num) \
        if papers.has_next else None
    prev_url = url_for('main.see_paper_leaderboard', page=papers.prev_num) \
        if papers.has_prev else None
    return render_template("see_data.html", title='See paper leaderboard', data=papers.items,
                           data_type='paper', tab_status=tab_status, header=header,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/see_paper/<paper_id>', methods=['GET', 'POST'])
@login_required
def see_paper(paper_id):
    paper = Paper.query.filter_by(id=paper_id).first()

    data = []
    data_nested = []

    data.append({'field_name': 'Title', 'data': paper.title})
    data.append({'field_name': 'First author', 'data': paper.first_author})
    data.append({'field_name': 'Last author', 'data': paper.last_author})
    data.append({'field_name': 'DOI', 'data': paper.doi})
    #data.append({'field_name': 'Rating', 'data': paper.rating})

    # comments
    # read by

    form = ModifyDataForm()
    if form.validate_on_submit():
        return redirect(url_for('main.modify_paper', paper_id=paper_id))

    return render_template("see_data_element.html", title='See paper', data_name=paper.title,
                           data_type='paper', data_list=data, data_list_nested=data_nested, form=form)


from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
#from flask_login import current_user, login_user

from app import db
from app.main import bp
from app.main.forms import PaperForm, CommentForm
from app.models import User, Paper, Comment
from app.utils.parsers import parse_input_list


@bp.route('/add_paper', methods=['GET', 'POST'])
#@login_required
def add_paper():
    form = PaperForm()

    if form.validate_on_submit():
        paper = Paper(title=form.title.data,
                      first_author=form.first_author.data,
                      last_author=form.last_author.data,
                      doi=form.doi.data)

        db.session.add(paper)
        db.session.commit()

        comment = Comment(paper_id=paper.id,
                          user_id=current_user.id,
                          rating=form.rating.data,
                          comment=form.comment.data)

        db.session.add(comment)
        db.session.commit()

        flash('Your paper is now live!', 'success')
        return redirect(url_for('main.see_paper_leaderboard'))

    return render_template('insert_data.html', title='Add paper', form=form, header='Add paper')


@bp.route('/add_comment', methods=['GET', 'POST'])
@login_required
def add_comment():
    form = CommentForm()

    if form.validate_on_submit():
        comment = Comment(paper_id=form.paper.id,
                          user_id=current_user.id,
                          rating=form.rating.data,
                          comment=form.rating.data)

        db.session.add(comment)
        db.session.commit()

        flash('Your comment is now live!', 'success')
        return redirect(url_for('main.see_paper_leaderboard'))

    return render_template('insert_data.html', title='Add comment', form=form, header='Add comment')

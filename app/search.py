from flask import render_template, redirect, url_for, flash, request
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from flask_wtf import FlaskForm

from flask import Blueprint
bp = Blueprint('search', __name__)


class DisplayForm():
	def __init__(self, content):
		self.content = content

class SearchForm(FlaskForm):
	search_kw = StringField('Search', validators=[DataRequired()])
	submit = SubmitField('Search')


@bp.route('/', methods=['GET', 'POST'])
def search_product():
	form = SearchForm()
	if form.validate_on_submit():
		return redirect(url_for('search.display_product', messages=form.search_kw.data))

	return "Error"

@bp.route('/result_page', methods=['GET', 'POST'])
def display_product():
	messages = request.args['messages']
	# do things here to get products data
	form = DisplayForm(messages)
	return render_template('search.html', title='Search Result', form=form)

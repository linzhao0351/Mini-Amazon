from flask import render_template, redirect, url_for, flash, request
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from flask_wtf import FlaskForm

from .models.search import Search

from flask import Blueprint
bp = Blueprint('search', __name__)


class SearchForm(FlaskForm):
	search_kw = StringField('Search', validators=[DataRequired()])
	submit = SubmitField('Search')


@bp.route('/', methods=['GET', 'POST'])
def search_product():
	form = SearchForm()
	if form.validate_on_submit():
		return redirect(url_for('search.display_product', search_kw=form.search_kw.data))

	return "Error"

@bp.route('/result_page', methods=['GET', 'POST'])
def display_product():
	search_kw = request.args['search_kw']
	
	matched_products = Search.search_product(search_kw)
	no_match = matched_products is None

	return render_template('search.html', title='Search Result', results=matched_products, 
																 no_match=no_match, 
																 search_kw=search_kw)

from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, ValidationError

from .models.product import Product
from .models.search import Search

from .models.recommend import Recommend

from flask import Blueprint
bp = Blueprint('index', __name__)


class SearchForm(FlaskForm):
    search_kw = StringField('Search', validators=[DataRequired()])
    typelist = SelectField('Category')
    submit = SubmitField('Search')


@bp.route('/', methods=['GET', 'POST'])
def index():
    # get all available products for sale:
    products = Product.get_all(True)
    products = products[0:min(len(products), 100)]

    # recommend current user products
    if current_user.is_authenticated:
        recent_viewed = Recommend.rec_recent_viewed_item(current_user.id)
        no_recent_viewed = recent_viewed is None
        if no_recent_viewed:
            pass
        else:
            recent_viewed = recent_viewed[0:min(len(recent_viewed),5)]

        most_viewed = Recommend.rec_most_viewed_item(current_user.id)
        no_most_viewed = most_viewed is None
        if no_most_viewed:
            pass
        else:
            most_viewed = most_viewed[0:min(len(most_viewed),5)]
    else:
        recent_viewed = None
        no_recent_viewed = None
        most_viewed = None
        no_most_viewed = None

    form = SearchForm()
    form.typelist.choices = Search.get_all_types()
    if form.validate_on_submit():
        return redirect(url_for('index.display_product', search_kw=form.search_kw.data, type_id=form.typelist.data ))

    return render_template('index.html',
                           avail_products=products,
                           form=form, 
                           recent_viewed=recent_viewed, no_recent_viewed=no_recent_viewed,
                           most_viewed=most_viewed, no_most_viewed=no_most_viewed)


@bp.route('/result_page', methods=['GET', 'POST'])
def display_product():
    search_kw = request.args['search_kw']
    type_id = request.args['type_id']

    matched_products = Search.search_product(search_kw, type_id)
    no_match = matched_products is None

    return render_template('search.html', title='Search Result', results=matched_products, 
                                                                 no_match=no_match, 
                                                                 search_kw=search_kw)

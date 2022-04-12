from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('index', __name__)


from .search import SearchForm

@bp.route('/')
def index():
    # get all available products for sale:
    products = Product.get_all(True)
    # find the products current user has bought:
    if current_user.is_authenticated:
        pass
    else:
        purchases = None
    # render the page by adding information to the index.html file

    form = SearchForm()
    return render_template('index.html',
                           avail_products=products,
                           form=form)

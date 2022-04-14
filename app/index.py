from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase

from .search import SearchForm
from .models.recommend import Recommend

from flask import Blueprint
bp = Blueprint('index', __name__)


@bp.route('/')
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
    return render_template('index.html',
                           avail_products=products,
                           form=form, 
                           recent_viewed=recent_viewed, no_recent_viewed=no_recent_viewed,
                           most_viewed=most_viewed, no_most_viewed=no_most_viewed)


from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FormField, FieldList, IntegerField, BooleanField, TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from datetime import datetime
from flask import Blueprint
bp = Blueprint('seller', __name__)

from .models.user import User
from .models.inventory import Inventory
from .models.seller_order import SellerOrder
from .models.analytics import Analytics
from .models.review import Product_Review, Seller_Review
from .models.search import Search

@bp.route('/seller/account')
def seller_portal():
	if current_user.is_authenticated:
		return render_template('seller_portal.html')
	else:
		return redirect(url_for('index.index'))


@bp.route('/seller/account/my-profile') # can directly copy from Mae's part
def my_profile():
	return redirect(url_for('customer.my_profile'))




@bp.route('/seller/account/my-balance') # can directly copy from Mae's part
def my_balance():
	msg = "Hello world!"
	return render_template('seller_my_balance.html', info = msg)



############### code starts here ###############
class ItemForm(FlaskForm):
	name = StringField('Product Name', validators=[DataRequired()])
	price = StringField('Price', validators=[DataRequired()])
	quantity = StringField('Quantity', validators=[DataRequired()])
	available = BooleanField('Available')
	short_desc = TextAreaField('Short Description')
	long_desc = TextAreaField('Long Description')
	type_id = SelectField('Category')
	submit = SubmitField('Add Item')

@bp.route('/seller/account/my-inventory', methods=['GET', 'POST'])
def my_inventory():
	inventory = Inventory.get(current_user.id)	
	return render_template('seller_my_inventory.html', inventory = inventory)

# add product
@bp.route('/seller/account/my-inventory/add_product', methods=['GET', 'POST'])
def my_inventory_add_product():
	form = ItemForm()
	form.type_id.choices = Search.get_all_types()
	if form.validate_on_submit():
		Inventory.add_product(current_user.id, 
							  form.name.data, 
							  form.price.data, 
							  form.quantity.data, 
							  form.available.data,
							  form.short_desc.data,
							  form.long_desc.data,
							  form.type_id.data)
		return redirect(url_for('seller.my_inventory'))
	return render_template('seller_add_product.html', form=form)

# edit inventory
class InventoryUpdateForm(FlaskForm):
	price = StringField('New Price')
	submit = SubmitField('Update Price')	
	quantity = StringField('New Quantity')
	type_id = SelectField('Category')
	available = BooleanField('Available')
	short_desc = TextAreaField('Short Description')
	long_desc = TextAreaField('Long Description')
	submit = SubmitField('Update Availability')	

@bp.route('/seller/account/my-inventory/update/<pid>', methods=['GET', 'POST'])
def update_inventory(pid):
	inventory = Inventory.get_product(pid, current_user.id)
	form = InventoryUpdateForm()
	form.type_id.choices = Search.get_all_types()
	if form.validate_on_submit():
		Inventory.update(pid, current_user.id, 
						form.price.data,
						form.quantity.data,
						form.available.data,
						form.short_desc,
						form.long_desc,
						form.type_id)
		return redirect(url_for('seller.my_inventory'))
	return render_template('seller_update_inventory.html', inventory=inventory, form=form)

# delete product
@bp.route('/seller/account/my-inventory/delete/<pid>', methods=['GET', 'POST'])
def delete_item(pid):
	Inventory.delete_product(pid, current_user.id)
	return redirect(url_for('seller.my_inventory'))

# analytics of inventory 
@bp.route('/seller/account/my-inventory/analytics', methods=['GET', 'POST'])
def analytics():
	products = Inventory.product_with_limited_inventory(current_user.id, 10)
	trendy_products = Analytics.get_trendy_prod(current_user.id)
	return render_template('seller_analytics.html', products = products, trendy_products = trendy_products)




### order fulfillment
# display order details
@bp.route('/seller/account/my-orders', methods=['GET', 'POST'])
def my_orders():
	orders = SellerOrder.get(current_user.id)
	
	is_none = False
	if orders is None:
		is_none = True
		return render_template('seller_my_orders.html', is_none=is_none)

	orders_dict = {}
	for item in orders:
		if item.order_id in orders_dict.keys():
			orders_dict[item.order_id].append(item)
		else:
			orders_dict[item.order_id] = [item]

	orders_summary = {}
	for order_id in orders_dict.keys():
		orders_summary[order_id] = SellerOrder.get_order_summary(order_id)

	return render_template('seller_my_orders.html', is_none=is_none, orders_dict = orders_dict, orders_summary=orders_summary)


# edit fake order info [can be deleted later]
class OrderForm(FlaskForm):
	uid = StringField('Buyer ID', validators=[DataRequired()])
	pid = StringField('Product ID', validators=[DataRequired()])
	price = StringField('Price', validators=[DataRequired()])
	quantity = StringField('Quantity', validators=[DataRequired()])
	submit = SubmitField('Add Fake Order')


# update fulillment status
class FulfillmentForm(FlaskForm):
	fulfillment = BooleanField('Order Completed?')
	submit = SubmitField('Submit')	


@bp.route('/seller/account/my-orders/order_fulfill/<order_id>/<product_id>', methods=['GET', 'POST'])
def order_fulfill(order_id, product_id):
	product = SellerOrder.get_product(order_id, product_id)
	form = FulfillmentForm()
	if form.validate_on_submit():
		SellerOrder.update(order_id, product_id, int(form.fulfillment.data))
		return redirect(url_for('seller.my_orders'))
	return render_template('seller_update_fulfillment.html', product=product, form=form)	


@bp.route('/seller/account/my-orders/summary', methods=['GET', 'POST'])
def order_summary():
	num_order = SellerOrder.norder(current_user.id)
	mean_nprod_rev = SellerOrder.mean_nprod_rev(current_user.id)
	return render_template('seller_fulfillment_summary.html', num_order = num_order[0][0], mean_nprod_rev = mean_nprod_rev[0])

############### code ends #############




@bp.route('/seller/account/my-reviews', methods=['GET', 'POST'])
def my_reviews():
	all_reviews = Product_Review.get_all_reviews_seller(current_user.id)
	all_seller_reviews = Seller_Review.get_all_reviews_seller(current_user.id)
	return render_template('seller_my_reviews.html', all_reviews=all_reviews, all_seller_reviews=all_seller_reviews)


@bp.route('/public_profile/seller/<seller_id>', methods=['GET', 'POST'])
def public_profile(seller_id):
	userinfo = User.get(current_user.id)

	top_upvotes = Seller_Review.get_top_upvotes(seller_id)
	most_recent = Seller_Review.get_most_recent(seller_id)
	review_count = Seller_Review.total_reviews(seller_id)
	average_rating = Seller_Review.average_rating(seller_id)
	
	if request.form.get("Seller_Upvote_1"):
		if Seller_Review.upvote_exists(current_user.id,request.form.get('Seller_Upvote_1')):
			Seller_Review.downvote(current_user.id,request.form.get('Seller_Upvote_1'))
			return redirect(url_for('seller.public_profile', seller_id=seller_id))	
		else:
			print('here')
			Seller_Review.upvote(current_user.id,request.form.get('Seller_Upvote_1'))
			return redirect(url_for('seller.public_profile',  seller_id=seller_id))
	
	if request.form.get("Seller_Upvote_2"):
		if Seller_Review.upvote_exists(current_user.id,request.form.get('Seller_Upvote_2')):
			Seller_Review.downvote(current_user.id,request.form.get('Seller_Upvote_2'))
			return redirect(url_for('seller.public_profile',  seller_id=seller_id))	
		else:
			Seller_Review.upvote(current_user.id,request.form.get('Seller_Upvote_2'))
			return redirect(url_for('seller.public_profile',  seller_id=seller_id))

	return render_template('seller_public_profile.html', 
													 cuser=userinfo, info = userinfo, 
													 top_upvotes = top_upvotes, 
													 most_recent = most_recent, 
													 avg = average_rating, 
													 count = review_count)


@bp.route('/seller/account/my-messages', methods=['GET', 'POST'])
def my_messages():
	msg = "Hello world!"
	return render_template('seller_my_messages.html', info = msg)

from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FormField, FieldList, IntegerField, BooleanField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from datetime import datetime
from flask import Blueprint
bp = Blueprint('seller', __name__)

from .models.user import User
from .models.inventory import Inventory
from .models.seller_order import SellerOrder


@bp.route('/seller/account')
def seller_portal():
	if current_user.is_authenticated:
		return render_template('seller_portal.html')
	else:
		return redirect(url_for('index.index'))


@bp.route('/seller/account/my-profile') # can directly copy from Mae's part
def my_profile():
	userinfo = User.get(current_user.id)
	return render_template('seller_my_profile.html', info = userinfo)


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
	submit = SubmitField('Add Item')

@bp.route('/seller/account/my-inventory', methods=['GET', 'POST'])
def my_inventory():
	inventory = Inventory.get(current_user.id)	
	return render_template('seller_my_inventory.html', inventory = inventory)

# add product
@bp.route('/seller/account/my-inventory/add_product', methods=['GET', 'POST'])
def my_inventory_add_product():
	form = ItemForm()
	if form.validate_on_submit():
		Inventory.add_product(current_user.id, form.name.data, form.price.data, form.quantity.data, form.available.data)
		return redirect(url_for('seller.my_inventory'))
	return render_template('seller_add_product.html', form=form)

# edit inventory
class InventoryUpdateForm(FlaskForm):
	price = StringField('New Price')
	submit = SubmitField('Update Price')	
	quantity = StringField('New Quantity')
	available = BooleanField('Available')
	submit = SubmitField('Update Availability')	

@bp.route('/seller/account/my-inventory/update/<pid>', methods=['GET', 'POST'])
def update_inventory(pid):
	inventory = Inventory.get_product(pid, current_user.id)
	form = InventoryUpdateForm()
	if form.validate_on_submit():
		Inventory.update(pid, current_user.id, form.price.data,form.quantity.data,form.available.data)
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
	trendy_products = Purchase.get_trendy_prod(current_user.id)
	return render_template('seller_analytics.html', products = products, trendy_products = trendy_products)




### order fulfillment
# display order details
@bp.route('/seller/account/my-orders', methods=['GET', 'POST'])
def my_orders():
	orders = SellerOrder.get(current_user.id)
	return render_template('seller_my_orders.html', orders = orders)





# edit fake order info [can be deleted later]
class OrderForm(FlaskForm):
	uid = StringField('Buyer ID', validators=[DataRequired()])
	pid = StringField('Product ID', validators=[DataRequired()])
	price = StringField('Price', validators=[DataRequired()])
	quantity = StringField('Quantity', validators=[DataRequired()])
	submit = SubmitField('Add Fake Order')

@bp.route('/seller/account/my-orders/fake_order', methods=['GET', 'POST'])
def add_fake_order():
	form = OrderForm()
	if form.validate_on_submit():
		Fulfillment.fake_order(form.uid.data, form.pid.data, form.price.data, form.quantity.data)
		return redirect(url_for('seller.my_orders'))
	return render_template('seller_fake_order.html', form=form)

# update fulillment status
class FulfillmentForm(FlaskForm):
	fulfillment = BooleanField('Order Completed?')
	submit = SubmitField('Submit')	

@bp.route('/seller/account/my-orders/order_fulfill/<order_id>', methods=['GET', 'POST'])
def order_fulfill(order_id):
	order = Fulfillment.get_order(order_id, current_user.id)
	form = FulfillmentForm()
	if form.validate_on_submit():
		Fulfillment.update(order_id,form.fulfillment.data)
		return redirect(url_for('seller.my_orders'))
	return render_template('seller_update_fulfillment.html', order=order, form=form)	

@bp.route('/seller/account/my-orders/summary', methods=['GET', 'POST'])
def order_summary():
	num_fulfillment = Fulfillment.count_fulfill(current_user.id)
	meanrev = Fulfillment.meanrev(current_user.id)
	return render_template('seller_fulfillment_summary.html', num_fulfillment = num_fulfillment, meanrev = meanrev)
############### code ends #############
@bp.route('/seller/account/my-reviews', methods=['GET', 'POST'])
def my_reviews():
	msg = "Hello world!"
	return render_template('seller_my_reviews.html', info = msg)


@bp.route('/seller/account/my-messages', methods=['GET', 'POST'])
def my_messages():
	msg = "Hello world!"
	return render_template('seller_my_messages.html', info = msg)
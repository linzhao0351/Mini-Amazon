
import os
import csv
import datetime
import random

from werkzeug.security import generate_password_hash

from faker import Faker
from config import fake


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')


def gen_users(num_users):
    with open(os.path.join(os.getcwd(), 'generated', 'Users.csv'), 'w') as f:
        writer = get_csv_writer(f)
        print('Generating Users...\n', end=' ', flush=True)
        
        data = []
        accounts = []
        for id in range(num_users):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            
            profile = fake.profile()
            
            email0 = profile['mail'] # fix repetitive issue
            email = f'n{id}_{email0}'
            plain_password = f'pass{id}'
            password = generate_password_hash(plain_password) #check_password_hash(password, plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            nickname = profile['username']
            address = fake.address()
            
            writer.writerow([id, email, password, firstname, lastname, nickname, address])
            data.append([id, email, password, firstname, lastname, nickname, address])
            
            accounts.append([email, plain_password])

        print(f'{num_users} generated \n')
    
    with open(os.path.join(os.getcwd(), 'generated', 'Accounts.csv'), 'w') as f:
        writer = get_csv_writer(f)
        for item in accounts:
            writer.writerow(item)

    return data


def gen_product_type():
    with open(os.path.join(os.getcwd(), 'generated', 'Product_type.csv'), 'w') as f:
        print('Product types...\n', end=' ', flush=True)
        writer = get_csv_writer(f)
        
        writer.writerow([0, "All"])
        writer.writerow([1, "Food"])
        writer.writerow([0, "Digital"])
    
    return 0
    

def gen_products(num_products, num_users):
    available_pids = []
    data = []
    with open(os.path.join(os.getcwd(), 'generated', 'Products.csv'), 'w') as f:
        writer = get_csv_writer(f)
        print('Products...\n', end=' ', flush=True)
        for product_id in range(num_products):
            if product_id % 100 == 0:
                print(f'{product_id}', end=' ', flush=True)
            seller_id = fake.random_int(min=0, max=num_users-1)
            type_id = fake.random_int(min=0, max=2)
            if type_id == 1:
                name = fake.food()
                short_desc = fake.food_adj()
                long_desc = f'{short_desc} {name}'
            elif type_id == 2:
                name = fake.digital()
                short_desc = fake.digital_adj()
                long_desc = f'{short_desc} {name}'
            else:    
                name = 'Type %s %s' % (seller_id, fake.ecommerce_name())
                short_desc = "This is a short description."
                long_desc = name + " is a very great good. Buy it!"
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            units_avail = f'{str(fake.random_int(min=1, max=9999))}'
            available = fake.random_element(elements=('true', 'false'))
            if available == 'true':
                available_pids.append(product_id)
            writer.writerow([product_id, seller_id, name, price, units_avail, available,short_desc, long_desc, type_id])
            data.append([product_id, seller_id, name, price, units_avail, available,short_desc, long_desc, type_id])
        
        print(f'{num_products} generated; {len(available_pids)} available \n')
    
    return data


def gen_orders(products, users):
    available_products = [item for item in products if item[5] == 'true']
    
    orders = []
    summary = []
    
    messages = []

    with open(os.path.join(os.getcwd(), 'generated', 'Orders.csv'), 'w') as f:
        writer = get_csv_writer(f)
        print('Orders...', end=' ', flush=True)
        
        order_id = 0
        for user in users:
            buyer_id = user[0]
            items = random.sample(available_products, fake.random_int(min=1, max=5))
            
            total_amount = 0
            ts = datetime.datetime.combine(fake.date_object(), fake.time_object())
            order_status = 0

            for item in items:
                product_id = item[0]
                seller_id = item[1]
                price = item[3]
                quantity = f'{fake.random_int(min=1, max=10)}'  
                fulfillment_status = f'{fake.random_int(min=0, max=1)}'
                
                writer.writerow([order_id, product_id, seller_id, quantity, price, fulfillment_status])
                orders.append([order_id, product_id, seller_id, quantity, price, fulfillment_status])                
                
                total_amount += float(price) * float(quantity)
                order_status += int(fulfillment_status)

                messages.append([seller_id, 'You have a new order! Order ID: %s' % order_id, ts])
           
            order_status = order_status == len(items)
            
            summary.append([order_id, buyer_id, ts, total_amount, int(order_status)])
            
            order_id += 1

        print(' generated \n')
        
    with open(os.path.join(os.getcwd(), 'generated', 'Orders_summary.csv'), 'w') as f:
        writer = get_csv_writer(f)
        print('Orders_summary...', end=' ', flush=True)
        for order in summary:
            writer.writerow(order)
        
        print(' generated \n')
 
    with open(os.path.join(os.getcwd(), 'generated', 'System_messages.csv'), 'w') as f:
        writer = get_csv_writer(f)
        print('System_messages...', end=' ', flush=True)
        for msg in messages:
            writer.writerow(msg)
        
        print(' generated \n')


    return orders, summary



def gen_views(num_views, num_users, products):
    available_pids = [item[0] for item in products if item[5] == 'true']
    with open(os.path.join(os.getcwd(), 'generated', 'User_browsing_history.csv'), 'w') as f:
        writer = get_csv_writer(f)
        print('User browsing history...\n', end=' ', flush=True)
        for v in range(num_views):
            if v % 100 == 0:
                print(f'{v}', end=' ', flush=True)
            user_id = fake.random_int(min=0, max=num_users-1)
            product_id = fake.random_element(elements=available_pids)
            view_times = fake.random_int(min=0, max=9)
            last_view_ts = fake.date_time()
            writer.writerow([user_id, product_id, view_times, last_view_ts])
        print(f'{num_views} generated \n')
               
    return 0


def gen_balance(num_users, orders, orders_summary):
    orders_dict = {}
    for item in orders:
        order_id = item[0]
        
        if order_id in orders_dict.keys():
            orders_dict[order_id].append(item)
        else:
            orders_dict[order_id] = [item]
    
    orders_summary_dict = {}
    for item in orders_summary:
        order_id = item[0]
        orders_summary_dict[order_id] = item
    
    
    # write records
    balance_dict = {}
    
    count_id = 0
    
    with open(os.path.join(os.getcwd(),'generated', 'Balance.csv'), 'w') as f:
        # Give each user an initial balance
        writer = get_csv_writer(f)
        print('User balance...\n', end=' ', flush=True)
        for user_id in range(num_users):
            if user_id % 100 == 0:
                print(f'{user_id}', end=' ', flush=True)
            trans_id = count_id
            trans_date = fake.date_object()
            trans = f'{str(fake.random_int(min=10000, max=50000))}.{fake.random_int(max=99):02}'
            balance = trans
            trans_ts = datetime.datetime.combine(trans_date, fake.time_object())
            trans_description ='Deposit from bank account'
            writer.writerow([trans_id, trans_date, trans_ts, user_id, trans, trans_description, balance])
            
            balance_dict[user_id] = float(trans)
            count_id += 1
    
        # Write transaction records associated with each orders
        for order_id in orders_summary_dict.keys():
            # buyer
            buyer_id = orders_summary_dict[order_id][1]
            ts = orders_summary_dict[order_id][2]
            total_amount = orders_summary_dict[order_id][3]
            
            trans_id = count_id
            trans_date = ts.date()
            trans = -total_amount
            balance = balance_dict[buyer_id] - float(total_amount)
            trans_ts = datetime.datetime.combine(trans_date, fake.time_object())
            trans_description ='Purchase'
            writer.writerow([trans_id, trans_date, trans_ts, buyer_id, trans, trans_description, balance])        
            
            balance_dict[buyer_id] -= total_amount
            count_id += 1

            # sellers
            for item in orders_dict[order_id]:
                product_id = item[1]
                seller_id = item[2]
                price = item[3]     
                quantity = item[4]
                
                trans_id = count_id
                trans_date = ts.date()
                trans = float(price) * float(quantity)
                balance = balance_dict[buyer_id] + trans
                trans_ts = datetime.datetime.combine(trans_date, fake.time_object())
                trans_description ='Sale of product %s' % product_id
                writer.writerow([trans_id, trans_date, trans_ts, seller_id, trans, trans_description, balance])  
                
                balance_dict[seller_id] += total_amount
                count_id += 1
        
        print(' generated \n')
            
    with open(os.path.join(os.getcwd(), 'generated', 'Current_balance.csv'), 'w') as f:   
        writer = get_csv_writer(f)
        print('Orders summary...', end=' ', flush=True)
        for user_id in balance_dict.keys():
            writer.writerow([user_id, balance_dict[user_id]])
        
        print(' generated \n')
            
    return balance_dict


def gen_reviews(orders, orders_summary):
    orders_dict = {}
    for item in orders:
        order_id = item[0]
        product_id = item[1]
        seller_id = item[2]
        if order_id in orders_dict.keys():
            orders_dict[order_id].append([product_id,seller_id])
        else:
            orders_dict[order_id] = [[product_id, seller_id]]
    
    orders_summary_dict = {}
    for item in orders_summary:
        order_id = item[0]
        buyer_id = item[1]
        orders_summary_dict[order_id] = buyer_id
    
    # seller review
    seller_upvotes = []
    with open(os.path.join(os.getcwd(), 'generated', 'Seller_review.csv'), 'w') as f:
        writer = get_csv_writer(f)
        print('Seller reviews...\n', end=' ', flush=True)
        review_id = 0

        reviewed_seller = {}

        for order_id in orders_summary_dict:
            buyer_id = orders_summary_dict[order_id]
            
            if buyer_id not in reviewed_seller.keys():
                reviewed_seller[buyer_id] = []

            order_info = orders_dict[order_id]
            seller_ids = [item[1] for item in order_info]
            
            for seller_id in seller_ids:
                if seller_id in reviewed_seller[buyer_id]:
                    continue
                else:
                    reviewed_seller[buyer_id].append(seller_id)

                if random.random() < 0.5:
                    review_ts = fake.date_time()
                    review_content = fake.seller_review()
                    upvote = fake.random_int(min=0, max=1)
                    rating = f'{str(fake.random_int(min=0, max=5))}'
                    if review_id % 100 == 0:
                        print(f'{review_id}', end=' ', flush=True)
                    writer.writerow([review_id, review_ts, buyer_id, seller_id, review_content, upvote, rating])
                    review_id = review_id+1
                    
                    if upvote == 1:
                        seller_upvotes.append([buyer_id, review_id])

        print(' generated \n')

    with open(os.path.join(os.getcwd(), 'generated', 'Seller_upvotes.csv'), 'w') as f:
        writer = get_csv_writer(f)
        for item in seller_upvotes:
            writer.writerow(item)
        
    
    # product review
    upvotes = []
    with open(os.path.join(os.getcwd(), 'generated', 'Product_review.csv'), 'w') as f:
        writer = get_csv_writer(f)
        print('Product reviews...\n', end=' ', flush=True)
        review_id = 0

        reviewed_product = {}

        for order_id in orders_summary_dict:
            buyer_id = orders_summary_dict[order_id]
            
            if buyer_id not in reviewed_product.keys():
                reviewed_product[buyer_id] = []

            order_info = orders_dict[order_id]
            product_ids = [item[0] for item in order_info]        
            
            for product_id in product_ids:
                if product_id in reviewed_seller[buyer_id]:
                    continue
                else:
                    reviewed_product[buyer_id].append(product_id)

                if random.random() < 0.5:
                    review_ts = fake.date_time()
                    review_content = fake.product_review()
                    upvote = fake.random_int(min=0, max=1)
                    rating = f'{str(fake.random_int(min=0, max=5))}'
                    if review_id % 100 == 0:
                        print(f'{review_id}', end=' ', flush=True)
                    writer.writerow([review_id, review_ts, buyer_id, product_id, review_content, upvote, rating])
                    review_id = review_id+1
                    
                    if upvote == 1:
                        upvotes.append([buyer_id, review_id])
    
        print(' generated \n')
    
    with open(os.path.join(os.getcwd(), 'generated', 'Upvotes.csv'), 'w') as f:
        writer = get_csv_writer(f)
        for item in seller_upvotes:
            writer.writerow(item)        
                        
                    
    return orders_dict, orders_summary_dict
        


if __name__ == '__main__':
    
    num_users = 100
    num_products = 5000
    num_purchases = 10000
    num_views = 20000


    Faker.seed(0)
    
    users = gen_users(num_users)
    
    products = gen_products(num_products, num_users)
    
    orders, orders_summary = gen_orders(products, users)
    
    gen_reviews(orders, orders_summary)
      
    gen_views(num_views, num_users, products)
    
    gen_balance(num_users, orders, orders_summary)


    
    
    
    
    
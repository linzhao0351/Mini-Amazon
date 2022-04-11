from werkzeug.security import generate_password_hash
import csv
from faker import Faker

num_users = 100
num_products = 2000
num_purchases = 2500

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')


def gen_users(num_users):
    with open('Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
            plain_password = f'pass{uid}'
            password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            writer.writerow([uid, email, password, firstname, lastname])
        print(f'{num_users} generated')
    return num_users

#### changes start here
def gen_purchases(num_purchases, available_pids):
    with open('Purchases.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for id in range(num_purchases):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_element(elements=available_pids)
            #add fake price and quantity
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            quantity = f'{str(fake.random_int(min=1, max=9999))}'
            time_purchased = fake.date_time()
            fulfillment = 'false'
            writer.writerow([id, uid, pid, price, quantity, time_purchased, fulfillment])
        print(f'{num_purchases} generated')
    return


# edit later to generate name and category
def gen_products(num_products, num_users):
    available_pids = []
    with open('Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for pid in range(num_products):
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            name = fake.sentence(nb_words=4)[:-1]
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            available = fake.random_element(elements=('true', 'false'))
            if available == 'true':
                available_pids.append(pid)
                quantity = f'{str(fake.random_int(min=1, max=9999))}'
            else:
                quantity = f'{str(0)}'   
            writer.writerow([pid, uid, name, price, quantity, available])
        print(f'{num_products} generated; {len(available_pids)} available')
    return available_pids

gen_users(num_users)
available_pids = gen_products(num_products, num_users)
gen_purchases(num_purchases, available_pids)

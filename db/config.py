
import os
import csv, codecs

from faker import Faker
from faker.providers import DynamicProvider
import faker_commerce

def readcsv(csvfile):
    data = []
    with codecs.open(csvfile, 'r', 
                     encoding='utf-8', 
                     errors='ignore') as fdata:
        csv_f = csv.reader(fdata)
        for row in csv_f:
            data.append(row)
        
    return data 


def make_fake(digital_provider, digital_adj_provider,
               food_provider, food_adj_provider, 
               product_review_provider, seller_review_provider ):
     fake = Faker()
     fake.add_provider(faker_commerce.Provider)
     fake.add_provider(digital_provider)
     fake.add_provider(digital_adj_provider)
     fake.add_provider(food_provider)
     fake.add_provider(food_adj_provider)
     fake.add_provider(product_review_provider)
     fake.add_provider(seller_review_provider)

     return fake


def create_branded_products(brands, products):
    branded_products = [brand + " " + product for brand in brands for product in products]
    return branded_products
    

####### Config data #####
brands = readcsv(os.path.join(os.getcwd(), 'data', 'brands.csv'))
brands = [item[0] for item in brands[1:]]

digital_products = ["iPad", 
                    "MacBook Pro", 
                    "Keyboard", 
                    "iPhone", 
                    "Alienware", 
                    "Nintendo Switch"]

food_products = ["Tuna",
                 "Chicken",
                 "Fish",
                 "Cheese",
                 "Bacon",
                 "Pizza",
                 "Salad",
                 "Sausages",
                 "Chips"]

# Digital products
branded_digital_products = create_branded_products(brands, digital_products)

digital_provider = DynamicProvider(
     provider_name="digital",
     elements=branded_digital_products
)

digital_adj_provider = DynamicProvider(
     provider_name="digital_adj",
     elements=["New",
        "Gently Used",
        "Used",
        "Refurbished"],
)


# Food products
branded_food_products = create_branded_products(brands, food_products)

food_provider = DynamicProvider(
     provider_name="food",
     elements=branded_food_products
)

food_adj_provider = DynamicProvider(
     provider_name="food_adj",
     elements=["Fresh", 
               "Tasty", 
               "Healthy", 
               "Homemade", 
               "Fantastic"],
)

# Reviews
product_review_provider = DynamicProvider(
     provider_name="product_review",
     elements=["Great product", 
               "Good quality", 
               "Fair", 
               "You got what you paid for", 
               "Defective product"],
)

seller_review_provider = DynamicProvider(
     provider_name="seller_review",
     elements=["Friendly", 
               "Quick response", 
               "Nice customer service", 
               "Just okay", 
               "Bad customer service", 
               "Fast shipping"],
)


fake = make_fake(digital_provider, digital_adj_provider,
               food_provider, food_adj_provider, 
               product_review_provider, seller_review_provider)
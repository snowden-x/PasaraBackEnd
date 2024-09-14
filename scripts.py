from backend1.models import Category,Product #Import your Django models here

def process_data():
    categories = [
        Category(name='Food'),
        Category(name='Drinks'),
        Category(name='Packages'),
        Category(Name='Beverages')
        # Add more instances as needed
    ]
    Category.objects.bulk_create(categories)
    print("Added successfully")

process_data()

food_category  = Category.objects.get(id=1)
drink_category = Category.objects.get(id=2)
packages_category = Category.objects.get(id=3)

food_data = [
    Product(name="Margherita Pizza", description="Classic pizza with tomato, mozzarella, and basil.", price=12.99, category=food_category, image_url="http://example.com/margherita.jpg"),
    Product(name="Cheeseburger", description="Juicy beef patty with melted cheese, lettuce, and tomato.", price=9.99, category=food_category, image_url="http://example.com/cheeseburger.jpg"),
    Product(name="Caesar Salad", description="Fresh romaine with Caesar dressing, croutons, and parmesan.", price=8.49, category=food_category, image_url="http://example.com/caesar_salad.jpg"),
    Product(name="Spaghetti Carbonara", description="Pasta with creamy egg and cheese sauce, pancetta, and black pepper.", price=14.99, category=food_category, image_url="http://example.com/spaghetti_carbonara.jpg"),
    Product(name="Chicken Tacos", description="Soft tacos filled with seasoned chicken, lettuce, and salsa.", price=10.99, category=food_category, image_url="http://example.com/chicken_tacos.jpg")
]

drink_data = [
    Product(name="Coca-Cola", description="Classic cola drink.", price=1.99, category=drink_category, image_url="http://example.com/coca_cola.jpg"),
    Product(name="Orange Juice", description="Freshly squeezed orange juice.", price=3.49, category=drink_category, image_url="http://example.com/orange_juice.jpg"),
    Product(name="Iced Tea", description="Refreshing iced tea with lemon.", price=2.49, category=drink_category, image_url="http://example.com/iced_tea.jpg"),
    Product(name="Espresso", description="Strong Italian coffee.", price=2.99, category=drink_category, image_url="http://example.com/espresso.jpg"),


]

packages_data = [
    Product(name="Family Dinner Pack", description="A dinner package including pizza, salad, and drinks.", price=39.99, category=packages_category, image_url="http://example.com/family_dinner_pack.jpg"),
    Product(name="Party Pack", description="Includes assorted snacks, drinks, and finger foods.", price=49.99, category=packages_category, image_url="http://example.com/party_pack.jpg"),
    Product(name="Lunch Special", description="A lunch package with a sandwich, chips, and a drink.", price=12.99, category=packages_category, image_url="http://example.com/lunch_special.jpg"),
    Product(name="Healthy Choice Pack", description="Includes a salad, fruit, and a smoothie.", price=22.99, category=packages_category, image_url="http://example.com/healthy_choice_pack.jpg"),
    Product(name="BBQ Kit", description="Everything you need for a BBQ including meat, buns, and condiments.", price=59.99, category=packages_category, image_url="http://example.com/bbq_kit.jpg")
]

# Bulk create products
Product.objects.bulk_create(food_data)
Product.objects.bulk_create(drink_data)
Product.objects.bulk_create(packages_data)

#exec(open('scripts.py').read())

"""
#if selectedCategory not in self.__class__.menu_content_box:
                 #   products = Product.objects.filter(category_id=self.content['selectedCategory']).values('name','description','price','image_url','id')
                  #  product_details = {product['id']:
                   ###       "description": product['description'],
                      #      "price": product['price'],
                       ##    "id": product['id']
                        #}
                        #for product in products
                    #}

                    menu_content_box[selectedCategory] = product_details
                    print(addItem)

                encoding_addItem = {
                    addItem['id']:
                        {
                            "name": addItem['name'],
                            "description": addItem['description'],
                            "price":addItem['price'],
                            "image_url":addItem['image_url']
                        }
                }



"""
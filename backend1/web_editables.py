food_items = [
    {
        "Name": " Kose",
        "Image": "kose.jpg",
        'Description':'Tasty with a slice of Peanut',
        'Price': 34
    },
    {
        "Name":"Jollof",
        "Image":"jollof.jpg",
'Description':'Tasty with a slice of Peanut',
        'Price': 34
    },
    {
        "Name":"Indomie",
        "Image":"indomie.jpg",
'Description':'Tasty with a slice of Peanut',
        'Price': 34
    },
    {
        "Name":"Kyerewa",
        "Image":"kyerewa.jpg",
'Description':'Tasty with a slice of Peanut',
        'Price': 34
    },
    {
        "Name":"Kyerewa",
        "Image":"kyerewa.jpg",
'Description':'Tasty with a slice of Peanut',
        'Price': 34
    },
    {
        "Name":"Kyerewa",
        "Image":"kyerewa.jpg",
'Description':'Tasty with a slice of Peanut',
        'Price': 34
    },
    {
        "Name":"Kyerewa",
        "Image":"kyerewa.jpg",
'Description':'Tasty with a slice of Peanut',
        'Price': 34
    }
]

drink_items = [
    {
        "Name":'Sobolo',
        "Image":'sobolo.jpg',
'Description':'Tasty with a slice of Peanut',
        'Price': 34
    },
    {
        "Name":"Coke",
        "Image":"coke.jpg",
'Description':'Tasty with a slice of Peanut',
        'Price': 34
    },
    {
        "Name":"Fanta",
        "Image":"fanta.jpg",
'Description':'Tasty with a slice of Peanut',
        'Price': 34
    },
    {
        "Name":"Mosaic",
        "Image":"mosaic.jpg",
'Description':'Tasty with a slice of Peanut',
        'Price': 34
    }
]

packages_items = [
    {
        "Name":'Full Package',
        "Image":'waakye.jpg',
'Description':'Tasty with a slice of Peanut',
        'Price': 34
    },
    {
        "Name":"True Package",
        "Image":"jollof.jpg",
'Description':'Tasty with a slice of Peanut',
        'Price': 34
    },
    {
        "Name":"Indomie",
        "Image":"indomie.jpg",
'Description':'Tasty with a slice of Peanut',
        'Price': 34
    },
    {
        "Name":"Kyerewa",
        "Image":"kyerewa.jpg",
'Description':'Tasty with a slice of Peanut',
        'Price': 34
    },
    {
        "Name":"Kyerewa",
        "Image":"kyerewa.jpg",
'Description':'Tasty with a slice of Peanut',
        'Price': 34
    },
    {
        "Name":"Kyerewa",
        "Image":"kyerewa.jpg",
'Description':'Tasty with a slice of Peanut',
        'Price': 34
    },
    {
        "Name":"Kyerewa",
        "Image":"kyerewa.jpg",
'Description':'Tasty with a slice of Peanut',
        'Price': 34
    }
]

Indexer_of_Food_Menu = {
    0: {"Category": "Food", "Menu_Content": food_items},
    1: {"Category": "Drinks", "Menu_Content": drink_items},
    2: {"Category": "All" , "Menu_Content": food_items + drink_items}
}


def send_categories(indexer_of_food_menu):
    return [indexer_of_food_menu[item]["Category"] for item in indexer_of_food_menu]


def create_current_food_items_in_display(index, indexer_of_food_menu):
    return indexer_of_food_menu[index]['Menu_Content']


def delete_item(indexer_of_food_menu,category,index):
    return [indexer_of_food_menu[index]['Menu_Content'].pop(category)]
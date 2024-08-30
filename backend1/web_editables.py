food_items = [
    {
        "Food":'Waakye',
        "Image":'waakye.jpg'
    },
    {
        "Food":"Jollof",
        "Image":"jollof.jpg",
    },
    {
        "Food":"Indomie",
        "Image":"indomie.jpg"
    },
    {
        "Food":"Kyerewa",
        "Image":"kyerewa.jpg"
    },
    {
        "Food":"Kyerewa",
        "Image":"kyerewa.jpg"
    },
    {
        "Food":"Kyerewa",
        "Image":"kyerewa.jpg"
    },
    {
        "Food":"Kyerewa",
        "Image":"kyerewa.jpg"
    }
]

drink_items = [
    {
        "Food":'Sobolo',
        "Image":'sobolo.jpg'
    },
    {
        "Food":"Coke",
        "Image":"coke.jpg",
    },
    {
        "Food":"Fanta",
        "Image":"fanta.jpg"
    },
    {
        "Food":"Mosaic",
        "Image":"mosaic.jpg"
    }
]

packages_items = [
    {
        "Food":'Full Package',
        "Image":'waakye.jpg'
    },
    {
        "Food":"True Package",
        "Image":"jollof.jpg",
    },
    {
        "Food":"Indomie",
        "Image":"indomie.jpg"
    },
    {
        "Food":"Kyerewa",
        "Image":"kyerewa.jpg"
    },
    {
        "Food":"Kyerewa",
        "Image":"kyerewa.jpg"
    },
    {
        "Food":"Kyerewa",
        "Image":"kyerewa.jpg"
    },
    {
        "Food":"Kyerewa",
        "Image":"kyerewa.jpg"
    }
]

Indexer_of_Food_Menu = {
    0: {"Menu_Name": "Food", "Menu_Content": food_items},
    1: {"Menu_Name": "Drinks", "Menu_Content": drink_items}
}


def create_horizontal_list(indexer_of_food_menu):
    return [indexer_of_food_menu[item]["Menu_Name"] for item in indexer_of_food_menu]


def create_current_food_items_in_display(index, indexer_of_food_menu):
    return indexer_of_food_menu[index]['Menu_Content']




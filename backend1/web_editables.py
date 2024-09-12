from backend1.models import Category,Product
from functools import partial

class Editables:
    categories = []
    menu_content_box = {}
    commands_to_go_live = []

    def __init__(self, data):

        self.action = data.get('action', None)
        self.content = data.get('content', None)

    

    def process_request(self):
        match self.action:
            case 'get_category':
                #checks category for updates
                if not self.__class__.categories:
                    # fetch from data base
                    self.__class__.categories = Category.objects.values('name')
                    #print(self.__class__.categories)
                return [food_category['name'] for food_category in  list(self.__class__.categories)]

            case 'get_menu_contents':
                menu_content = []
                selectedCategory = self.content['selectedCategory']


                if selectedCategory in self.__class__.menu_content_box:
                    print("retrieved from here")
                    for id_,content in self.__class__.menu_content_box[selectedCategory].items():
                        menu_content.append(content)
                    return menu_content

                else:
                    products = Product.objects.filter(category_id = self.content['selectedCategory']).values('name','description','price','image_url','id')

                    product_details = {product['id']:
                                           {
                                               "name":product['name'],
                                               "description":product['description'],
                                               "price": product['price'],
                                               "image_url": product['image_url'],
                                               "id":product['id']
                                           }
                                       for product in products
                                       }
                    print(self.__class__.menu_content_box)
                    self.__class__.menu_content_box[selectedCategory]= product_details
                    for id_,content in self.__class__.menu_content_box[selectedCategory].items():
                        menu_content.append(content)
                    return menu_content

            case 'delete_menu_content':
                menu_content = []
                item_id = self.content['item_id']
                selectedCategory = self.content['selectedCategory']
                menu_content_box = self.__class__.menu_content_box

                del menu_content_box[selectedCategory][item_id]

                #for db
                self.__class__.commands_to_go_live.append(partial(self.crud_delete, item_id))

                for id_, content in self.__class__.menu_content_box[selectedCategory].items():
                    menu_content.append(content)
                return menu_content


            case 'edit_item':
                menu_content = []
                selectedCategory = self.content['selectedCategory']
                editedItem = self.content['editedItem']
                menu_content_box = self.__class__.menu_content_box
                id_ = editedItem['id']

                print(menu_content_box)
                menu_content_box[selectedCategory][id_] = editedItem



                #for db
                self.__class__.commands_to_go_live.append(partial(self.crud_edit
                                                          ,selectedCategory=selectedCategory,
                                                                  item_id=id_,editedItem=editedItem))

                for id_, content in self.__class__.menu_content_box[selectedCategory].items():
                    menu_content.append(content)
                return menu_content

            case 'add_item':
                selectedCategory = self.content['selectedCategory']
                addItem = self.content['addItem']
                menu_content_box = self.__class__.menu_content_box



                menu_content_box[selectedCategory][addItem['id']] = addItem

                #for db
                self.__class__.commands_to_go_live.insert(0,partial(self.crud_add,selectedCategory=selectedCategory,
                                                                  addItem=addItem))

                return {'selectedCategory':"Content Added Successfully"}

            case 'apply_changes':
                print("lets go")
                for command in self.__class__.commands_to_go_live:
                    command()
                self.__class__.commands_to_go_live.clear()
                return {'reply':'db_command'}

    @staticmethod
    def crud_delete(item_id):
        Product.objects.get(id=item_id).delete()

    @staticmethod
    def crud_edit(selectedCategory,item_id,editedItem):
        print("I am runing")
        item_to_edit = Product.objects.get(id=item_id)
        print('This is the edited Item',item_to_edit)
        item_to_edit.name = editedItem['name']
        item_to_edit.description = editedItem['description']
        item_to_edit.price = editedItem['price']
        item_to_edit.image_url = editedItem['image_url']
        print("vrrom")
        item_to_edit.save()

    @staticmethod
    def crud_add(selectedCategory,addItem):
        name = addItem['name']
        description = addItem['description']
        price = addItem['price']
        category = Category.objects.get(id=selectedCategory)
        image_url = addItem['image_url']

        new_product = Product(name= name, description=description, price=price, category=category, image_url=image_url)
        new_product.save()


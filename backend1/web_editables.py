from backend1.models import Category,Product
import json
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
                    print(self.__class__.categories)
                return [food_category['name'] for food_category in  list(self.__class__.categories)]

            case 'get_menu_contents':
                selectedCategory = self.content['selectedCategory']

                if selectedCategory in self.__class__.menu_content_box:
                    print('retrieved from here')
                    return list(self.__class__.menu_content_box[selectedCategory])
                else:
                    menu_content = Product.objects.filter(category_id = self.content['selectedCategory']).values('name','description','price','image_url','id')
                    self.__class__.menu_content_box[selectedCategory] = menu_content
                    print(self.__class__.menu_content_box)
                    return list(menu_content)

            case 'delete_menu_content':
                index = self.content['index']
                selectedCategory = self.content['selectedCategory']
                menu_content_box = self.__class__.menu_content_box

                menu_content = list(menu_content_box[selectedCategory])
                menu_content.pop(index)
                menu_content_box[selectedCategory] = menu_content


                return menu_content

            case 'edit_item':
                index = self.content['index']
                selectedCategory = self.content['selectedCategory']
                menu_content_box = self.__class__.menu_content_box

                menu_content = list(menu_content_box[selectedCategory])
                menu_content[index] = self.content['editedItem']
                menu_content_box[selectedCategory] = menu_content
                return menu_content

            case 'add_item':
                selectedCategory = self.content['selectedCategory']
                menu_content_box = self.__class__.menu_content_box

                if selectedCategory not in self.__class__.menu_content_box:
                    menu_content = Product.objects.filter(category_id=selectedCategory).values('name','description','price','image_url','id')
                    menu_content_box[selectedCategory] = menu_content

                menu_content = list(menu_content_box[selectedCategory])
                menu_content.insert(0,self.content['addItem'])
                menu_content_box[selectedCategory] = menu_content
                return {'selectedCategory':selectedCategory,'menuContent':menu_content}


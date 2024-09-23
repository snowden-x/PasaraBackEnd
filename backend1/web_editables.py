from backend1.models import Category, Product, CustomizationCategory, CustomizationOption, ProductCustomization, Cart, CartItem, CartItemCustomization, User
from functools import partial
import json
from decimal import Decimal


class Editables:
    categories = []
    menu_content_box = {}
    commands_to_go_live = []
    cart = None

    def __init__(self, data):
        self.action = data.get('action', None)
        self.content = data.get('content', None)

    def process_request(self):
        match self.action:
            case 'get_category':
                return self.get_categories()
            case 'get_all_menu_contents':
                return self.get_all_menu_contents()
            case 'get_menu_contents':
                return self.get_menu_contents()
            case 'delete_menu_content':
                return self.delete_menu_content()
            case 'edit_item':
                return self.edit_item()
            case 'add_item':
                return self.add_item()
            case 'is_available':
                return self.toggle_availability()
            case 'apply_changes':
                return self.apply_changes()
            case 'add_to_cart':
                return self.add_to_cart()
            case 'update_cart_item':
                return self.update_cart_item()
            case 'remove_from_cart':
                return self.remove_from_cart()
            case 'get_cart':
                return self.get_cart()
            case 'clear_cart':
                return self.clear_cart()
            case 'checkout':
                return self.checkout()

    def get_categories(self):
        if not self.__class__.categories:
            self.__class__.categories = Category.objects.values('id', 'name')
        return [{'id': category['id'], 'name': category['name']} for category in self.__class__.categories]

    def get_all_menu_contents(self):
        all_menu_content = []
        if self.__class__.menu_content_box:
            for category, items in self.__class__.menu_content_box.items():
                all_menu_content.extend(items.values())
        else:
            products = Product.objects.prefetch_related('customizations__customization_category',
                                                        'customizations__default_option').all()
            for product in products:
                category = product.category.name
                item = self._format_product(product)
                all_menu_content.append(item)
                if category not in self.__class__.menu_content_box:
                    self.__class__.menu_content_box[category] = {}
                self.__class__.menu_content_box[category][product.id] = item
        return all_menu_content

    def get_menu_contents(self):
        selected_category = self.content['selectedCategory']
        if selected_category in self.__class__.menu_content_box:
            return list(self.__class__.menu_content_box[selected_category].values())
        else:
            products = Product.objects.filter(category__name=selected_category).prefetch_related(
                'customizations__customization_category', 'customizations__default_option')
            menu_content = []
            for product in products:
                item = self._format_product(product)
                menu_content.append(item)
                if selected_category not in self.__class__.menu_content_box:
                    self.__class__.menu_content_box[selected_category] = {}
                self.__class__.menu_content_box[selected_category][product.id] = item
            return menu_content

    def delete_menu_content(self):
        item_id = self.content['item_id']
        selected_category = self.content['selectedCategory']
        del self.__class__.menu_content_box[selected_category][item_id]
        self.__class__.commands_to_go_live.append(partial(self.crud_delete, item_id))
        return list(self.__class__.menu_content_box[selected_category].values())

    def edit_item(self):
        selected_category = self.content['selectedCategory']
        edited_item = self.content['editedItem']
        id_ = edited_item['id']
        self.__class__.menu_content_box[selected_category][id_] = edited_item
        self.__class__.commands_to_go_live.append(partial(self.crud_edit, item_id=id_, edited_item=edited_item))
        return list(self.__class__.menu_content_box[selected_category].values())

    def add_item(self):
        selected_category = self.content['selectedCategory']
        add_item = self.content['addItem']
        self.__class__.menu_content_box[selected_category][add_item['id']] = add_item
        self.__class__.commands_to_go_live.insert(0, partial(self.crud_add, selected_category=selected_category,
                                                             add_item=add_item))
        return {'message': "Content Added Successfully"}

    def toggle_availability(self):
        selected_category = self.content['selectedCategory']
        item_to_edit_availability = self.content['item']
        item_id = item_to_edit_availability['id']
        current_state = item_to_edit_availability['is_available']
        self.__class__.menu_content_box[selected_category][item_id]['is_available'] = not current_state
        self.__class__.commands_to_go_live.append(
            partial(self.crud_available, item_id=item_id, state=not current_state))
        return list(self.__class__.menu_content_box[selected_category].values())

    def apply_changes(self):
        for command in self.__class__.commands_to_go_live:
            command()
        self.__class__.commands_to_go_live.clear()
        self.__class__.categories = []
        self.__class__.menu_content_box = {}
        return {'reply': 'db_command'}

    def add_to_cart(self):
        product_id = self.content['product_id']
        quantity = self.content['quantity']
        customizations = self.content['customizations']
        user_id = self.content.get('user_id', None)

        product = Product.objects.get(id=product_id)
        if user_id:
            user = User.objects.get(id=user_id)
            cart, _ = Cart.objects.get_or_create(user=user)
        else:
            if not self.__class__.cart:
                self.__class__.cart, _ = Cart.objects.get_or_create(id=1)
            cart = self.__class__.cart

        base_price = product.price
        total_price = base_price * Decimal(quantity)

        cart_item = CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=quantity,
            total_price=total_price
        )

        for customization in customizations:
            category = CustomizationCategory.objects.get(name=customization['category'])
            option = CustomizationOption.objects.get(category=category, name=customization['option_id'])
            CartItemCustomization.objects.create(
                cart_item=cart_item,
                customization_option=option
            )
            total_price += option.price_adjustment * Decimal(quantity)

        cart_item.total_price = total_price
        cart_item.save()

        return self._format_cart_item(cart_item)

    def update_cart_item(self):
        cart_item_id = self.content['cart_item_id']
        new_quantity = self.content['quantity']

        cart_item = CartItem.objects.get(id=cart_item_id)
        cart_item.quantity = new_quantity
        cart_item.total_price = cart_item.product.price * Decimal(new_quantity)

        for customization in cart_item.customizations.all():
            cart_item.total_price += customization.customization_option.price_adjustment * Decimal(new_quantity)

        cart_item.save()

        return self._format_cart_item(cart_item)

    def remove_from_cart(self):
        cart_item_id = self.content['cart_item_id']
        CartItem.objects.filter(id=cart_item_id).delete()
        return {'message': 'Item removed from cart'}

    def get_cart(self):
        if not self.__class__.cart:
            self.__class__.cart, _ = Cart.objects.get_or_create(id=1)
        cart_items = CartItem.objects.filter(cart=self.__class__.cart)
        return [self._format_cart_item(item) for item in cart_items]

    def clear_cart(self):
        if self.__class__.cart:
            self.__class__.cart.items.all().delete()
        return {'message': 'Cart cleared'}

    def checkout(self):
        if self.__class__.cart:
            # Here you would implement the actual checkout process
            # For now, we'll just clear the cart
            self.__class__.cart.items.all().delete()
        return {'message': 'Checkout completed'}

    @staticmethod
    def _format_product(product):
        customizations = {}
        for pc in product.customizations.all():
            options = CustomizationOption.objects.filter(category=pc.customization_category)
            customizations[pc.customization_category.name] = {
                'default': pc.default_option.name if pc.default_option else None,
                'options': [{'name': opt.name, 'price_adjustment': float(opt.price_adjustment)} for opt in options]
            }

        return {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": float(product.price),
            "image": product.image_url,
            "category": product.category.name,
            "customizations": customizations,
            "is_available": product.is_available
        }

    @staticmethod
    def _format_cart_item(cart_item):
        return {
            "id": cart_item.id,
            "product_name": cart_item.product.name,
            "quantity": cart_item.quantity,
            "base_price": float(cart_item.product.price),
            "total_price": float(cart_item.total_price),
            "customizations": [
                {
                    "category": cic.customization_option.category.name,
                    "option": cic.customization_option.name,
                    "price_adjustment": float(cic.customization_option.price_adjustment)
                }
                for cic in cart_item.customizations.all()
            ]
        }

    @staticmethod
    def crud_delete(item_id):
        Product.objects.get(id=item_id).delete()

    @staticmethod
    def crud_edit(item_id, edited_item):
        item_to_edit = Product.objects.get(id=item_id)
        item_to_edit.name = edited_item['name']
        item_to_edit.description = edited_item['description']
        item_to_edit.price = edited_item['price']
        item_to_edit.image_url = edited_item['image']
        item_to_edit.is_available = edited_item['is_available']
        item_to_edit.save()

        # Update customizations
        for cat_name, cat_data in edited_item['customizations'].items():
            cat, _ = CustomizationCategory.objects.get_or_create(name=cat_name)
            pc, _ = ProductCustomization.objects.get_or_create(product=item_to_edit, customization_category=cat)

            default_option = None
            for opt_data in cat_data['options']:
                option, _ = CustomizationOption.objects.get_or_create(
                    category=cat,
                    name=opt_data['name'],
                    defaults={'price_adjustment': opt_data['price_adjustment']}
                )
                if opt_data['name'] == cat_data['default']:
                    default_option = option

            pc.default_option = default_option
            pc.save()

    @staticmethod
    def crud_available(item_id, state):
        item_to_edit = Product.objects.get(id=item_id)
        item_to_edit.is_available = state
        item_to_edit.save()

    @staticmethod
    def crud_add(selected_category, add_item):
        category = Category.objects.get(id=selected_category)
        new_product = Product(
            name=add_item['name'],
            description=add_item['description'],
            price=add_item['price'],
            category=category,
            image_url=add_item['image'],
            is_available=add_item['is_available']
        )
        new_product.save()

        # Add customizations
        for cat_name, cat_data in add_item['customizations'].items():
            cat, _ = CustomizationCategory.objects.get_or_create(name=cat_name)
            pc = ProductCustomization.objects.create(product=new_product, customization_category=cat)

            default_option = None
            for opt_data in cat_data['options']:
                option, _ = CustomizationOption.objects.get_or_create(
                    category=cat,
                    name=opt_data['name'],
                    defaults={'price_adjustment': opt_data['price_adjustment']}
                )
                if opt_data['name'] == cat_data['default']:
                    default_option = option

            pc.default_option = default_option
            pc.save()
class Cart:  # CONSTRUCTOR
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get("cart")
        if not cart:
            cart = self.session["cart"] = {}
        self.cart = cart

    def add(self, product):
        if str(product.id) not in self.cart.keys():
            self.cart[product.id] = {
                "product_id": product.id,
                "name": product.name,
                "quantity": 1,
                "price": str(product.price),
                "image": product.image.url,

            }
        else:
            for key, value in self.cart.items():
                if key == str(product.id):
                    value["quantity"] = value["quantity"] + 1
                    break
        self.save()

    def save(self):
        self.session["cart"] = self.cart
        # Con esto logramos que django persista la informacion cuando una sesion fue actualizada
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]  # del para eliminar
            self.save()  # para perisistir la sesion

    def decrement(self, product):
        for key, value in self.cart.items():
            if key == str(product.id):
                value["quantity"] = value["quantity"] - 1
                if value["quantity"] < 1:
                    self.remove(product)
                else:
                    self.save()
                break
            else:
                print('EL producto no existe en el carrito')

    def clear(self):
        self.session["cart"] = {}
        self.session.modified = True

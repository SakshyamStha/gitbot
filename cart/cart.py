from ecommerce.models import Product

class Cart():

    def __init__(self, request):
        self.session = request.session

        # Get the current session key if it exists
        cart = self.session.get('session_key')

        # If the user is new, no session key. So create one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # Make sure cart is available on all pages of the site
        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        # Logic
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        # Get IDs from cart
        product_ids = self.cart.keys()

        # Use IDs to lookup products in database model
        products = Product.objects.filter(id__in=product_ids)
        return products

    def cart_total(self):
        # Get product ID
        product_ids = self.cart.keys()

        # Lookup those keys in product database model
        products = Product.objects.filter(id__in=product_ids)

        # Get quantities
        quantities = self.cart

        # Start counting at 0
        total = 0
        for key, value in quantities.items():
            key = int(key)  # Convert key string into int
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total += product.sale_price * value
                    else:
                        total += product.price * value

        return total

    def total(self, product_id=None):
   
        quantities = self.cart  # Get quantities for each product
        
        total_sum = 0

        # If a specific product_id is provided, calculate total for that product
        if product_id:
            if str(product_id) in quantities:  # Check if the product is in the cart
                product = Product.objects.get(id=product_id)
                quantity = quantities[str(product_id)]
                if product.is_sale:
                    total_sum = product.sale_price * quantity
                else:
                    total_sum = product.price * quantity
        
        return total_sum



    def get_quants(self):
        quantities = self.cart
        return quantities

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        # Get cart
        ourcart = self.cart

        # Update dictionary/cart
        ourcart[product_id] = product_qty

        self.session.modified = True
        thing = self.cart

        return thing

    def delete(self, product):
        product_id = str(product)

        # Delete from cart
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

    def clear(self):
        """
        Clear all items from the cart and update the session.
        """
        self.cart = {}  # Reset the cart dictionary
        self.session['session_key'] = self.cart  # Update session key to reflect cleared state
        self.session.modified = True

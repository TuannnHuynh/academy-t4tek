from odoo import http
from odoo.http import request

class CartController(http.Controller):

    @http.route('/cart/add', type='json', auth='user', methods=['POST'])
    def add_to_cart(self, product_id, quantity=1):
        user = request.env.user
        Cart = request.env['cart.order']
        CartLine = request.env['cart.order.line']

        # Kiểm tra giỏ hàng của user
        cart = Cart.search([('user_id', '=', user.id)], limit=1)
        if not cart:
            cart = Cart.create({'user_id': user.id})

        # Kiểm tra xem sản phẩm đã có trong giỏ hàng chưa
        line = cart.line_ids.filtered(lambda l: l.product_id.id == product_id)
        if line:
            line.quantity += quantity
        else:
            CartLine.create({
                'cart_id': cart.id,
                'product_id': product_id,
                'quantity': quantity
            })
        return {'status': 'success', 'message': 'Product added to cart'}

    @http.route('/cart/remove', type='json', auth='user', methods=['POST'])
    def remove_from_cart(self, product_id):
        user = request.env.user
        cart = request.env['cart.order'].search([('user_id', '=', user.id)], limit=1)

        if cart:
            line = cart.line_ids.filtered(lambda l: l.product_id.id == product_id)
            if line:
                line.unlink()
                return {'status': 'success', 'message': 'Product removed from cart'}
        
        return {'status': 'error', 'message': 'Product not found in cart'}

    @http.route('/cart/get', type='json', auth='user', methods=['POST', 'GET'])
    def get_cart(self):
        user = request.env.user
        cart = request.env['cart.order'].search([('user_id', '=', user.id)], limit=1)
        if not cart:
            return {'status': 'empty', 'message': 'Cart is empty'}

        data = {
            'cart_id': cart.id,
            'total_price': cart.total_price,
            'total_quantity': cart.total_quantity,
            'items': [{
                'product_id': line.product_id.id,
                'product_name': line.product_id.name,
                'quantity': line.quantity,
                'price_unit': line.price_unit,
                'subtotal': line.subtotal
            } for line in cart.line_ids]
        }
        return data

from odoo import models, fields, api

class CartOrder(models.Model):
    _name = 'cart.order'
    _description = 'Shopping Cart'

    user_id = fields.Many2one('res.users', string="User", required=True, default=lambda self: self.env.user)
    line_ids = fields.One2many('cart.order.line', 'cart_id', string="Cart Lines")
    total_price = fields.Float(string="Total Price", compute="_compute_total_price", store=True)
    total_quantity = fields.Integer(string="Total Quantity", compute="_compute_total_quantity", store=True)

    @api.depends('line_ids.subtotal')
    def _compute_total_price(self):
        for cart in self:
            cart.total_price = sum(cart.line_ids.mapped('subtotal'))

    @api.depends('line_ids.quantity') 
    def _compute_total_quantity(self):
        for cart in self:
            cart.total_quantity = sum(cart.line_ids.mapped('quantity'))

class CartOrderLine(models.Model):
    _name = 'cart.order.line'
    _description = 'Shopping Cart Line'

    cart_id = fields.Many2one('cart.order', string="Cart", required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string="Product", required=True)
    quantity = fields.Integer(string="Quantity", default=1)
    price_unit = fields.Float(string="Unit Price", related='product_id.lst_price', store=True)
    subtotal = fields.Float(string="Subtotal", compute="_compute_subtotal", store=True)

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit

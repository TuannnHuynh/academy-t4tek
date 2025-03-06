from odoo import http
from odoo.http import request
from unidecode import unidecode

class ThemeController(http.Controller):

    def format_currency(self, value):
        """ Định dạng số thành dạng 6,300,000 (dấu phẩy ngăn cách) """
        return "{:,.0f}".format(value)

    @http.route('/', type='http', auth="public", website=True)
    def home_page(self, **kw):
        template_exists = request.env["ir.ui.view"].sudo().search([
            ("key", "=", "theme_elearning.test_page_template")
        ], limit=1)

        if template_exists:
            return request.render("theme_elearning.test_page_template")
        else:
            return request.render("website.layout", {
                "error_message": "Template không tồn tại hoặc theme đã bị thay đổi."
            })

    @http.route('/khoa-hoc-ngan-han', type='http', auth="public", website=True)
    def course_short_page(self, **kw):
        template_exists = request.env["ir.ui.view"].sudo().search([
            ("key", "=", "theme_elearning.course_short")
        ], limit=1)

        if template_exists:
            return request.render("theme_elearning.course_short")
        else:
            return request.render("website.layout", {
                "error_message": "Template không tồn tại hoặc theme đã bị thay đổi."
            })

    def _get_cart(self):
        user = request.env.user
        return request.env['cart.order'].sudo().search([('user_id', '=', user.id)], limit=1)

    @http.route('/thanh-toan', type='http', auth="public", website=True)
    def checkout_page(self, **kw):
        cart = self._get_cart()

        if not cart:
            return request.render("website.layout", {"error_message": "Giỏ hàng trống."})

        # Tính tổng số lượng sản phẩm
        total_quantity = sum(line.quantity for line in cart.line_ids)

        # Tính tổng tiền đơn hàng
        total_price = sum(line.quantity * line.price_unit for line in cart.line_ids)

        # Định dạng số tiền (ví dụ: 6.300.000)
        formatted_total_price = "{:,.0f}".format(total_price).replace(",", ".")

        template_exists = request.env["ir.ui.view"].sudo().search([
            ("key", "=", "theme_elearning.checkout_page_template")
        ], limit=1)

        if template_exists:
            return request.render("theme_elearning.checkout_page_template", {
                'cart': cart.line_ids,
                'total_quantity': total_quantity,
                'total_price': formatted_total_price
            })
        else:
            return request.redirect("/")

    @http.route('/khoa-hoc-ngan-han/<string:slug>', type='http', auth='public', website=True)
    def product_detail(self, slug):
        def create_slug(text):
            return unidecode(text).replace(" ", "-").lower()

        products = request.env['product.template'].sudo().search([])
        product = next((p for p in products if create_slug(p.name) == slug), None)

        if not product:
            return request.render('website.404')

        return request.render('theme_elearning.product_page_template', {
            'product': product
        })

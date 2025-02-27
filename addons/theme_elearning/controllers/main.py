from odoo import http
from odoo.http import request
from unidecode import unidecode

class ThemeController(http.Controller):

    @http.route('/', type='http', auth="public", website=True)
    def home_page(self, **kw):
        # Kiểm tra xem template có tồn tại không
        template_exists = request.env["ir.ui.view"].sudo().search([
            ("key", "=", "theme_elearning.test_page_template")
        ], limit=1)

        if template_exists:
            return request.render("theme_elearning.test_page_template")
        else:
            # Nếu template không tồn tại, hiển thị trang mặc định
            return request.render("website.layout", {
                "error_message": "Template không tồn tại hoặc theme đã bị thay đổi."
            })
        
    @http.route('/khoa-hoc-ngan-han', type='http', auth="public", website=True)
    def course_short_page(self, **kw):
        # Kiểm tra xem template có tồn tại không
        template_exists = request.env["ir.ui.view"].sudo().search([
            ("key", "=", "theme_elearning.course_short")
        ], limit=1)

        if template_exists:
            return request.render("theme_elearning.course_short")
        else:
            # Nếu template không tồn tại, hiển thị trang mặc định
            return request.render("website.layout", {
                "error_message": "Template không tồn tại hoặc theme đã bị thay đổi."
            })
        
    @http.route('/khoa-hoc-ngan-han/<string:slug>', type='http', auth='public', website=True)
    def product_detail(self, slug):
        # Tạo slug không dấu
        def create_slug(text):
            return unidecode(text).replace(" ", "-").lower()

        # Tìm sản phẩm dựa trên slug
        products = request.env['product.template'].sudo().search([])
        product = next((p for p in products if create_slug(p.name) == slug), None)

        if not product:
            return request.render('website.404')  # Trả về trang 404 nếu không tìm thấy sản phẩm
        
        return request.render('theme_elearning.product_page_template', {
            'product': product
        })


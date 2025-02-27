from odoo import http
from odoo.http import request
from unidecode import unidecode 

class ProductController(http.Controller):
    @http.route('/get_products', type='json', auth='public')
    def get_products(self):
        products = request.env['product.template'].sudo().search([], limit=10)
        product_list = [{
            "name": product.name,
            "image": f"/web/image/product.template/{product.id}/image_1024",
            "opening_date": product.opening_date.strftime('%d/%m/%Y') if product.opening_date else '',
            "level": dict(product._fields['level'].selection).get(product.level, ''),
            "study_days": dict(product._fields['study_days'].selection).get(product.study_days, ''),
            "study_time": dict(product._fields['study_time'].selection).get(product.study_time, '')
        } for product in products]

        return product_list
    
    

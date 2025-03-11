from odoo import http
from odoo.http import request

class ProductController(http.Controller):

    @http.route('/get_products', type='json', auth='public', methods=['POST'])
    def get_products(self, location=None, category_name=None):
        """
        Lấy danh sách khóa học danh mục (category).
        """
        domain = [('sale_ok', '=', True)]  # Chỉ lấy sản phẩm có thể bán

        # Lọc theo danh mục (category)
        if category_name and category_name.lower() != "Tất cả khoá học":
            domain.append(('categ_id.name', 'ilike', category_name))

        products = request.env['product.product'].sudo().search(domain, limit=10)

        product_list = []
        for product in products:
            location_value = product.product_template_attribute_value_ids.filtered(
                lambda v: v.attribute_id.name == "Location"
            )
            teacher_value = product.product_template_attribute_value_ids.filtered(
                lambda v: v.attribute_id.name == "Teacher"
            )

            # Chuyển selection thành dictionary trước khi dùng `.get()`
            study_days_selection = dict(product._fields.get('study_days', {})._description_selection(request.env))
            study_time_selection = dict(product._fields.get('study_time', {})._description_selection(request.env))
            level_selection = dict(product._fields.get('level', {})._description_selection(request.env))

            product_list.append({
                "id": product.id,
                "name": product.name,
                "image": f"/web/image/product.product/{product.id}/image_1024" if product.image_1024 else '',
                "opening_date": product.opening_date.strftime('%d/%m/%Y') if product.opening_date else '',
                "level": level_selection.get(product.level, ''),
                "study_days": study_days_selection.get(product.study_days, ''),
                "study_time": study_time_selection.get(product.study_time, ''),
                "location": location_value.name if location_value else '',
                "teacher": teacher_value.name if teacher_value else ''
            })

        return product_list

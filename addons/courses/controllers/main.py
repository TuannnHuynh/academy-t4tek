from odoo import http
from odoo.http import request

class ProductController(http.Controller):

    @http.route('/get_products', type='json', auth='public', methods=['POST'])
    def get_products(self, location=None, category_name=None):
        domain = [('sale_ok', '=', True)]  # Chỉ lấy sản phẩm có thể bán

        # Lọc theo danh mục (category)
        if category_name and category_name.lower() != "tất cả khoá học":
            domain.append(('categ_id.name', 'ilike', category_name))

        # Truy vấn sản phẩm theo template
        products = request.env['product.template'].sudo().search(domain)

        product_list = []
        for product in products:
            # Lấy giá trị của Location và Teacher
            location_values = product.attribute_line_ids.filtered(lambda v: v.attribute_id.name == "Location")
            teacher_values = product.attribute_line_ids.filtered(lambda v: v.attribute_id.name == "Teacher")

            # Nếu sản phẩm không có giáo viên nào thì bỏ qua
            teacher_names = teacher_values.mapped('value_ids.name')
            if not teacher_names:
                continue  

            # Lấy danh sách Location bị loại trừ từ product.template.attribute.exclusion
            excluded_locations = request.env['product.template.attribute.exclusion'].sudo().search([
                ('product_tmpl_id', '=', product.id)
            ]).mapped('value_ids.name')

            # Lọc danh sách Location hợp lệ (không bị exclude)
            valid_locations = [
                loc for loc in location_values.mapped('value_ids.name')
                if loc not in excluded_locations
            ]

            # Nếu chọn một location cụ thể, kiểm tra xem nó có hợp lệ không
            if location and location.lower() != "tất cả địa điểm":
                if location not in valid_locations:
                    continue  # Bỏ qua nếu không hợp lệ

            # Nếu không có Location hợp lệ, bỏ qua sản phẩm
            if not valid_locations:
                continue

            # Thêm sản phẩm vào danh sách kết quả
            product_list.append({
                "id": product.id,
                "name": product.name,
                "image": f"/web/image/product.template/{product.id}/image_1024" if product.image_1024 else '',
                "opening_date": product.opening_date.strftime('%d/%m/%Y') if product.opening_date else '',
                "level": dict(product._fields.get('level', {})._description_selection(request.env)).get(product.level, ''),
                "study_days": dict(product._fields.get('study_days', {})._description_selection(request.env)).get(product.study_days, ''),
                "study_time": dict(product._fields.get('study_time', {})._description_selection(request.env)).get(product.study_time, ''),
                "location": valid_locations,  # Chỉ chứa địa điểm có giáo viên
                "teacher": teacher_names,  # Danh sách giáo viên
                "promotion_text": product.promotion_text
            })

        return product_list

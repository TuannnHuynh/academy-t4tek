from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    opening_date = fields.Date(string="Ngày khai giảng")
    level = fields.Selection(
        [
            ('basic', 'Cơ bản'),
            ('intermediate', 'Cơ bản - Trung cấp'),
            ('advanced', 'Cao cấp')
        ],
        string="Trình độ"
    )
    study_days = fields.Selection(
        [
            ('mon_wed_fri', 'Thứ 2, Thứ 4, Thứ 6'),
            ('tue_thu', 'Thứ 3, Thứ 5'),
            ('weekend', 'Thứ 7, Chủ Nhật')
        ],
        string="Lịch học"
    )
    study_time = fields.Selection(
        [
            ('morning', '08:00 - 11:00'),
            ('afternoon', '13:30 - 16:30'),
            ('evening', '18:30 - 21:00')
        ],
        string="Giờ học"
    )

    duration_sessions = fields.Integer(string="Số buổi học")
    class_name = fields.Char(string="Lớp học")

    promotion_text = fields.Char(string="Ưu đãi")

    def get_promotion_text(self):
        """Lấy nội dung ưu đãi để hiển thị trên giao diện"""
        return self.promotion_text if self.promotion_text else "Ưu đãi đặc biệt!"
    
    def get_variant_locations(self):
        """Lấy danh sách địa điểm từ biến thể sản phẩm"""
        locations = []
        for variant in self.product_variant_ids:
            location_values = variant.product_template_attribute_value_ids.filtered(lambda attr: attr.attribute_id.name == "Location").mapped("name")
            if location_values:
                locations.append(location_values[0])  # Lấy giá trị đầu tiên (nếu có nhiều)
        return list(set(locations))  # Loại bỏ giá trị trùng lặp
    
    def get_teacher_by_location(self, location_name):
        """
        Lấy danh sách giáo viên dựa theo địa điểm từ biến thể sản phẩm.
        """
        self.ensure_one()

        # Tìm biến thể có location đúng
        variant = self.product_variant_ids.filtered(lambda v: 
            location_name in v.product_template_attribute_value_ids.filtered(
                lambda attr: attr.attribute_id.name == "Location"
            ).mapped("name")
        )

        if variant:
            # Lấy danh sách giáo viên từ biến thể này
            teachers = variant.product_template_attribute_value_ids.filtered(
                lambda attr: attr.attribute_id.name == "Teacher"
            ).mapped("name")

            return ", ".join(teachers) if teachers else "Chưa có giáo viên"

        return "Chưa có giáo viên"




    def get_total_price(self):
        return "{:,.0f}".format(self.list_price)

    def get_study_days_label(self):
        """Trả về label của 'study_days' thay vì value"""
        return dict(self._fields['study_days'].selection).get(self.study_days, 'Không xác định')

    def get_level_label(self):
        """Trả về label của 'level'"""
        return dict(self._fields['level'].selection).get(self.level, 'Không xác định')

    def get_study_time_label(self):
        """Trả về label của 'study_time'"""
        return dict(self._fields['study_time'].selection).get(self.study_time, 'Không xác định')
    
    def get_opening_date(self):
        """Trả về ngày khai giảng dưới dạng chuỗi dd/mm/yyyy"""
        return self.opening_date.strftime('%d/%m/%Y') if self.opening_date else "Chưa có thông tin"

    def get_duration_sessions(self):
        """Trả về số buổi học dưới dạng chuỗi"""
        return f"{self.duration_sessions}" if self.duration_sessions else "Chưa có thông tin"

    def get_class_name(self):
        """Trả về tên lớp học"""
        return self.class_name if self.class_name else "Chưa có thông tin"
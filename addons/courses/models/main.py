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

    def get_total_price(self):
        """Lấy giá tiền đã bao gồm thuế"""
        tax_amount = sum(self.taxes_id.mapped('amount')) / 100
        total_price = self.list_price * (1 + tax_amount)
        return "{:,.0f}".format(total_price)


    def get_instructor_name(self):
        """Lấy tên giảng viên từ Tags (product.tag)"""
        return ", ".join(self.product_tag_ids.mapped('name')) if self.product_tag_ids else "Không có giảng viên"


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
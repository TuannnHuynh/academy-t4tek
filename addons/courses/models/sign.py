from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.exceptions import AccessDenied

class ResUsers(models.Model):
    _inherit = 'res.users'

    email = fields.Char(string="Email", required=True)

    @api.model
    def create(self, vals):
        if 'email' in vals:
            email = vals['email']
            if any(c.isupper() for c in email):
                raise ValidationError("Email không được chứa chữ in hoa!")
            vals['email'] = email.lower()  # Chuyển email thành chữ thường
        return super(ResUsers, self).create(vals)

    def write(self, vals):
        if 'email' in vals:
            email = vals['email']
            if any(c.isupper() for c in email):
                raise ValidationError("Email không được chứa chữ in hoa!")
            vals['email'] = email.lower()  # Chuyển email thành chữ thường
        return super(ResUsers, self).write(vals)

    def _check_credentials(self, password, user_agent_env):
        """ Kiểm tra thông tin đăng nhập và chặn email có chữ hoa """
        for user in self:
            if any(c.isupper() for c in user.login):
                raise AccessDenied("Email đăng nhập không được chứa chữ in hoa!")
        return super(ResUsers, self)._check_credentials(password, user_agent_env)
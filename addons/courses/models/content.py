from odoo import models, fields

class ResCompany(models.Model):
    _inherit = "res.company"

    x_banner_title_1 = fields.Char(string="First title")
    x_banner_content_1 = fields.Text(string="First content")
    x_banner_image_1 = fields.Binary(string="First banner")

    x_banner_title_2 = fields.Char(string="Second title")
    x_banner_content_2 = fields.Text(string="Second content")
    x_banner_image_2 = fields.Binary(string="Second banner")

    x_banner_title_3 = fields.Char(string="Third title")
    x_banner_content_3 = fields.Text(string="Third content")
    x_banner_image_3 = fields.Binary(string="Third banner")

    x_banner_title_4 = fields.Char(string="Fourth title")
    x_banner_content_4 = fields.Text(string="Fourth content")
    x_banner_image_4 = fields.Binary(string="Fourth banner")


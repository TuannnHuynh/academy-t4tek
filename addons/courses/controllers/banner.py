from odoo import http
from odoo.http import request

class WebsiteBanner(http.Controller):

    @http.route('/get_banners', type='json', auth='public', website=True)
    def get_banners(self):
        company = request.env.company  # Lấy công ty hiện tại
        banners = [
            {
                'title': company.x_banner_title_1,
                'content': company.x_banner_content_1,
                'image': f"data:image/png;base64,{company.x_banner_image_1.decode()}" if company.x_banner_image_1 else "",
            },
            {
                'title': company.x_banner_title_2,
                'content': company.x_banner_content_2,
                'image': f"data:image/png;base64,{company.x_banner_image_2.decode()}" if company.x_banner_image_2 else "",
            },
            {
                'title': company.x_banner_title_3,
                'content': company.x_banner_content_3,
                'image': f"data:image/png;base64,{company.x_banner_image_3.decode()}" if company.x_banner_image_3 else "",
            },
            {
                'title': company.x_banner_title_4,
                'content': company.x_banner_content_4,
                'image': f"data:image/png;base64,{company.x_banner_image_4.decode()}" if company.x_banner_image_4 else "",
            },
        ]
        return banners

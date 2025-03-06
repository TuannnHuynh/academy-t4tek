{
    'name': 'Courses T4Tek',
    'version': '18.0.1.0.0',

    'category': 'Products Management',

    'summary': 'Courses',
    'description': '',
    'sequence': 5,

    'depends': ["website","product","website_sale"],
    'data': [
        'security/product_template_security.xml',
        'security/cart_order_security.xml',
        'views/product_template.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,

    'assets': {
        'web.assets_frontend':[
            
        ],
        'point_of_sale._assets_pos': [
            'courses/static/src/**/*'
        ],

    },
    'license': 'LGPL-3',
}
{
    'name': 'T4Tek Elearning',
    'version': '18.0.1.0.0',

    'category': 'Theme/Website',

    'summary': 'Theme Elearning',
    'description': '',


    'depends': ['website'],
    'data': [
        'views/pages/home.xml',
        'views/pages/khoa-hoc-ngan.xml',
        'views/pages/chi-tiet-khoa-hoc-ngan.xml',
       'views/blocks/s_content.xml',
       'views/customs/header.xml',
       'views/customs/footer.xml',
       'views/snippet.xml',
    ],

    'assets': {
        'web.assets_frontend':[
            'theme_elearning/static/src/scss/rest.scss',
            'theme_elearning/static/src/scss/course_short.scss',
            'theme_elearning/static/src/scss/course_detail_short.scss',
            'theme_elearning/static/src/scss/main.scss',
            'theme_elearning/static/src/js/product_widget.js',
            'theme_elearning/static/src/js/course_detail_short.js',
            "web/static/src/libs/fontawesome/css/font-awesome.css",
        ],
        'point_of_sale._assets_pos': [
            'theme_elearning/static/src/**/*'
        ],

    },
    'license': 'LGPL-3',
}
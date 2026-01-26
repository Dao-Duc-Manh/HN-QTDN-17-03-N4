# -*- coding: utf-8 -*-
{
    'name': "QLKH",

    'summary': """
        Module quản lý khách hàng và hợp đồng kế thừa từ quản lý văn bản""",

    'description': """
        Module quản lý khách hàng bao gồm:
        - Quản lý thông tin khách hàng
        - Phân loại khách hàng
        - Quản lý hợp đồng với khách hàng
        - Theo dõi trạng thái hợp đồng
        - Dashboard quản lý hợp đồng
    """,

    'author': "Nhom 8 - CNTT 16-0606",
    'website': "http://www.yourcompany.com",

    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'quan_ly_van_ban'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/khach_hang_data.xml',
        'views/loai_khach_hang.xml',
        'views/trang_thai_hop_dong.xml',
        'views/khach_hang.xml',
        'views/hop_dong.xml',
        'views/van_ban_lien_ket.xml',
        # 'views/cong_viec_ext.xml',
        'views/dashboard.xml',
        'views/dashboard_main.xml',
        'views/menu.xml',
    ],
}


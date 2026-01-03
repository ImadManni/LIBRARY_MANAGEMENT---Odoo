# -*- coding: utf-8 -*-
{
    'name': 'Library Management',
    'version': '16.0.1.0.0',
    'category': 'Education',
    'summary': 'Manage library books, readers, and loans',
    'description': """
        Library Management Module
        ========================
        This module provides a complete library management system with:
        - Book management (title, author, ISBN, category, copies, state)
        - Reader management (name, email, phone, type)
        - Loan management (borrowing and returning books)
        - Automatic book state updates
        - Copy availability checking
    """,
    'author': 'Academic Project',
    'website': 'https://www.odoo.com',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/book_views.xml',
        'views/reader_views.xml',
        'views/loan_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}


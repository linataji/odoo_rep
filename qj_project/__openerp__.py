# -*- coding: utf-8 -*- 
{
    'name': "SW - QJ - Project",
    'description': """
        Long description of module's purpose
    """,
    'author': "Smart Way Business Solution",
    'website': "https://www.smartway-jo.com",
    'category': 'Project',
    'version': '0.1',
    'depends': ['base','product','crm','sale','analytic','account_analytic_analysis'],
    'data': [
        'views/project_view.xml',
        'views/product_view.xml',
        'views/opportunities_view.xml',
        'views/sale_view.xml',
        'views/analytic_view.xml',
    ],
}
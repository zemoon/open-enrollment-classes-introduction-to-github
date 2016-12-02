# -*- coding: utf-8 -*-
{
    'name': "Cookbook",
    'summary': "Odoo can even make the cook!",
    'description': """
This module permit you to record recipes and to share them
on the internet.
""",
    'author': "DambyGreen",
    'category': 'Knowledge Management',
    'application': True,
    'version': '0.1',
    'licence': 'AGPL',
    'depends': ['base'],
    'data': [
        'data/cookbook.recipe.category.csv',
        'data/cookbook_recipe_data.xml',
        'views/recipe_views.xml',
        'views/recipe_template.xml',
        'security/recipe_security.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
        'data/cookbook_recipe_demo.xml',
    ],
}

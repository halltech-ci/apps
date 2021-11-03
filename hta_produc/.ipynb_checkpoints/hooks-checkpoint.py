from odoo import SUPERUSER_ID, api

def pre_init_product_category_code(cr):
    """
    This post-init-hook will update all existing category assigning them the
    corresponding default category_code.
    """
    
    cr.execute("ALTER TABLE product_category " "ADD COLUMN category_code character varying;")
    cr.execute("UPDATE product_category " "SET category_code = id;")
    
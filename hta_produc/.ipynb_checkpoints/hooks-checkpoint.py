from odoo import SUPERUSER_ID, api

def pre_init_product_code_ref(cr):
    """
    This post-init-hook will update all existing template assigning them the
    corresponding default code_ref.
    """
    
    cr.execute("ALTER TABLE product_template " "ADD COLUMN code_ref character varying;")
    cr.execute("UPDATE product_template " "SET code_ref = id;")
    
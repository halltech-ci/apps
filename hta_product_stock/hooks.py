#from odoo import SUPERUSER_ID, api

def pre_init_product_name(cr):
    
    """
    This post-init-hook will update all existing template assigning them the
    corresponding default name.
    """
    
    cr.execute("ALTER TABLE product_template " "ADD COLUMN name character varying;")
    cr.execute("UPDATE product_template " "SET name = id;")
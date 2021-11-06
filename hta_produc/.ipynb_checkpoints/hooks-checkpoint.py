#from odoo import SUPERUSER_ID, api

def pre_init_product_categ_id(cr):
    """
    This post-init-hook will update all existing template assigning them the
    corresponding default categ_id.
    """
    
    cr.execute("ALTER TABLE product_template " "ADD COLUMN categ_id character varying;")
    cr.execute("UPDATE product_template " "SET categ_id = id;")
    
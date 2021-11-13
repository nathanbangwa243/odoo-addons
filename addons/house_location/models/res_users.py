#-*- coding: utf-8 -*-

# odoo imports
from odoo import models
from odoo import fields

# others imports

class Users(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many('house.location', "salesperson", string="Property", help="",)
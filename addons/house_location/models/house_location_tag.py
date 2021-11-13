#-*- coding: utf-8 -*-

# odoo imports
from odoo import models
from odoo import fields
from odoo import api
from odoo import exceptions

# others imports


class HouseLocationTag(models.Model):
    _name = 'house.location.tag'
    _description = 'Property Tag'

    name = fields.Char(string="Property Tag", required=True, help="",)

    @api.model
    def create(self, vals):
        """create new tag

        Args:
            vals (dict): offer tag values

        Raises:
            exceptions.ValidationError: tag name already exists

        Returns:
            HouseLocationTag: a new instance of HouseLocationTag
        """

        tags_count = self.env['house.location.tag'].search([('name', '=', vals['name'])], count=True,)
        
        if tags_count > 0:
            raise exceptions.ValidationError(f"Tag {vals['name']} already exist")
        
        else:
            return super(HouseLocationTag, self).create(vals)
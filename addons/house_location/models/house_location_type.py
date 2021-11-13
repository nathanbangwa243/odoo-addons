# -*- coding: utf-8 -*-

# odoo imports
from odoo import models
from odoo import fields
from odoo import api
from odoo import exceptions

# others imports


class HouseLocationType(models.Model):
    _name = 'house.location.type'
    _description = 'Property Type'

    name = fields.Char(string="Property Type", required=True, help="",)

    @api.model
    def create(self, vals):
        """create new type

        Args:
            vals (dict): offer type values

        Raises:
            exceptions.ValidationError: type name already exists

        Returns:
            HouseLocationType: a new instance of HouseLocationType
        """

        types_count = self.env['house.location.type'].search(
            [('name', '=', vals['name'])], count=True,)

        if types_count > 0:
            raise exceptions.ValidationError(
                f"Type {vals['name']} already exist")

        else:
            return super(HouseLocationType, self).create(vals)

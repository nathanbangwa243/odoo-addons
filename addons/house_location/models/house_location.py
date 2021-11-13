# -*- coding: utf-8 -*-

# odoo imports
from odoo import models
from odoo import fields
from odoo import api
from odoo import exceptions

# others imports
import datetime


class HouseLocation(models.Model):
    _name = 'house.location'
    _description = 'House Location'

    name = fields.Char(string="Title", required=True, help="",)

    description = fields.Text(string="Description", help="",)

    postcode = fields.Char(string="Postcode", help="",)

    # the default availability date is in 3 months
    date_availability = fields.Date(string="Available From", default=fields.Date.today(
    ) + datetime.timedelta(days=90), help="",)

    expected_price = fields.Float(
        string="Expected Price", required=True, help="",)

    selling_price = fields.Float(
        string="Selling Price", readonly=True, help="",)

    bedrooms = fields.Integer(string="Bedrooms", default=2, help="",)

    living_area = fields.Integer(
        string="Living Area (sqm)", default=0, help="",)

    facades = fields.Integer(string="Facades", help="",)

    garage = fields.Boolean(string="Garage", help="",)

    garden = fields.Boolean(string="Garden", help="",)

    garden_area = fields.Integer(
        string="Garden Area (sqm)", default=0, help="",)

    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],

        help="",
    )

    active = fields.Boolean(string="Active", default=True, help="",)

    state = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        default='new',
        readonly=True,
    )

    # computed fields
    total_area = fields.Integer(
        string="Total Area", compute="_compute_total_area", help="")

    best_price = fields.Float(
        string="Best Offer", compute="_compute_best_offer", default=0, readonly=True, help="")

    # Model Link

    # property tags
    property_type_id = fields.Many2one(
        "house.location.type", string="Property Type",)

    # property tags
    tag_ids = fields.Many2many("house.location.tag", string="Property Tag",)

    # users and partners
    salesperson = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user, copy=False, help="")
    buyer = fields.Many2one("res.partner", string="Buyer", help="",)

    # offers
    offer_ids = fields.One2many(
        "house.location.offer", "property_id", string="Offers")

    # psql constraints : warning -> ne fonctionne pas
    _sql_constraints = [
        # ("check_positive_expected_price", "expected_price >= 0", "expected_price must be positive"),
    ]

    # Python constraints

    @api.constrains('expected_price')
    def _check_expected_price(self):
        """check expected_price constraint

        Raises:
            exceptions.ValidationError: negative value
        """

        for record in self:
            if (record.expected_price < 0):
                raise exceptions.ValidationError(
                    "Expected Price must be positive")

    @api.constrains('selling_price')
    def _check_selling_price(self):
        """check selling_price constraint

        Raises:
            exceptions.ValidationError: negative value
        """

        for record in self:
            if (record.selling_price < 0):
                raise exceptions.ValidationError(
                    "Selling Price must be positive")

    @api.constrains('bedrooms')
    def _check_bedrooms(self):
        """check bedrooms constraint

        Raises:
            exceptions.ValidationError: negative value
        """

        for record in self:
            if (record.bedrooms < 1):
                raise exceptions.ValidationError(
                    "Bedrooms must be positive and greater than 1")

    @api.constrains('living_area')
    def _check_living_area(self):
        """check living_area constraint

        Raises:
            exceptions.ValidationError: negative value
        """

        for record in self:
            if (record.living_area < 0):
                raise exceptions.ValidationError(
                    "Living Area must be positive")

    @api.constrains('facades')
    def _check_facades(self):
        """check facades constraint

        Raises:
            exceptions.ValidationError: negative value
        """

        for record in self:
            if (record.facades < 0):
                raise exceptions.ValidationError("facades must be positive")

    @api.constrains('garden_area')
    def _check_garden_area(self):
        """check garden_area constraint

        Raises:
            exceptions.ValidationError: negative value
        """

        for record in self:
            if (record.garden_area < 0):
                raise exceptions.ValidationError(
                    "Garden Area must be positive")

    # crud actions
    @api.model
    def unlink(self):
        """when user attempt to delete a property

        Raises:
            exceptions.UserError: only 'new' and 'canceled' property can be deleted

        Returns:
            HouseLocation: a new instance of HouseLocation
        """

        if self.state != "new" and self.state != 'canceled':
            raise exceptions.UserError(
                "only 'new' and 'canceled' property can be deleted")

        else:
            return super(HouseLocation, self).create()

    # computed function
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        """when living_area or garden_area changes, update total_area
        """

        for record in self:
            record.total_area = int(record.living_area) + \
                int(record.garden_area)

    @api.depends('offer_ids')
    def _compute_best_offer(self):
        """when an new offer is added, update the best offer
        """

        for record in self:
            # update best_price
            for offer in record.offer_ids:
                record.best_price = offer.price if offer.price > record.best_price else record.best_price

            # assign best_price when offer_ids is empty
            record.best_price = record.best_price

    # onchanges functions
    @api.onchange("garden")
    def _onchange_garden(self):
        """Onchange garden, set garden_area to 10 and garden_orientation to 'north'
        """

        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'

        else:
            self.garden_area = 0
            self.garden_orientation = None

    # buttons actions
    def sold_property(self):
        """Sold property

        Raises:
            exceptions.UserError: canceled property can't be sold
        """

        for record in self:
            if record.state == 'canceled':
                raise exceptions.UserError("Canceled property can't be sold")

            else:
                record.state = 'sold'

    def cancel_property(self):
        """Cancel property

        Raises:
            exceptions.UserError: sold property can't be canceled
        """

        for record in self:
            if record.state == 'sold':
                raise exceptions.UserError("Sold property can't be canceled")
            else:
                record.state = 'canceled'

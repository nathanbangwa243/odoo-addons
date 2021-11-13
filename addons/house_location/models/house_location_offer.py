# -*- coding: utf-8 -*-

# odoo imports
from odoo import models
from odoo import fields
from odoo import api
from odoo import exceptions

# others imports
import datetime


class HouseLocationOffer(models.Model):
    _name = 'house.location.offer'
    _description = 'Property Offer'

    price = fields.Float(string="Price", default=0, required=True, help="",)

    status = fields.Selection(
        string="Status",
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        readonly=True,
        copy=False,
    )

    # who is a offer owner?
    partner_id = fields.Many2one(
        "res.partner", required=True, string="Partner", help="",)

    # virtual link with 'house.location' model
    property_id = fields.Many2one(
        "house.location", string="Property", readonly=True, help="",)

    # warning : is only filled in when the record is created, therefore you will need a fallback to prevent crashing at time of creation.
    create_date = fields.Date(string="Create Date", copy=False,
                              default=lambda *args: fields.Date.today(), readonly=True, help="")
    validity = fields.Integer(string="Validity (days)")
    date_deadline = fields.Date(
        string="Deadline", compute="_compute_offer_deadline", inverse="_inverse_offer_deadline")

    # crud
    @api.model
    def create(self, vals):
        """create new offer

        Args:
            vals (dict): offer properties values

        Raises:
            exceptions.ValidationError: an other offer with this vals['price'] already exists

        Returns:
            HouseLocationOffer: a new instance of HouseLocationOffer
        """

        # warning : faire un filtre composite, les offres relatives a une seule maison

        offers_count = self.env['house.location.offer'].search(
            [('price', '=', vals['price'])], count=True,)

        if (offers_count > 0):
            raise exceptions.ValidationError(
                f"[NEW OFFER ERROR] Property have already received this offer \n {vals}")

        else:
            return super(HouseLocationOffer, self).create(vals)

    # constrains
    @api.constrains('price')
    def _check_price(self):
        """check price constraint

        Raises:
            exceptions.ValidationError: negative value or existing offer
        """

        for record in self:
            offers_count = self.env['house.location.offer'].search(
                [('price', '=', record.price)], count=True,)

            if (record.price < 0):
                raise exceptions.ValidationError(
                    f"[OFFER ID : {record.id}] Price must be positive")

            elif (offers_count > 1):
                raise exceptions.ValidationError(
                    f"[OFFER ID : {record.id}] An offer with this price already exist")

    @api.constrains('validity')
    def _check_validity(self):
        """check validity constraint

        Raises:
            exceptions.ValidationError: negative value
        """

        for record in self:
            if (record.validity < 0):
                raise exceptions.ValidationError(
                    f"[OFFER ID : {record.id}] validity must be positive")

    @api.constrains('date_deadline')
    def _check_date_deadline(self):
        """check validity constraint

        Raises:
            exceptions.ValidationError: date deadline < create date
        """

        for record in self:
            if (record.date_deadline < record.create_date):
                raise exceptions.ValidationError(
                    f"[OFFER ID : {record.id}] date deadline must be greater than create date")

    # compute
    @api.depends('validity')
    def _compute_offer_deadline(self):
        """compute deadline when validity value change
        """

        for record in self:
            record.date_deadline = record.create_date + \
                datetime.timedelta(days=record.validity)

    def _inverse_offer_deadline(self):
        """compute validity when date_deadline value change
        """

        for record in self:
            time_delta = record.date_deadline - record.create_date

            record.validity = time_delta.days

    # buttons actions

    def accept_offer(self):
        """check offer acceptability and set offer status to 'accepted' if not other accepted offer

        Raises:
            exceptions.ValidationError: an other accepted offer already exists  
        """

        # check existing accepted offer
        best_offer = 0.0

        for record in self:
            if record.property_id.state == 'offer accepted':  # il y a deja une offre accepted
                raise exceptions.UserError(
                    f"[OFFER ID : {record.id}] Property have already an accepted offer")

            else:
                # house_location.state = 'offer accepted'
                record.status = "accepted"
                record.property_id.state = 'offer accepted'
                record.property_id.selling_price = record.price
                record.property_id.buyer = record.partner_id

            # update best offer
            if record.price > best_offer:
                best_offer = record.price
                record.property_id.best_price = record.price

    def refuse_offer(self):
        """refuse an offer and set offer status to 'refused'
        """

        best_offer = 0.0

        for record in self:
            if record.status == 'accepted':  # c'etait une offre accepted
                record.property_id.state = 'offer received'
                record.property_id.selling_price = None
                record.property_id.buyer = None

            else:
                # house_location.state = 'offer accepted'
                pass

            # refuse offer
            record.status = "refused"

            # update best offer
            if record.price > best_offer:
                best_offer = record.price
                record.property_id.best_price = record.price

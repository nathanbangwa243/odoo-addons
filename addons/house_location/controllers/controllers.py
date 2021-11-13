# -*- coding: utf-8 -*-
from odoo import http


class HouseLocation(http.Controller):
    @http.route('/house_location/house_location/', auth='public')
    def index(self, **kw):
        return "Hello, world"

#     @http.route('/house_location/house_location/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('house_location.listing', {
#             'root': '/house_location/house_location',
#             'objects': http.request.env['house_location.house_location'].search([]),
#         })

#     @http.route('/house_location/house_location/objects/<model("house_location.house_location"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('house_location.object', {
#             'object': obj
#         })

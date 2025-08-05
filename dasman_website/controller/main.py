# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class DasmanWebsiteController(http.Controller):

    @http.route("/", type="http", auth="public", website=True)
    def home_page(self, **kwargs):
        cities = request.env["res.city"].search([])
        areas = request.env["res.area"].search([])
        return request.render("dasman_website.home_page", {"cities": cities, "areas": areas})

# -*- coding: utf-8 -*-
"""
This module is used to extend product.template model to add the following fields:
    1. is_accessory: This field is used to indicate whether the product is an accessory or not.
    2. has_accessory: This field is used to indicate whether the product has an accessory or not.
"""
from odoo import models, fields, api


class ProductTemplate(models.Model):
    """
    This class is used to extend product.template model.
    """

    _inherit = "product.template"

    is_accessory = fields.Boolean(string="Is Accessory")
    has_accessory = fields.Boolean(string="Has Accessory")
    accessory_line_ids = fields.One2many(
        "product.accessory.line",
        "product_tmpl_id",
        string="Accessory Lines",
        help="List of accessory lines for this product",
    )

    @api.onchange("is_accessory")
    def _onchange_is_accessory(self):
        if self.is_accessory:
            self.list_price = 0.0


class ProductAccessoryLine(models.Model):
    """
    This class is used to extend product.accessory.line model.
    """

    _name = "product.accessory.line"
    _description = "Product Accessory Line"
    _rec_name = "product_id"

    product_tmpl_id = fields.Many2one("product.template", string="Product Template", required=True, ondelete="cascade")
    product_id = fields.Many2one(
        "product.product",
        string="Accessory Product",
        required=True,
        domain="[('is_accessory', '=', True)]",
        help="Select an accessory product",
    )
    quantity = fields.Integer(string="Quantity", required=True, default=1)
    serial_number = fields.Char(string="Serial Number")

    def default_get(self, fields_list):
        # Optionally, you can override default_get to not pre-fill product_id
        return super(ProductAccessoryLine, self).default_get(fields_list)

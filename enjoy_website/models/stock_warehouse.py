from odoo import models, fields


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    gov_id = fields.Many2one(related='company_id.gov_id', string='Governorate')
    area_ids = fields.One2many(related='gov_id.area_ids', string='Areas')

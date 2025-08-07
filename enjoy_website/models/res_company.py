from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    gov_id = fields.Many2one('gov', string='Governorate')
    area_ids = fields.One2many(related='gov_id.area_ids', string='Areas')

from odoo import models, fields

class Gov(models.Model):
    _name = 'gov'
    _description = 'Governorate'

    name = fields.Char(string='Name', required=True)
    area_ids = fields.One2many('area', 'gov_id', string='Areas')
    branch_id = fields.Many2one('res.company', string='Branch')


class Area(models.Model):
    _name = 'area'
    _description = 'Area'

    name = fields.Char(string='Name', required=True)
    gov_id = fields.Many2one('gov', string='Governments', required=True)
    branch_id = fields.Many2one(related='gov_id.branch_id', string='Branch')

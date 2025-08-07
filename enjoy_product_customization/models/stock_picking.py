from odoo import models, api, fields
from odoo.exceptions import UserError


class StockMoveInherit(models.Model):
    _inherit = "stock.move"

    @api.model
    def create(self, vals):
        move = super().create(vals)
        if move.product_id and move.picking_id:
            move._add_accessory_moves()
        return move

    def write(self, vals):
        res = super().write(vals)
        if "product_id" in vals:
            for move in self:
                if move.product_id and move.picking_id:
                    move._add_accessory_moves()
        return res

    def _add_accessory_moves(self):
        product_tmpl = self.product_id.product_tmpl_id
        if product_tmpl.has_accessory and product_tmpl.accessory_line_ids:
            existing_accessory_ids = self.picking_id.move_ids_without_package.mapped("product_id").ids
            for accessory_line in product_tmpl.accessory_line_ids:
                if accessory_line.product_id.id not in existing_accessory_ids:
                    self.env["stock.move"].create(
                        {
                            "product_id": accessory_line.product_id.id,
                            "product_uom_qty": accessory_line.quantity or 1,
                            "product_uom": accessory_line.product_id.uom_id.id,
                            "name": accessory_line.product_id.display_name,
                            "picking_id": self.picking_id.id,
                            "location_id": self.location_id.id,  # Copy from parent move
                            "location_dest_id": self.location_dest_id.id,  # Copy from parent move
                            "origin": self.origin or self.picking_id.name,  # Optional but useful
                        }
                    )
        
    def unlink(self):
        for move in self:
            if move.picking_id:
                # Find accessory moves by product template reference
                accessory_products = move.product_id.product_tmpl_id.accessory_line_ids.mapped('product_id')
                accessory_moves = move.picking_id.move_ids_without_package.filtered(
                    lambda m: m.product_id in accessory_products and m != move
                )
                accessory_moves.unlink()
        return super().unlink()


# from odoo import models, api, fields
# from odoo.exceptions import UserError

# class StockMoveInherit(models.Model):
#     _inherit = "stock.move"

#     @api.onchange("product_id")
#     def _onchange_product_id_add_accessories(self):
#         if self.product_id and self._origin.picking_id:
#             product_tmpl = self.product_id.product_tmpl_id
#             if product_tmpl.has_accessory and product_tmpl.accessory_line_ids:
#                 # Get all accessory products
#                 for accessory_line in product_tmpl.accessory_line_ids:
#                     # Check if accessory already exists in move lines
#                     already_exists = self.picking_id.move_ids_without_package.filtered(lambda m: m.product_id == accessory_line.product_id)
#                     if not already_exists:
#                         self.picking_id.move_ids_without_package += self.env["stock.move"].new(
#                             {
#                                 "product_id": accessory_line.product_id.id,
#                                 "product_uom_qty": accessory_line.quantity or 1,
#                                 "product_uom": accessory_line.product_id.uom_id.id,
#                                 "name": accessory_line.product_id.display_name,
#                                 "picking_id": self.picking_id.id,
#                             }
#                         )

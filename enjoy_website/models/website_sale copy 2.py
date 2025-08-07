# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError


class WebsiteSale(models.Model):
    _inherit = "website"

    @api.model
    def get_location_filtered_products(self, gov_id=None, area_id=None):
        """
        Get products filtered by location (governorate) based on branch mapping
        Governorate → Branch → Warehouses
        """
        # Get all published and saleable products
        products = self.env["product.template"].sudo().search([("is_published", "=", True), ("sale_ok", "=", True)])

        if not gov_id:
            return products

        # Get the governorate and its associated branch
        governorate = self.env["gov"].sudo().browse(int(gov_id))
        if not governorate or not governorate.branch_id:
            return self.env["product.template"]

        # Get all warehouses under the governorate's branch
        warehouses = self.env["stock.warehouse"].sudo().search([("company_id", "=", governorate.branch_id.id)])

        if not warehouses:
            return self.env["product.template"]

        # Get all locations under these warehouses
        warehouse_locations = warehouses.mapped("view_location_id")
        all_locations = self.env["stock.location"].sudo().search([("id", "child_of", warehouse_locations.ids)])

        # Get products available in these locations
        quants = self.env["stock.quant"].sudo().search([("location_id", "in", all_locations.ids), ("quantity", ">", 0)])

        # Filter products to only those available in the selected location
        available_product_ids = quants.mapped("product_id.product_tmpl_id").ids
        filtered_products = products.filtered(lambda p: p.id in available_product_ids)

        return filtered_products

    @api.model
    def get_warehouses_by_governorate(self, gov_id):
        """
        Get warehouses associated with a governorate through its branch
        """
        if not gov_id:
            return self.env["stock.warehouse"]

        governorate = self.env["gov"].sudo().browse(int(gov_id))
        if not governorate or not governorate.branch_id:
            return self.env["stock.warehouse"]

        return self.env["stock.warehouse"].sudo().search([("company_id", "=", governorate.branch_id.id)])

    @api.model
    def get_branch_by_governorate(self, gov_id):
        """
        Get branch associated with a governorate
        """
        if not gov_id:
            return False

        governorate = self.env["gov"].sudo().browse(int(gov_id))
        return governorate.branch_id if governorate else False

    @api.model
    def get_products_domain_with_location_filter(self, base_domain=None, gov_id=None):
        """
        Get product domain with location filtering based on Governorate
        """
        if base_domain is None:
            base_domain = [("is_published", "=", True), ("sale_ok", "=", True)]

        if not gov_id:
            return base_domain

        # Get the governorate and its associated branch
        governorate = self.env["gov"].sudo().browse(int(gov_id))
        if not governorate or not governorate.branch_id:
            return base_domain

        # Get all warehouses under the governorate's branch
        warehouses = self.env["stock.warehouse"].sudo().search([("company_id", "=", governorate.branch_id.id)])

        if not warehouses:
            # If no warehouses, return empty result
            return [("id", "=", 0)]

        # Get all locations under these warehouses
        warehouse_locations = warehouses.mapped("view_location_id")
        all_locations = self.env["stock.location"].sudo().search([("id", "child_of", warehouse_locations.ids)])

        # Get products available in these locations
        quants = self.env["stock.quant"].sudo().search([("location_id", "in", all_locations.ids), ("quantity", ">", 0)])

        # Filter products to only those available in the selected location
        available_product_ids = quants.mapped("product_id.product_tmpl_id").ids
        if available_product_ids:
            base_domain.append(("id", "in", available_product_ids))
        else:
            # If no products available in the selected location, return empty result
            base_domain.append(("id", "=", 0))

        return base_domain


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def get_available_locations(self):
        """
        Get all locations where this product is available
        """
        self.ensure_one()
        quants = self.env["stock.quant"].sudo().search([("product_id.product_tmpl_id", "=", self.id), ("quantity", ">", 0)])
        return quants.mapped("location_id")

    def get_branches_with_stock(self):
        """
        Get branches that have stock of this product
        """
        self.ensure_one()
        locations = self.get_available_locations()

        # Get warehouses that contain these locations
        warehouses = self.env["stock.warehouse"].sudo().search([("view_location_id", "parent_of", locations.ids)])

        # Return the branches of these warehouses
        return warehouses.mapped("company_id")

    def get_governorates_with_stock(self):
        """
        Get governorates that have stock of this product through their branches
        """
        self.ensure_one()
        branches_with_stock = self.get_branches_with_stock()

        # Get governorates that have these branches
        return self.env["gov"].sudo().search([("branch_id", "in", branches_with_stock.ids)])

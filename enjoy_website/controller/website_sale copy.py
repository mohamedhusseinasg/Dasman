# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.exceptions import UserError


class DasmanWebsiteSale(WebsiteSale):
    """Extend WebsiteSale controller to add location filtering"""

    @http.route()
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        """Override shop method to add location filtering"""

        # Get location filters from request parameters
        gov_id = post.get('gov_id') or request.params.get('gov_id')
        area_id = post.get('area_id') or request.params.get('area_id')

        # Add location filters to context for product filtering
        context = dict(request.env.context)
        if gov_id:
            context['gov_id'] = int(gov_id)
        if area_id:
            context['area_id'] = int(area_id)
        # raise UserError(context)
        # {"lang": "en_US", "tz": "Asia/Kuwait", "uid": 2, "allowed_company_ids": [1], "website_id": 1, "edit_translations": False, "gov_id": 1, "area_id": 2}
        request.env.context = context

        # Call the parent method to get the base response
        response = super().shop(page=page, category=category, search=search, ppg=ppg, **post)
        # raise UserError(response)
        # Filter products if governorate is selected
        if gov_id:
            print(f"DEBUG: Filtering products for governorate ID: {gov_id}")
            filtered_products = request.env['website'].get_location_filtered_products(gov_id=int(gov_id))
            print(f"DEBUG: Found {len(filtered_products)} filtered products")

            # Update the response context with filtered products
            if hasattr(response, 'qcontext'):
                print(f"DEBUG: Updating qcontext with filtered products")
                response.qcontext['products'] = filtered_products
            elif hasattr(response, 'context'):
                print(f"DEBUG: Updating context with filtered products")

                raise UserError(response.context["products"].name)

            else:
                print(f"DEBUG: Response has no qcontext or context attribute")
        raise UserError(response.context["products"])
        return response

    @http.route()
    def products(self, **kwargs):
        """Override products method to filter by location"""
        # Get location filters from request parameters
        gov_id = request.params.get('gov_id')

        # Call parent method first
        response = super().products(**kwargs)

        # Filter products if governorate is selected
        if gov_id:
            filtered_products = request.env['website'].get_location_filtered_products(gov_id=int(gov_id))
            if hasattr(response, 'qcontext'):
                response.qcontext['products'] = filtered_products
            elif hasattr(response, 'context'):
                response.context['products'] = filtered_products

        return response 

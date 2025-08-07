# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.exceptions import UserError
from odoo.addons.website.controllers.main import QueryURL
# from odoo.tools import TableCompute
from odoo.addons.website_sale.controllers.main import TableCompute

class DasmanWebsiteSale(WebsiteSale):
    """Extend WebsiteSale controller to add location filtering"""

    @http.route()
    def shop(self, page=0, category=None, search="", ppg=False, **post):
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
        request.env.context = context
        # Call the parent method to get the base response
        response = super().shop(page=page, category=category, search=search, ppg=ppg, **post)

        filtered_products = request.env['website'].get_location_filtered_products(gov_id=int(gov_id) if gov_id else 1)

        response.qcontext["products"] = filtered_products
        response.qcontext["search_product"] = filtered_products
        response.qcontext["search_count"] = len(filtered_products)
        filtered_products = request.env['website'].sudo().get_location_filtered_products(gov_id=int(gov_id) if gov_id else 1)
        response.qcontext.update(
            {
            "products": filtered_products,
            "search_product": filtered_products,
            "search_count": len(filtered_products),
            }
        )

        # raise UserError(f"qcontext: {response.qcontext},, : {response.qcontext.get('products', [])} ,")
        # Set bins for the grid display
        ppg = response.qcontext.get('ppg', 20)
        ppr = response.qcontext.get('ppr', 4)
        bins = TableCompute().process(filtered_products, ppg, ppr)
        response.qcontext['bins'] = bins

        return request.render("website_sale.products", response.qcontext)

    # @http.route()
    # def products(self, **kwargs):
    #     """Override products method to filter by location"""
    #     # Get location filters from request parameters
    #     gov_id = kwargs.get("gov_id") or request.params.get("gov_id")
    #     area_id = kwargs.get("area_id") or request.params.get("area_id")

    #     # Prepare context with location filters
    #     context = dict(request.env.context)
    #     if gov_id:
    #         context["gov_id"] = int(gov_id)
    #     if area_id:
    #         context["area_id"] = int(area_id)
    #     request.env.context = context

    #     # Call parent method first to get base response
    #     response = super().products(**kwargs)

    #     # Only proceed with filtering if we have a governorate
    #     if not gov_id:
    #         return response

    #     # Get filtered products
    #     filtered_products = request.env["website"].with_context(context).get_location_filtered_products(gov_id=int(gov_id), area_id=int(area_id) if area_id else None)

    #     # Handle different response types
    #     if isinstance(response, bytes):
    #         # For JSON responses, we need to parse and modify
    #         try:
    #             import json

    #             response_data = json.loads(response.decode("utf-8"))
    #             if "products" in response_data:
    #                 response_data["products"] = [p for p in response_data["products"] if p["id"] in filtered_products.ids]
    #             return json.dumps(response_data)
    #         except:
    #             return response
    #     elif hasattr(response, "qcontext"):
    #         # For regular template responses
    #         response.qcontext["products"] = filtered_products
    #         # Keep original products if needed for other functionality
    #         response.qcontext["original_products"] = response.qcontext.get("products", [])
    #     elif hasattr(response, "response"):
    #         # For werkzeug responses
    #         return self._filter_products_in_response(response, filtered_products)

    #     return response

    # # def _filter_products_in_response(self, response, filtered_products):
    # #     """Helper method to filter products in a werkzeug response"""
    # #     from werkzeug.wrappers import Response
    # #     raise UserError(f"Filtered Products: {filtered_products.mapped('name')}")
    # #     if isinstance(response, Response):
    # #         try:
    # #             import json

    # #             response_data = json.loads(response.data)
    # #             if "products" in response_data:
    # #                 response_data["products"] = [p for p in response_data["products"] if p["id"] in filtered_products.ids]
    # #                 response.data = json.dumps(response_data)
    # #         except:
    # #             pass
    # #     return response

    # # def _prepare_product_values(self, product, category, search, **kwargs):
    # #     ProductCategory = request.env['product.public.category']
    # #     raise UserError(f"Preparing product values for {product.name}")
    # #     if category:
    # #         category = ProductCategory.browse(int(category)).exists()
    # #     keep = QueryURL(
    # #         '/shop',
    # #         **self._product_get_query_url_kwargs(
    # #             category=category and category.id,
    # #             search=search,
    # #             **kwargs,
    # #         ),
    # #     )

    # #     # Needed to trigger the recently viewed product rpc
    # #     view_track = request.website.viewref("website_sale.product").track

    # #     return {
    # #         'search': search,
    # #         'category': category,
    # #         'keep': keep,
    # #         'categories': ProductCategory.search([('parent_id', '=', False)]),
    # #         'main_object': product,
    # #         'optional_product_ids': [
    # #             p.with_context(active_id=p.id) for p in product.optional_product_ids
    # #         ],
    #         'product': product,
    #         'view_track': view_track,
    #     }


# from odoo import http
# from odoo.http import request
# from odoo.addons.website_sale.controllers.main import WebsiteSale
# from odoo.exceptions import UserError

# from odoo.addons.website.controllers.main import QueryURL

# class DasmanWebsiteSale(WebsiteSale):
#     """Extend WebsiteSale controller to add location filtering"""

#     @http.route()
#     def shop(self, page=0, category=None, search="", ppg=False, **post):
#         # Get location filters from request parameters
#         gov_id = post.get('gov_id') or request.params.get('gov_id')
#         area_id = post.get('area_id') or request.params.get('area_id')

#         # Add location filters to context for product filtering
#         context = dict(request.env.context)
#         if gov_id:
#             context['gov_id'] = int(gov_id)
#         if area_id:
#             context['area_id'] = int(area_id)
#         # raise UserError(context)
#         request.env.context = context
#         # Call the parent method to get the base response
#         response = super().shop(page=page, category=category, search=search, ppg=ppg, **post)


#         filtered_products = request.env['website'].get_location_filtered_products(gov_id=int(gov_id) if gov_id else 1)

#         response.qcontext["products"] = filtered_products
#         response.qcontext["search_product"] = filtered_products
#         response.qcontext["search_count"] = len(filtered_products)
#         filtered_products = request.env['website'].sudo().get_location_filtered_products(gov_id=int(gov_id) if gov_id else 1)
#         response.qcontext.update(
#             {
#             "products": filtered_products,
#             "search_product": filtered_products,
#             "search_count": len(filtered_products),
#             }
#         )
#         # raise UserError(f"qcontext: {response.qcontext},, : {response.qcontext.get('products', [])} ,")
#         return request.render("website_sale.products", response.qcontext)
# return response

# @http.route()
# def products(self, **kwargs):
#     """Override products method to filter by location"""
#     # Get location filters from request parameters
#     gov_id = kwargs.get("gov_id") or request.params.get("gov_id")
#     area_id = kwargs.get("area_id") or request.params.get("area_id")

#     # Prepare context with location filters
#     context = dict(request.env.context)
#     if gov_id:
#         context["gov_id"] = int(gov_id)
#     if area_id:
#         context["area_id"] = int(area_id)
#     request.env.context = context

#     # Call parent method first to get base response
#     response = super().products(**kwargs)

#     # Only proceed with filtering if we have a governorate
#     if not gov_id:
#         return response

#     # Get filtered products
#     filtered_products = request.env["website"].with_context(context).get_location_filtered_products(gov_id=int(gov_id), area_id=int(area_id) if area_id else None)

#     # Handle different response types
#     if isinstance(response, bytes):
#         # For JSON responses, we need to parse and modify
#         try:
#             import json

#             response_data = json.loads(response.decode("utf-8"))
#             if "products" in response_data:
#                 response_data["products"] = [p for p in response_data["products"] if p["id"] in filtered_products.ids]
#             return json.dumps(response_data)
#         except:
#             return response
#     elif hasattr(response, "qcontext"):
#         # For regular template responses
#         response.qcontext["products"] = filtered_products
#         # Keep original products if needed for other functionality
#         response.qcontext["original_products"] = response.qcontext.get("products", [])
#     elif hasattr(response, "response"):
#         # For werkzeug responses
#         return self._filter_products_in_response(response, filtered_products)

#     return response

# # def _filter_products_in_response(self, response, filtered_products):
# #     """Helper method to filter products in a werkzeug response"""
# #     from werkzeug.wrappers import Response
# #     raise UserError(f"Filtered Products: {filtered_products.mapped('name')}")
# #     if isinstance(response, Response):
# #         try:
# #             import json

# #             response_data = json.loads(response.data)
# #             if "products" in response_data:
# #                 response_data["products"] = [p for p in response_data["products"] if p["id"] in filtered_products.ids]
# #                 response.data = json.dumps(response_data)
# #         except:
# #             pass
# #     return response

# # def _prepare_product_values(self, product, category, search, **kwargs):
# #     ProductCategory = request.env['product.public.category']
# #     raise UserError(f"Preparing product values for {product.name}")
# #     if category:
# #         category = ProductCategory.browse(int(category)).exists()
# #     keep = QueryURL(
# #         '/shop',
# #         **self._product_get_query_url_kwargs(
# #             category=category and category.id,
# #             search=search,
# #             **kwargs,
# #         ),
# #     )

# #     # Needed to trigger the recently viewed product rpc
# #     view_track = request.website.viewref("website_sale.product").track

# #     return {
# #         'search': search,
# #         'category': category,
# #         'keep': keep,
# #         'categories': ProductCategory.search([('parent_id', '=', False)]),
# #         'main_object': product,
# #         'optional_product_ids': [
# #             p.with_context(active_id=p.id) for p in product.optional_product_ids
# #         ],
#         'product': product,
#         'view_track': view_track,
#     }

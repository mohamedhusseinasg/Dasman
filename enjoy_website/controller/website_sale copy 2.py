# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.exceptions import UserError

from odoo.addons.website.controllers.main import QueryURL


class TableCompute:

    def __init__(self):
        self.table = {}

    def _check_place(self, posx, posy, sizex, sizey, ppr):
        res = True
        for y in range(sizey):
            for x in range(sizex):
                if posx + x >= ppr:
                    res = False
                    break
                row = self.table.setdefault(posy + y, {})
                if row.setdefault(posx + x) is not None:
                    res = False
                    break
            for x in range(ppr):
                self.table[posy + y].setdefault(x, None)
        return res

    def process(self, products, ppg=20, ppr=4):
        # Compute products positions on the grid
        minpos = 0
        index = 0
        maxy = 0
        x = 0
        for p in products:
            x = min(max(p.website_size_x, 1), ppr)
            y = min(max(p.website_size_y, 1), ppr)
            if index >= ppg:
                x = y = 1

            pos = minpos
            while not self._check_place(pos % ppr, pos // ppr, x, y, ppr):
                pos += 1
            # if 21st products (index 20) and the last line is full (ppr products in it), break
            # (pos + 1.0) / ppr is the line where the product would be inserted
            # maxy is the number of existing lines
            # + 1.0 is because pos begins at 0, thus pos 20 is actually the 21st block
            # and to force python to not round the division operation
            if index >= ppg and ((pos + 1.0) // ppr) > maxy:
                break

            if x == 1 and y == 1:  # simple heuristic for CPU optimization
                minpos = pos // ppr

            for y2 in range(y):
                for x2 in range(x):
                    self.table[(pos // ppr) + y2][(pos % ppr) + x2] = False
            self.table[pos // ppr][pos % ppr] = {
                "product": p,
                "x": x,
                "y": y,
                "ribbon": p.sudo().website_ribbon_id,
            }
            if index <= ppg:
                maxy = max(maxy, y + (pos // ppr))
            index += 1

        # Format table according to HTML needs
        rows = sorted(self.table.items())
        rows = [r[1] for r in rows]
        for col in range(len(rows)):
            cols = sorted(rows[col].items())
            x += len(cols)
            rows[col] = [r[1] for r in cols if r[1]]

        return rows



class DasmanWebsiteSale(WebsiteSale):
    """Extend WebsiteSale controller to add location filtering"""


    @http.route()
    def shop(self, page=0, category=None, search="", ppg=False, **post):
        # Get location filters
        gov_id = post.get("gov_id") or request.params.get("gov_id")
        area_id = post.get("area_id") or request.params.get("area_id")

        # Call parent method first to get base response
        response = super().shop(page=page, category=category, search=search, ppg=ppg, **post)

        # Only apply filtering if location parameters exist
        if gov_id or area_id:
            # Get filtered products
            filtered_products = request.env["website"].get_location_filtered_products(gov_id=int(gov_id) if gov_id else None, area_id=int(area_id) if area_id else None)

            # Update context
            if hasattr(response, "qcontext"):
                response.qcontext.update(
                    {
                        "products": filtered_products,
                        "search_product": filtered_products,
                        "search_count": len(filtered_products),
                        "bins": lazy(lambda: TableCompute().process(products, ppg, ppr)),
                    }
                )

        return response


    def _prepare_product_grid(self, products, ppg):
        # """Helper method to prepare product grid bins"""
        # if not products:
        #     return []

        # ppr = 4  # products per row - hardcoded for simplicity
        # bins = 
        # for i in range(0, len(products), ppr):
        #     row = []
        #     for j in range(ppr):
        #         idx = i + j
        #         if idx >= len(products):
        #             break
        #         row.append({"product": products[idx], "x": 1, "y": 1, "ribbon": False})  # column span  # row span  # no ribbon by default
        #     bins.append(row)

        # return bins

    # @http.route()
    # def shop(self, page=0, category=None, search="", ppg=False, **post):
    #     # Get location filters from request parameters
    #     gov_id = post.get('gov_id') or request.params.get('gov_id')
    #     area_id = post.get('area_id') or request.params.get('area_id')

    #     # Add location filters to context for product filtering
    #     context = dict(request.env.context)
    #     if gov_id:
    #         context['gov_id'] = int(gov_id)
    #     if area_id:
    #         context['area_id'] = int(area_id)
    #     # raise UserError(context)
    #     # {"lang": "en_US", "tz": "Asia/Kuwait", "uid": 2, "allowed_company_ids": [1], "website_id": 1, "edit_translations": False, "gov_id": 1, "area_id": 2}
    #     request.env.context = context
    #     # raise UserError(f"Context: {context}")

    #     # Call the parent method to get the base response
    #     response = super().shop(page=page, category=category, search=search, ppg=ppg, **post)

    #     # Filter products if governorate is selected
    #     # if gov_id and hasattr(response, "qcontext"):
    #     filtered_products = request.env['website'].get_location_filtered_products(gov_id=int(gov_id) if gov_id else 1)
    #     # filtered_products = request.env["website"].get_location_filtered_products(gov_id=int(gov_id), area_id=int(area_id) if area_id else None)
    #     # Update the response context with filtered products
    #     response.qcontext["products"] = filtered_products
    #     # raise UserError(f"Filtered Products: {filtered_products.mapped('name')}")
    #     response.qcontext["search_product"] = filtered_products
    #     response.qcontext["search_count"] = len(filtered_products)
    #     filtered_products = request.env['website'].sudo().get_location_filtered_products(gov_id=int(gov_id) if gov_id else 1)
    #     response.qcontext.update(
    #         {
    #         "products": filtered_products,
    #         "search_product": filtered_products,
    #         "search_count": len(filtered_products),
    #         }
    #     )
    #     # raise UserError(f"Context: {request.env.context}, Filtered Products: {request}")
    #     # Show details of the current request for debugging

    #     # raise UserError("response details:\n%s" % response)
    #     # Render the template with the updated context

    #     return response

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

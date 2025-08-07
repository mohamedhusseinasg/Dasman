# -*- coding: utf-8 -*-
"""
==============================================================================
#  This module is used to extend product.template model to add the following
#  fields:
#    1. is_accessory: This field is used to indicate whether the product is an
#       accessory or not.
#    2. has_accessory: This field is used to indicate whether the product has an
#       accessory or not.
#
==============================================================================
"""
from . import product_model
from . import stock_picking
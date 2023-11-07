# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
  "name"                 :  "POS Multi Unit Of Measure",
  "summary"              :  """This module allow to use multiple units of measure for products in point of sale.""",
  "category"             :  "Point Of Sale",
  "version"              :  "1.0.1",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/",
  "description"          :  """POS Multi UOM, Multiple units, Product Multi UOM, Product Multi Units""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=pos_multi_product_uom&custom_url=/pos/auto",
  "depends"              :  ['point_of_sale','sale_management'],
  "data"                 :  ['views/product._uom.xml'],
  
  "assets"               :  {
                              'point_of_sale.assets': [
                                 "/pos_multi_product_uom/static/src/js/main.js",
                                  "/pos_multi_product_uom/static/src/js/ticket.js",
                                  "/pos_multi_product_uom/static/src/js/product.js",
                                "/pos_multi_product_uom/static/src/css/main.css",
                              ],
                              'web.assets_qweb': [
                                'pos_multi_product_uom/static/src/xml/**/*',
                              ],
                            },
  "images"               :  ['static/description/Banner.gif'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  45,
  "currency"             :  "USD",
  "pre_init_hook"        :  "pre_init_check",
}
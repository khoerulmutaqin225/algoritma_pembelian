from odoo import models, fields, _

class algoritma_pembelian(models.Model):
    _name = 'algoritma.pembelian'

    name = fields.Char(string="Name")

    tanggal = fields.Date(string="Tanggal")
    status = fields.Selection([('draft','Draft'),('to_approve','To Approve'),('approved','Approved'),('done','Done')], default='draft')
    algoritma_pembelian_ids = fields.One2many('algoritma.pembelian.line', 'algoritma_pembelian_id', string="Algoritma Pembelian Ids")
    brand_ids = fields.Many2many(
        'algoritma.brand',
        'algoritma_pembelian_brand_rel',
        'algoritma_pembelian_id',
        'brand_id',
        string='Brand Ids')

class algoritma_pembelian_line(models.Model):
    _name = 'algoritma.pembelian.line'

    algoritma_pembelian_id = fields.Many2one('algoritma.pembelian', string="Algoritma Pembelian Id")
    product_id = fields.Many2one('product.product', string="Product Id")
    quantity = fields.Float(string="Quantity", default=0.0)
    uom_id = fields.Many2one('uom.uom', string="Uom Id")

class algoritma_brand(models.Model):
    _name = 'algoritma.brand'

    name = fields.Char(string="Name")
# -*- coding: utf-8 -*-

#from odoo import models, fields, _


# class algoritma_pembelian(models.Model):
#     _name = 'algoritma_pembelian.algoritma_pembelian'
#     _description = 'algoritma_pembelian.algoritma_pembelian'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

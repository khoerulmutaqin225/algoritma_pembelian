from odoo import models, fields, _,api
from datetime import date
from odoo.exceptions import ValidationError

class algoritma_pembelian(models.Model):
    _name = 'algoritma.pembelian'
    
    # Inherite res dari model algoritma.pembelian
    @api.model
    def create(self, values):
        res = super(algoritma_pembelian, self).create(values)
        for rec in res:
            tanggal_pembelian = rec.tanggal
            tanggal_sekarang = date.today()                      
            if tanggal_pembelian < tanggal_sekarang:
                raise ValidationError(("Tanggal yang anda inputkan tidak boleh kurang dari tanggal sekarang"))
        return res
    
    
    def write(self, values):
        res = super(algoritma_pembelian, self).write(values)
        if 'tanggal' in values:
            tanggal_pembelian = self.tanggal
            tanggal_sekarang = date.today()
            if tanggal_pembelian < tanggal_sekarang:
                  raise ValidationError(("Tidak bisa edit jika tanggal yang anda inputkan kurang dari tanggal sekarang"))
        return res
    
    
    def func_to_approve(self):
        if self.status == 'draft':
            if self.name == 'New':
                seq = self.env['ir.sequence'].next_by_code('algoritma.pembelian') or 'New'
                self.name = seq
            self.status = 'to_approve'
    
    def func_approve(self):
        if self.status == 'to_approve':
            self.status = 'approved'
    
    def func_done(self):
        if self.status == 'approved':
            self.status = 'done'


    name = fields.Char(string="Name", default="New")

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
    
    @api.onchange('product_id')
    def func_onchange_product_id(self):
        if not self.product_id:
            return{}
        else:
            self.description = self.product_id.name
            return{}
        
    def _func_amount_total(self):
        for line in self:
            line.sub_total = line.quantity *line.price
    
    # def _func_domain_product_id(self):
    #     product_obj = self.env['product.product'].search([('type', '=', 'product')])
    #     domain =[('id', 'in', product_obj.ids)]
    #     return domain
        

    algoritma_pembelian_id = fields.Many2one('algoritma.pembelian', string="Algoritma Pembelian Id")
    # product_id = fields.Many2one('product.product', string="Product Id", domain=_func_domain_product_id)
    product_id = fields.Many2one('product.product', string="Product Id")
    quantity = fields.Float(string="Quantity", default=0.0)
    uom_id = fields.Many2one('uom.uom', string="Uom Id")
    description = fields.Char('Description')
    price = fields.Float(
        'Price',
         default=0.0
    )
    sub_total = fields.Float('Sub Total', compute=_func_amount_total)

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

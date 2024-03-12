from odoo import models, fields, _, api
from datetime import date, datetime
from odoo.exceptions import ValidationError
import xlrd
import base64
import os

def load_data(sheet):
    data =[]
    offset = 0
    for row in range(sheet.nrows):
        if row-offset == 0:
            col_codes = []
            for col in range(sheet.ncols):
                value = sheet.cell(row, col).value
                if type(value) == str:
                    value = value.strip()
                col_codes.append(value)
        elif row-offset > 0:
            new_line = {}
            for col in range(sheet.ncols):
                new_line[col_codes[col]] = sheet.cell(row, col).value
            data.append((new_line))
    return data
                

class algoritma_pembelian(models.Model):
    _name = 'algoritma.pembelian'
    def action_sql(self):
        # create
        # data_read0 = self.env.cr.execute("INSERT INTO ALGORITMA_PEMBELIAN(name,tanggal,status) VALUES('AP/2025/03/0000001','2024/03/06','to approve')")
        sqlCreate ="""
        INSERT INTO
        ALGORITMA_PEMBELIAN(name,tanggal,status)
        VALUES('AP/2025/03/0000001','2024/03/06','to approve')
        """
        sqlRead ="""
           SELECT 
           DISTINCT name,tanggal,status 
           from ALGORITMA_PEMBELIAN;
        """
        sqlUpdate ="""
            UPDATE 
            algoritma_pembelian 
            SET tanggal='2029/03/06' 
            WHERE id=12
        """
        sqlDelete ="""
            DELETE FROM
            algoritma_pembelian
            WHERE name='New'
        """
        data_read0 = self.env.cr.execute(sqlCreate)
        # read
        data_read1 = self.env.cr.execute(sqlRead)
        data_read2 = self.env.cr.fetchall()
        
        # update
        data_read3 = self.env.cr.execute(sqlUpdate)
        # delete
        self.env.cr.execute(sqlDelete)
        today = date.today()
        mail_values = {
            "email_from": "khoerulmutaqin225@gmail.com",
            "email_to": "khoerulmutaqin529@yahoo.com",
            "subject": "Notificatin SQL",
            "recipient_ids": [(6,0,[66])],
            "body_html": "NOTIFIKASI EMAIL",
        } 
        mail = self.env["mail.mail"].sudo().create(mail_values)
        mail.send()
        mail_values.update({"email_to":"khoerulmutaqin555@outlook.com"})
        mail = self.env["mail.mail"].sudo().create(mail_values)
        mail.send()
        return self
    
    def get_excel_report(self):
        return {
            'type': 'ir.actions.act_url',
            'url'  : '/algoritma_pembelian/algoritma_pembelian_report_excel/%s' % (self.id),
            'target' : 'new',  
        }
    
    def func_delete_status_draft(self):
        algoritma_pembelian_obj = self.env['algoritma.pembelian'].search([('status', '=', 'draft')])
        for line in algoritma_pembelian_obj:
            line.unlink()
        return True
        
    
    def show_tree_view(self):
        tree_view_id = self.env['ir.model.data'].xmlid_to_res_id('algoritma_pembelian.algoritma_pembelian_tree_view_id')
        form_view_id = self.env['ir.model.data'].xmlid_to_res_id('algoritma_pembelian.algoritma_pembelian_form_view_id')
        domain =[('status' , '=', 'draft')]
        result={
            'name': 'Pembelian B',
            'type': 'ir.actions.act_window',
            'views':[[tree_view_id, 'tree'],[form_view_id,'form']],
            'target': 'current',
            'res_model': 'algoritma.pembelian',
            'domain': domain,
            'limit': 40
        }
        return result
        
    
    
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
        for line in self:
            if line.status == 'draft':
                if line.name == 'New':
                    seq = self.env['ir.sequence'].next_by_code('algoritma.pembelian') or '/'
                    line.name = seq
                line.status = 'to_approve'
    
    def func_approve(self):
        if self.status == 'to_approve':
            self.status = 'approved'
    
    def func_done(self):
        if self.status == 'approved':
            self.status = 'done'


    name = fields.Char(string="Name", default="New")

    tanggal = fields.Date(string="Tanggal")
    status = fields.Selection([('draft','Draft'),('to_approve','To Approve'),('approved','Approved'),('done','Done')], default='draft')
    algoritma_pembelian_ids = fields.One2many('algoritma.pembelian.line', 'algoritma_pembelian_id', string="Algoritma Pembelian Ids" , ondelete='cascade')
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

class algoritma_pembelian_report_wizard(models.TransientModel):
    _name = 'algoritma.pembelian.report.wizard'

    name = fields.Char(string="Name")
    periode_awal = fields.Date('Periode Awal')
    periode_akhir = fields.Date('Periode Akhir')
    
    
    
class product_template(models.Model):
    _inherit = 'product.template'
    
    def _get_product_qrcode(self):
        for rec in self:
            rec.product_qrcode = str(rec.id)
                       
    def func_approve(self):
        if self.status == 'draft':
            self.status == 'approved'
    
    def print_qrcode(self):
        return{
            'type': 'ir.actions.report',
            'report_name'  : 'algoritma_pembelian.report_algoritma_pembelian_qrcode_id',
            'report_type' : 'qweb-pdf',  
        }
    
    status = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('done', 'Done'),
    ], string='status', default="draft")
    
    product_qrcode = fields.Char(
        'Product QR Code',
        compute= _get_product_qrcode
    )
    
class base_import(models.TransientModel):
    _inherit = 'base_import.import'
    # base_import.import
    
    file_import = fields.Binary('File Import')
    file_name_import = fields.Char('File Name Import')
    
    def action_import_algoritma_pembelian(self):
        data_product = []
        dict_algoritma_pembelian = {}
        algoritma_pembelian_obj = self.env['algoritma.pembelian']
        if self.file_import:
            filename, file_extension = os.path.splitext(self.file_name_import)
            if file_extension == '.xlsx' or file_extension == '.xls':
                book = xlrd.open_workbook(file_contents=base64.decodestring(self.file_import))
                sheet = book.sheet_by_index(0)
                data = load_data(sheet)
                for row in data:
                    # Pengambilan data tanggal
                    check_tanggal = row['Tanggal']
                    type_check_tanggal = type(check_tanggal)
                    if type_check_tanggal == float:
                        calculation_tanggal = (check_tanggal - 25569) * 86400
                        tanggal = datetime.utcfromtimestamp(calculation_tanggal).date()
                    else:
                        tanggal = check_tanggal.strip()
                        
                    # pengambilan data brand
                    check_brands = row['Brands'].strip()
                    brands = []
                    if check_brands != '':
                        get_name_brand = []
                        split_brand = check_brands.split(',')
                        for i in split_brand:
                            get_name_brand.append(i.strip())
                        brands_obj = self.env['algoritma.brand'].search([('name', 'in', get_name_brand)])
                        brands = brands_obj.ids
                        
                    # pengambilan data product
                    check_product = row['Product'].strip()
                    if check_product != '':
                        split_product= str(check_product).split(' ')[0]
                        replace_product_name = (split_product.replace('[', '')).replace(']', '')
                        product_obj = self.env['product.product'].search([('default_code', '=', replace_product_name )])
                        if product_obj:
                            product = product_obj.id
                        else:
                            product = None
                    else:
                        product = None
                    # Pengambilan data deskription
                    description = row['Description'].strip()
                
                    # pengambilan data quantity
                    check_quantity =row['Quantity']
                    if check_quantity != '':
                        quantity =  float(check_quantity)
                    else:
                        quantity = 0.0
                    
                    # pengambilan dara Uom
                    check_uom = row['Uom'].strip()
                    if check_uom != '':
                        uom_obj = self.env['uom.uom'].search([('name', '=', check_uom)])
                        if uom_obj:
                            uom = uom_obj.id
                        else:
                            uom = None
                            
                
                    # pengambilan dara price
                    check_price = row['Price']
                    if check_price != '':
                        price = float(check_price)
                    else:
                        price = 0.0
                    
                    # Catatan umum
                    # 0 = create
                    # 1 = updata
                    # 2 = remove
                    # 3 = cut dari beberapa object
                    # 4 = link ke exciting record
                    # 5 = delete all
                    # 6 = replace
                
                    values_header ={
                        'tanggal': tanggal,
                        'brand_ids': [(6,0, brands)],
                        'algoritma_pembelian_ids':[(0,0,{
                            'product_id': product,
                            'description': description,
                            'quantity': quantity,
                            'uom_id': uom,
                            'price': price                        
                        })]
                    }
                    new_algoritma_pembelian_id = algoritma_pembelian_obj.create(values_header)
                
                tree_view_id = self.env['ir.model.data'].xmlid_to_res_id('algoritma_pembelian.algoritma_pembelian_tree_view_id')               
                form_view_id = self.env['ir.model.data'].xmlid_to_res_id('algoritma_pembelian.algoritma_pembelian_form_view_id')
                return {
                    'name' : 'Algoritma pembelian',
                    'view_type' : 'form',
                    'view_mode' : 'tree,form', 
                    'type' : 'ir.actions.act_window', 
                    'res_model' : 'algoritma.pembelian', 
                    'views' : [[tree_view_id,'tree'],[form_view_id,'form']] 
                }               
        
    
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

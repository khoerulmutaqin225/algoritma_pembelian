# -*- coding: utf-8 -*-
from email import header
import json
import math
import logging
from odoo import _, api, fields, models
import requests
import werkzeug.wrappers
import functools
from odoo.http import request

from odoo import http
from odoo.http import content_disposition, request
import io
import xlsxwriter

class ReportExcelAlgoritmaPembelianController(http.Controller):
    @http.route([
        '/algoritma_pembelian/algoritma_pembelian_report_excel/<model("algoritma.pembelian"):data>',
    ], type='http', auth="user", csrf=False)
    def get_algoritma_pembelian_excel_report(self, data=None, **args):
        response = request.make_response(
            None,
            headers=[
                ('Content-Type', 'application/vnd.ms-excel'),
                ('Content-Disposition', content_disposition('Algoritma Pembelian Reports' + '.xlsx'))
            ]
        )
            
        
        # buat object workbook dari library xlsxwriter
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})

    
        # buat style untuk mengatur jenis font, ukuran font, dan alligment
        atas_style = workbook.add_format({'font_name': 'Times','bold':True, 'align':'left'})
        atas_isi_style = workbook.add_format({'font_name': 'Times','bold':False, 'align':'left'})
        header_style = workbook.add_format({'font_name': 'Times','bold':True, 'left':1, 'bottom': 1, 'right':1, 'top':1, 'align':'center' })
        text_style = workbook.add_format({'font_name': 'Times','bold':False, 'left':1, 'bottom': 1, 'right':1, 'top':1, 'align':'left' })
        
       
        # Looping algoritma Pembelian yang di pilih
        for atas in data:
            # buat worksheet / tab per user
            sheet = workbook.add_worksheet(atas.name)
            
            # set orientation jadi landscape
            sheet.set_landscape()
            
            # set ukuran dengan angka 9, yang artinya kertas A4
            sheet.set_paper(9)
            
            # set margin kertas dalam satuan inchi
            sheet.set_margins(0.5, 0.5, 0.5, 0.5)
            
            # set lebar kolom
            sheet.set_column('A:A', 5)
            sheet.set_column('B:B', 55)
            sheet.set_column('C:C', 40)
            sheet.set_column('D:D', 15)
            sheet.set_column('E:E', 15)
            sheet.set_column('F:F', 25)
            sheet.set_column('G:G', 25)
        
            # set judul atas 
            sheet.merge_range('A1:B1', 'Name', atas_style)
            sheet.merge_range('A2:B2', 'Tanggal', atas_style)
        

            # # set isi atas
            sheet.write(0, 2, atas.name, atas_isi_style)
            sheet.write(1, 2, atas.tanggal, atas_isi_style)
                    
                    
            # # set judul table
            sheet.write(3, 0, 'No', header_style)
            sheet.write(3, 1, 'Product', header_style)
            sheet.write(3, 2, 'Descriptions', header_style)
            sheet.write(3, 3, 'Quantity', header_style)
            sheet.write(3, 4, 'Uom', header_style)
            sheet.write(3, 5, 'Price', header_style)
            sheet.write(3, 6, 'Sub Total', header_style)

            row = 4
            number = 1
            
        
      
        
            # cari record data algoritma pembelian line yang dipilih
            record_line = request.env['algoritma.pembelian.line'].search([('algoritma_pembelian_id','=', atas.id)])
            for line in record_line:
                # content / list 
                sheet.write(row, 0, number, text_style)
                sheet.write(row, 1, line.product_id.display_name, text_style)
                sheet.write(row, 2, line.description, text_style)
                sheet.write(row, 3, line.quantity, text_style)
                sheet.write(row, 4, line.uom_id.name)
                sheet.write(row, 5, line.price)
                sheet.write(row, 6, line.sub_total)
                
                row += 1
                number += 1
        
        # Masuka file excel yang sudah di generate ke response dan return
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
        return response
    
class HelloApi(http.Controller):
    @http.route('/api', auth='public', website=False, csrf=False, type='json', methods=['GET', 'POST'])
    def hello(self, **kw):
        
        contacts = http.request.env['res.partner'].sudo().search([])

        contact_list =[]
        for contact in contacts:
            contact_list.append({
                'name': contact.name,
                'email': contact.email
            })
        return contact_list
                    
            
        # contact_list = [{
        #         'name': 'Ahsan',
        #         'last_name':'Ichi',
        #         'email': 'Ichi@gmail.com'
        #     },
        #     {
        #         'name': 'Khoerul',
        #         'last_name':'Ni',
        #         'email': 'Ni@gmail.com'
        #     },
        #     {
        #         'name': 'Apnan',
        #         'last_name':'San',
        #         'email': 'San@gmail.com'
        #     },
        #     {
        #         'name': 'Roku',
        #         'last_name':'cena',
        #         'email': 'john@gmail.com'
        #     },
        # ]

        # return contact_list               
    
class pembelianApi(http.Controller):
    @http.route('/api/pembelian', auth='public', website=False, csrf=False, type='json', methods=['GET', 'POST'])
    def pembelian(self, **kw):
        
        x = http.request.env['algoritma.pembelian'].sudo().search([])

        x_list =[]
        for xx in x:
            x_list.append({
                'id': xx.id,
                'name': xx.name,
                'email': xx.tanggal
            })
        return x_list
    
class GetControllerPembelianAPi(http.Controller):
    @http.route('/api/pembelian_get', auth='public', website=False, csrf=False, type='http', methods=['GET'])
    def pembelian(self, **params):

        algoritma_pembelian = http.request.env['algoritma.pembelian'].sudo().search([])
        disc_algoritma_pembelian ={}
        data_algoritma_pembelian =[]
        for h in algoritma_pembelian:
            dict_brand   = {}
            detail_brand = []
            dict_detail_product = {}
            detail_product = []
            
            for b in h.brand_ids:
                dict_brand = {'id': b.id, 'name': b.name}
                detail_brand.append(dict_brand)
            
            for p in h.algoritma_pembelian_ids:
                dict_detail_product = {
                    'product_id': p.product_id.display_name,
                    'description': p.description,
                    'quantity': p.quantity,
                    'uom_id': p.uom_id.name,
                    'price': p.price,
                    'sub_total': p.sub_total
                }
                detail_product.append(dict_detail_product)
            
            dict_algoritma_pembelian = {
                'id': h.id,
                'name': h.name,
                'brand_ids': detail_brand,
                'algoritma_pembelian_ids': detail_product
            }
            
            data_algoritma_pembelian.append(dict_algoritma_pembelian)
        
        data = {
            'status': 200,
            'message': 'success',
            'response': data_algoritma_pembelian
        }
        
        try:
            return werkzeug.wrappers.Response(
                status=200,
                content_type='application/json; charset=utf-8',
                response=json.dumps(data)
            )
        except:
            return werkzeug.wrappers.Response(
                status=400,
                content_type='application/json; charset=utf-8',
                headers=[('Access-Control-Allow-Origin', '*')],
                response=json.dumps({
                    'error': 'Error',
                    'error_descrip': str(e)
                })
            )


class AlgoritmaPembelianRestApi(http.Controller): 
    @http.route('/api/algoritma_pembelian_post/', type='json', auth='public',methods=['POST'] , csrf=False)
    def algoritma_pembelian_restapi_post(self, **params):
        order = params.get("order")
        tanggal = order[0]['tanggal']
        brand_ids= order[0]['brands_ids']
        name_brand = []
        for a in brand_ids:
            name_brand.append(a['name'])
        brands_obj = request.env['algoritma.brand'].sudo().search([('name', 'in', name_brand)])
        algoritma_pembelian_ids = order[0]['algoritma_pembelian_ids']
        vals_line = []
        for i in algoritma_pembelian_ids:
            product_obj = request.env['product.product'].sudo().search([('default_code', '=', i['product'])])
            uom_obj =  request.env['uom.uom'].sudo().search([('name', '=', i['uom'])])
            vals_line.append((0,0,{
                'product_id' : product_obj.id,
                'description' : product_obj.name,
                'quantity' : i['quantity'],
                'uom_id' : uom_obj.id,
                'price' : i['price'],
            }))
        vals_header = {
            'tanggal': tanggal, 'brand_ids': [(6,0, brands_obj.ids)], 'algoritma_pembelian_ids': vals_line
        }
        new_algoritma_pembelian = request.env['algoritma.pembelian'].sudo().create(vals_header)
        data = {
            'status' : 200,
            'message' : 'success',
            'tanggal' : tanggal,
            'brands' : brand_ids,
            'algoritma_pembelian_ids' : algoritma_pembelian_ids
        }
        return data

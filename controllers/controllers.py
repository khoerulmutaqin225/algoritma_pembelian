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
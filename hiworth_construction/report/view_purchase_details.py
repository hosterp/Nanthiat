from openerp import fields, models, api
import datetime, calendar
from openerp.osv import osv


class ViewPurchaseDetailsReport(models.TransientModel):
    _name='purchase.report.details.wizard'

    from_date = fields.Date('Date From')
    to_date = fields.Date('Date To')
    partner_id = fields.Many2one('res.partner', 'Supplier')
    status=fields.Boolean('Paid')

    @api.multi
    def get_purchase_products(self):
        domain = [('date_order', '>=', self.from_date), ('date_order', '<=', self.to_date)]

        if self.partner_id:
            domain.append(('partner_id', '=', self.partner_id.id))
        if self.status:
            domain.append(('state', '=', 'paid'))

        purchase_orders = self.env['purchase.order'].search(domain)

        products = []
        for rec in purchase_orders:
            for line in rec.order_line:
                products.append(line.product_id)
                print(line.product_id.name, 'product....................')

        return purchase_orders, products


    @api.multi
    def print_purchase_details_report(self):
        datas = {
            'ids': self._ids,
            'model': self._name,
            'form': self.read(),
            'context': self._context,
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'hiworth_construction.report_purchase_details_template_view',
            'datas': datas,
            'report_type': 'qweb-pdf',
            #             'context':{'start_date': self.from_date, 'end_date': self.to_date}
        }

    @api.multi
    def view_purchase_details_report(self):

        datas = {
            'ids': self._ids,
            'model': self._name,
            'form': self.read(),
            'context': self._context,
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'hiworth_construction.report_purchase_details_template_view',
            'datas': datas,
            'report_type': 'qweb-html',
            #             'context':{'start_date': self.from_date, 'end_date': self.to_date}
        }

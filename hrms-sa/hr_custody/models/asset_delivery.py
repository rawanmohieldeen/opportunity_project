
from datetime import date, datetime, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import Warning, UserError, ValidationError


class AssetDelivery(models.Model):
    _name = 'asset.delivery'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Reference",required=True, copy=False, readonly=True,default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee',string='Employee',required=True,copy=False)
    job_id = fields.Many2one('hr.job',string='Designation',related='employee_id.job_id')
    asset_type = fields.Selection([
        ('car', 'Car'),
        ('it', 'Information Technology'),
       ], string="Asset Type",required=True,default='car')
    car_id = fields.Many2one('hr.vehicle',string='Asset Name',copy=False)
    # plate_no = fields.Char(string="Plate NO",related='car_id.license_plate')
    property_id = fields.Many2one('custody.property',string='Asset Name',copy=False)
    brand = fields.Char(string="Plate NO",)
    model = fields.Char(string="Model NO",)
    quantity = fields.Integer(string="Quantity",)
    delivered_employee_id = fields.Many2one('hr.employee',string='Employee',required=True,copy=False)
    remark = fields.Text(string="Remarks",)


    @api.model
    def create(self, vals):
       if vals.get('name', _('New')) == _('New'):
           vals['name'] = self.env['ir.sequence'].next_by_code(
               'asset.delivery') or _('New')
       res = super(AssetDelivery, self).create(vals)
       return res
       
from odoo import models, fields, api , _

class OffenceReport(models.Model):
    _name = 'offence.report'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'employee_id'
    
    name = fields.Char(string="Reference",required=True, copy=False, readonly=True,default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee',string='Employee',required=True,track_visibility='onchange',copy=False)
    deparment_id = fields.Many2one('hr.department',string='Deparment',required=True,related='employee_id.department_id',track_visibility='onchange',copy=False)
    designation = fields.Many2one('hr.job',string='Designation',related='employee_id.job_id')
    violating_employee_id = fields.Many2one('hr.employee',string='Violating Employee',required=True,track_visibility='onchange',copy=False)
    violating_date = fields.Date(string='Violating Date',required=True,track_visibility='onchange',copy=False)
    line_ids = fields.One2many('offence.report.line', 'offence_report_id',string="offence Report Line",track_visibility='onchange')

    @api.model
    def create(self, vals):
       if vals.get('name', _('New')) == _('New'):
           vals['name'] = self.env['ir.sequence'].next_by_code(
               'offence.report') or _('New')
       res = super(OffenceReport, self).create(vals)
       return res

class OffenceReportLine(models.Model):
    _name = 'offence.report.line'


    offence_id = fields.Many2one('hr.offence',string='Offence',required=True)
    details = fields.Text('Further details and explanations')
    penalty = fields.Selection([
            ('verbal_warning', 'Verbal Warning'),
            ('written_warning', 'Written Warning'),
            ('termination', 'Termination'),
        ], string='Recommended Penalty', default='verbal_warning',required=True)

    offence_report_id = fields.Many2one('offence.report',string='Offence',required=True)




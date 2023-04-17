from odoo import models, fields, api

class HrTrainingCourse(models.Model):
    _name = 'hr.training.course'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'course'
    
    course = fields.Char(string='Training Course',required=True,track_visibility='onchange')
    place = fields.Char(string='Place',required=True,track_visibility='onchange')
    duration = fields.Char(string='Duration',required=True,track_visibility='onchange')
    duration_unit = fields.Selection([
        ('day', 'Day(s)'),
        ('month', 'Month(s)'),
       ], string="Duration Unit",required=True,track_visibility='onchange')
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True, default=lambda self: self.env.company.currency_id)
    fees = fields.Monetary('Fees',required=True,currency_field='currency_id',)
    comments = fields.Char(string='Comments',required=True,track_visibility='onchange')
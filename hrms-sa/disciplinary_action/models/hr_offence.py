from odoo import models, fields, api

class HROffence(models.Model):
    _name = 'hr.offence'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'action_type'

    action_type = fields.Char(string='Type of Action',required=True,track_visibility='onchange')
    initail_procedure = fields.Char(string='Initail Procedure',required=True,track_visibility='onchange')
    first_time = fields.Char(string='First Time',required=True,track_visibility='onchange')
    second_time = fields.Char(string='Second Time',required=True,track_visibility='onchange')
    third_time = fields.Char(string='Third Time',required=True,track_visibility='onchange')


    

from odoo import models, fields, api

class HrExitFactors(models.Model):
    _name = 'hr.exit.factors'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name',required=True,track_visibility='onchange')
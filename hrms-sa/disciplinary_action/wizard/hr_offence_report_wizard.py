# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class HrOffenceReportWizard(models.TransientModel):
    _name = "hr.offence.report.wizard"
    
    offence_ids = fields.Many2many('hr.offence',string='Journals', required=True)

    def print_report(self):
        data = {
            'model' : 'hr.offence.report.wizard',
            'form' : self.read()[0]
        }
        return self.env.ref('disciplinary_action.action_report_offence').report_action(records, data=data)

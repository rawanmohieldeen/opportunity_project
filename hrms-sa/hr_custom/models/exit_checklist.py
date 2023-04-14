# -*- coding: utf-8 -*-

from odoo import models, fields, api,_


class ExitChecklist(models.Model):
    _name = 'exit.checklist'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string="Employee",required=True,tracking=True)
    employee_no = fields.Char(related="employee_id.employee_no")
    department_id = fields.Many2one('hr.department', string="Department / Project",related="employee_id.department_id")
    job_id = fields.Many2one('hr.job', related="employee_id.job_id")
    parent_id = fields.Many2one('hr.employee',string="Line Manager / Project Head",related="employee_id.parent_id")
    end_date = fields.Date('Last Working Day',required=True,tracking=True)

    resignation_signed = fields.Boolean('Letter of Resignation/Termination signed',default=False)
    acknowledgement_signed = fields.Boolean('Termination Acknowledgement and Release Letter signed',default=False)
    demobilisation = fields.Boolean('Demobilisation arrangements (if expat) Departure date',default=False)
    timesheet = fields.Boolean('Final Timesheet submitted',default=False)
    bank_letter = fields.Boolean('Letter to the Bank sent',default=False)
    visa_cancellation = fields.Boolean('Visa/GOSI cancellation (To be done before or on the last working day)',default=False)
    insurance_submitted = fields.Boolean('Insurance Card submitted (To be submitted on the last day of employment)',default=False)
    exit_interview = fields.Boolean('Exit Interview conducted (if Resignation)',default=False)
    parking_submitted = fields.Boolean('Parking Card submitted',default=False)
    hr_comments = fields.Html()
    hr_date = fields.Date()

    laptop = fields.Boolean('Laptop / Desktop handed over',default=False)
    other_equipments = fields.Boolean('Other IT equipments handed over',default=False)
    email_changed = fields.Boolean('E-mail password changed',default=False)
    files_backed_up = fields.Boolean('Electronic files backed up',default=False)
    it_comments = fields.Html()
    it_date = fields.Date()

    process_completed = fields.Boolean('Hand over process completed',default=False)
    clearance = fields.Boolean('Office desk clearance',default=False)
    line_comments = fields.Html()
    line_date = fields.Date()

    payment_date = fields.Date('Final Payment to be processed ')
    stop_salary = fields.Boolean('Stop Salary Payments',default=False)
    finance_comments = fields.Html()
    finance_date = fields.Date()

    state = fields.Selection(selection=[
        ('hr','Hr'),('it','IT Approval'),
        ('line_manager','Line Manager Approval'),
        ('finance','Finance Approval'),
        ('approved','Approved')],default='hr',tracking=True)


    def action_to_it(self):
        self.write({'state':'it'})

    def action_to_line_manager(self):
        self.write({'state':'line_manager'})

    def action_to_finance(self):
        self.write({'state':'finance'})

    def action_to_done(self):
        self.write({'state':'approved'})

    
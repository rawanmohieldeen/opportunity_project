# -*- coding: utf-8 -*-

import datetime
from datetime import datetime, timedelta
from odoo.exceptions import UserError, AccessError
from odoo import models, fields, api, _


class LeaveApplicationForm(models.Model):
	_name = 'leave.application.form'
	_inherit = ['mail.thread', 'mail.activity.mixin']

	name = fields.Char(string="Reference Number", required=True,
					   readonly=True, default=lambda self: _('New'))
	employee_id = fields.Many2one('hr.employee', string="Employee Name", required=True)
	employee_no = fields.Char(related="employee_id.employee_no")
	job_title = fields.Many2one('hr.job', string="Job Title", required=True,related="employee_id.job_id")
	department_id = fields.Many2one('hr.department', string="Department", required=True,related="employee_id.department_id")
	contact_number = fields.Char(tracking=True)
	email = fields.Char(tracking=True)

	annual = fields.Boolean(default=False,tracking=True)
	hajj = fields.Boolean(default=False,tracking=True)
	maternity = fields.Boolean(default=False,tracking=True)
	marriage = fields.Boolean(default=False,tracking=True)
	paternity = fields.Boolean(default=False,tracking=True)
	accompanying = fields.Boolean(default=False,tracking=True)
	sick = fields.Boolean(default=False,tracking=True)
	quarantine = fields.Boolean(default=False,tracking=True)
	bereavement = fields.Boolean(default=False,tracking=True)
	academic = fields.Boolean(default=False,tracking=True)
	unpaid_leave = fields.Boolean(default=False,tracking=True)
	extended_leave_without_pay = fields.Boolean(default=False,tracking=True)
	unauthorised = fields.Boolean(default=False,tracking=True)
	other = fields.Boolean(default=False,tracking=True)

	leave_days = fields.Integer('Required Leave Days',required=True,tracking=True)
	official_holidays = fields.Integer(tracking=True)
	first_day = fields.Date('First Day of Leave',tracking=True)
	last_day = fields.Date('Last Day of Leave',tracking=True)
	first_day_office = fields.Date('First Day in Office',tracking=True)
	net_leave_days = fields.Integer('Net Leave Days',tracking=True)

	available_days = fields.Integer('Available Entitled Leave Days',tracking=True)
	requested_days = fields.Integer('Requested Leave Days',tracking=True)
	remaining_days = fields.Integer('Remaining Entitled Leave Days',tracking=True)
	state = fields.Selection([
		('draft', 'Draft'),
		('emp_submit', 'Employee Submit'), ('hr_approve', 'HR Approval'),
		('approved', 'Approved')], string='Status', default='draft')


	@api.model
	def create(self, vals):
		if vals.get('name', _('New')) == _('New'):
			vals['name'] = self.env['ir.sequence'].next_by_code(
				'leave.application.form') or _('New')
		res = super(LeaveApplicationForm, self).create(vals)
		return res

	def action_draft(self):
		self.write({
			'state': 'draft'
		})

	def action_submit(self):
		self.write({
			'state': 'emp_submit'
		})

	def action_approval(self):
		self.write({
			'state': 'hr_approve'
		})

	def action_approved(self):
		self.write({
			'state': 'approved'
		})
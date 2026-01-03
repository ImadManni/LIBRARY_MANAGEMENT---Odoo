# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class Reader(models.Model):
    _name = 'library.reader'
    _description = 'Library Reader'
    _order = 'name'

    name = fields.Char(string='Name', required=True, index=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    type = fields.Selection([
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('staff', 'Staff'),
        ('external', 'External')
    ], string='Type', required=True, default='student')

    # Relations
    loan_ids = fields.One2many('library.loan', 'reader_id', string='Loans')
    active_loans_count = fields.Integer(
        string='Active Loans',
        compute='_compute_active_loans_count',
        help='Number of books currently borrowed'
    )

    @api.depends('loan_ids', 'loan_ids.state')
    def _compute_active_loans_count(self):
        """Compute number of active loans"""
        for reader in self:
            reader.active_loans_count = len(
                reader.loan_ids.filtered(lambda l: l.state in ['borrowed', 'overdue'])
            )

    @api.constrains('email')
    def _check_email(self):
        """Validate email format"""
        for reader in self:
            if reader.email:
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(email_pattern, reader.email):
                    raise ValidationError('Please enter a valid email address.')


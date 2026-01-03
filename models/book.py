# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Book(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _order = 'title'

    name = fields.Char(string='Title', required=True, index=True)
    author = fields.Char(string='Author', required=True)
    isbn = fields.Char(string='ISBN', help='International Standard Book Number')
    category = fields.Char(string='Category')
    copies = fields.Integer(string='Total Copies', required=True, default=1)
    available_copies = fields.Integer(
        string='Available Copies',
        compute='_compute_available_copies',
        store=True,
        help='Number of copies currently available for loan'
    )
    state = fields.Selection([
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
        ('maintenance', 'Under Maintenance')
    ], string='State', default='available', required=True, tracking=True)

    # Relations
    loan_ids = fields.One2many('library.loan', 'book_id', string='Loans')

    @api.depends('copies', 'loan_ids', 'loan_ids.state')
    def _compute_available_copies(self):
        """Compute available copies based on active loans"""
        for book in self:
            active_loans = book.loan_ids.filtered(
                lambda l: l.state in ['borrowed', 'overdue']
            )
            book.available_copies = book.copies - len(active_loans)

    @api.constrains('copies')
    def _check_copies(self):
        """Ensure copies is a positive number"""
        for book in self:
            if book.copies < 0:
                raise ValidationError('Number of copies must be positive or zero.')

    @api.model
    def _update_book_states(self):
        """Automatically update book states based on availability"""
        for book in self.search([]):
            if book.available_copies > 0:
                if book.state == 'unavailable':
                    book.state = 'available'
            elif book.available_copies == 0:
                if book.state == 'available':
                    book.state = 'unavailable'

    def action_mark_maintenance(self):
        """Mark book as under maintenance"""
        self.write({'state': 'maintenance'})

    def action_mark_available(self):
        """Mark book as available"""
        if self.available_copies > 0:
            self.write({'state': 'available'})
        else:
            self.write({'state': 'unavailable'})


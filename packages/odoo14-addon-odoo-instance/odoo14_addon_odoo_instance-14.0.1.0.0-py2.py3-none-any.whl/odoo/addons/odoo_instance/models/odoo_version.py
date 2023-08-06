from odoo import models, fields

class OdooVersion(models.Model):
    _name = 'odoo.version'
    _description = 'Odoo Version'

    name = fields.Char(string='Version', required=True)

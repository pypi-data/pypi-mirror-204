from odoo import fields, models
import logging

class OdooInstanceProcess(models.Model):
    _logger = logging.getLogger(__name__)
    _name = 'odoo.instance.process'
    _description = 'Instance Process'

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    module_ids = fields.Many2many(
        "odoo.instance.module",
        "process_module_rel",
        "process_id",
        "module_id",
        string="Related Modules",
        search=['|', ('name', 'ilike', '%search%'),
                    ('technical_name', 'ilike', '%search%')]
    )
    handbook_url = fields.Char(string="Handbook URL")    
    odoo_version_id = fields.Many2one("odoo.version", string="Odoo Version", required=True)

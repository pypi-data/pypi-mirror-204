from odoo import models, api, fields
from odoo.tools.translate import _


class MetadataLine(models.Model):
    _name = 'metadata.line'

    key = fields.Char(string=_("Key"))
    value = fields.Char(string=_("Value"), translate=True)
    sort_order = fields.Integer(string=_("Sort order"))

    _order = "sort_order asc"

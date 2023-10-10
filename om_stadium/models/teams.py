from odoo import api, fields, models
from odoo.exceptions import ValidationError

class Teams(models.Model):
    _name="team.id"
    _describtion="teams_name"
    _inherit=['mail.thread']

    team_name = fields.Char(string="team_name", required=True,tracking=True)
    



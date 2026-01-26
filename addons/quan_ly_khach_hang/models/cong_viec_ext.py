from odoo import models, fields, api


class CongViecCustomer(models.Model):
    _inherit = 'cong.viec'

    khach_hang_id = fields.Many2one(
        'khach_hang',
        string='Khách hàng',
        compute='_compute_khach_hang_id',
        store=True,
    )

    @api.depends('van_ban_den_id', 'van_ban_den_id.id_khach_hang')
    def _compute_khach_hang_id(self):
        for record in self:
            record.khach_hang_id = record.van_ban_den_id.id_khach_hang if record.van_ban_den_id else False



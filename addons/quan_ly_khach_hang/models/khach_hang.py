from odoo import models, fields, api


class KhachHang(models.Model):
    _name = 'khach_hang'
    _description = 'Bảng chứa thông tin khách hàng'
    _rec_name = "ten_khach_hang"
    
    ma_khach_hang = fields.Char("Mã khách hàng", store=True, readonly=True)
    ten_khach_hang = fields.Char("Tên khách hàng", required=True)
    dia_chi = fields.Text("Địa chỉ", required=True)
    so_dien_thoai = fields.Char("Số điện thoại", required=True)
    email = fields.Char("Email")
    ma_so_thue = fields.Char("Mã số thuế")
    ghi_chu = fields.Text("Ghi chú")
    
    id_loai_khach_hang = fields.Many2one('loai_khach_hang', string='Loại khách hàng')
    hop_dong_ids = fields.One2many('hop_dong', 'id_khach_hang', string='Hợp đồng')
    van_ban_di_ids = fields.One2many('van_ban_di', 'id_khach_hang', string='Văn bản đi liên quan')
    van_ban_den_ids = fields.One2many('van_ban_den', 'id_khach_hang', string='Văn bản đến liên quan')
    cong_viec_ids = fields.One2many('cong.viec', 'khach_hang_id', string='Công việc liên quan')
    van_ban_di_count = fields.Integer(string="Số VB đi", compute="_compute_van_ban_counts")
    van_ban_den_count = fields.Integer(string="Số VB đến", compute="_compute_van_ban_counts")
    
    @api.model
    def create(self, vals):
        count = self.env['khach_hang'].search_count([]) + 1
        vals['ma_khach_hang'] = f"KH{count:05d}"
        return super(KhachHang, self).create(vals)

    def _compute_van_ban_counts(self):
        for rec in self:
            rec.van_ban_di_count = len(rec.van_ban_di_ids)
            rec.van_ban_den_count = len(rec.van_ban_den_ids)

    def action_view_van_ban_di(self):
        self.ensure_one()
        return {
            'name': "Văn bản đi của khách hàng",
            'type': 'ir.actions.act_window',
            'res_model': 'van_ban_di',
            'view_mode': 'tree,form',
            'domain': [('id_khach_hang', '=', self.id)],
            'context': {'default_id_khach_hang': self.id},
        }

    def action_view_van_ban_den(self):
        self.ensure_one()
        return {
            'name': "Văn bản đến của khách hàng",
            'type': 'ir.actions.act_window',
            'res_model': 'van_ban_den',
            'view_mode': 'tree,form',
            'domain': [('id_khach_hang', '=', self.id)],
            'context': {'default_id_khach_hang': self.id},
        }


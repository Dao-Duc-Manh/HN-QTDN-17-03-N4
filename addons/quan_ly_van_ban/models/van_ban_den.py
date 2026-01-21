from odoo import models, fields, api
import json
import time


class VanBanDen(models.Model):
    _name = 'van_ban_den'
    _description = 'Bảng chứa thông tin văn bản đến'
    _rec_name = "tieu_de"
    id = fields.Integer("ID văn bản đến", required=True)
    ngay_den = fields.Date("Ngày đến", required=True)
    so_hieu = fields.Char("Số hiệu",  store=True, readonly=True)
    co_quan_ban_hanh = fields.Char("Cơ quan ban hành", required=True)
    trich_yeu = fields.Text("Trích yếu", required=True)
    tieu_de =fields.Text("Tiêu đề", required=True)
    id_co_quan_nhan= fields.Many2one('phong_ban', string = 'Cơ quan nhận')
    tep_dinh_kem = fields.Binary("Tệp đính kèm")

    id_do_mat = fields.Many2one('do_mat', string='Độ mật')
    id_loai_van_ban = fields.Many2one('loai_van_ban', string='Loại văn bản')
    id_nam = fields.Many2one('nam', string='Năm')
    ids_cong_viec = fields.One2many('cong_viec', 'van_ban_den_ids', string='Công việc')
    id_nguoi_nhan =fields.Many2one('nhan_vien', string = 'Người nhận')
    ho_so = fields.Many2one ('ho_so', string='Hồ sơ')
    @api.model
    def create(self, vals):
        # region agent log
        try:
            payload = {
                "sessionId": "debug-session",
                "runId": "run1",
                "hypothesisId": "H1",
                "location": "van_ban_den.py:create",
                "message": "Incoming create for van_ban_den",
                "data": {"vals": vals},
                "timestamp": int(time.time() * 1000),
            }
            with open(r"\\wsl.localhost\Ubuntu-22.04\home\trungduc\BTL\.cursor\debug.log", "a", encoding="utf-8") as debug_file:
                debug_file.write(json.dumps(payload, ensure_ascii=False) + "\n")
        except Exception:
            pass
        # endregion
        count = self.env['van_ban_den'].search_count([]) + 1
        vals['so_hieu'] = f"{count}_{fields.Date.from_string(vals['ngay_den']).strftime('%Y%m%d')}"
        # region agent log
        try:
            payload = {
                "sessionId": "debug-session",
                "runId": "run1",
                "hypothesisId": "H2",
                "location": "van_ban_den.py:create",
                "message": "Computed so_hieu for van_ban_den",
                "data": {"count": count, "ngay_den": vals.get("ngay_den"), "so_hieu": vals.get("so_hieu")},
                "timestamp": int(time.time() * 1000),
            }
            with open(r"\\wsl.localhost\Ubuntu-22.04\home\trungduc\BTL\.cursor\debug.log", "a", encoding="utf-8") as debug_file:
                debug_file.write(json.dumps(payload, ensure_ascii=False) + "\n")
        except Exception:
            pass
        # endregion
        return super(VanBanDen, self).create(vals)

    



 
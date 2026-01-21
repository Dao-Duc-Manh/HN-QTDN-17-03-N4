from odoo import models, fields, api
import json
import time


class VanBanDashboard(models.TransientModel):
    _name = 'van_ban.dashboard'
    _description = 'Dashboard Quản lý Văn bản'

    # Computed fields for statistics
    tong_van_ban_den = fields.Integer(string="Tổng văn bản đến", compute="_compute_statistics", store=False)
    tong_van_ban_di = fields.Integer(string="Tổng văn bản đi", compute="_compute_statistics", store=False)
    tong_nhan_su = fields.Integer(string="Tổng nhân sự", compute="_compute_statistics", store=False)
    cong_viec_hoan_thanh = fields.Integer(string="Công việc đã hoàn thành", compute="_compute_statistics", store=False)
    cong_viec_dang_xu_ly = fields.Integer(string="Công việc đang xử lý", compute="_compute_statistics", store=False)
    cong_viec_hoan_thanh_muon = fields.Integer(string="Công việc hoàn thành muộn", compute="_compute_statistics", store=False)
    cong_viec_da_nhan = fields.Integer(string="Công việc đã nhận", compute="_compute_statistics", store=False)

    @api.model
    def action_open_dashboard(self):
        """Tạo record dashboard và trả về action để mở form view"""
        # region agent log
        try:
            payload = {
                "sessionId": "debug-session",
                "runId": "run1",
                "hypothesisId": "H3",
                "location": "dashboard.py:action_open_dashboard",
                "message": "Opening dashboard",
                "data": {},
                "timestamp": int(time.time() * 1000),
            }
            with open(r"\\wsl.localhost\Ubuntu-22.04\home\trungduc\BTL\.cursor\debug.log", "a", encoding="utf-8") as debug_file:
                debug_file.write(json.dumps(payload, ensure_ascii=False) + "\n")
        except Exception:
            pass
        # endregion
        dashboard = self.create({})
        return {
            'name': 'Dashboard Quản lý Văn bản',
            'type': 'ir.actions.act_window',
            'res_model': 'van_ban.dashboard',
            'res_id': dashboard.id,
            'view_mode': 'form',
            'target': 'current',
            'view_id': self.env.ref('quan_ly_van_ban.view_van_ban_dashboard_form').id,
        }

    @api.depends()
    def _compute_statistics(self):
        # region agent log
        try:
            payload = {
                "sessionId": "debug-session",
                "runId": "run1",
                "hypothesisId": "H4",
                "location": "dashboard.py:_compute_statistics",
                "message": "Computing statistics - start",
                "data": {},
                "timestamp": int(time.time() * 1000),
            }
            with open(r"\\wsl.localhost\Ubuntu-22.04\home\trungduc\BTL\.cursor\debug.log", "a", encoding="utf-8") as debug_file:
                debug_file.write(json.dumps(payload, ensure_ascii=False) + "\n")
        except Exception:
            pass
        # endregion
        # Tổng số lượng
        self.tong_van_ban_den = self.env['van_ban_den'].search_count([])
        self.tong_van_ban_di = self.env['van_ban_di'].search_count([])
        self.tong_nhan_su = self.env['nhan_vien'].search_count([])

        # Công việc theo trạng thái
        trang_thai_hoan_thanh = self.env['trang_thai'].search([('ten_trang_thai', '=', 'Hoàn thành')], limit=1)
        trang_thai_dang_xu_ly = self.env['trang_thai'].search([('ten_trang_thai', '=', 'Đang xử lý')], limit=1)
        trang_thai_hoan_thanh_qua_han = self.env['trang_thai'].search([('ten_trang_thai', '=', 'Hoàn thành quá hạn')], limit=1)
        trang_thai_da_nhan = self.env['trang_thai'].search([('ten_trang_thai', '=', 'Đã nhận')], limit=1)

        self.cong_viec_hoan_thanh = self.env['cong_viec'].search_count([('trang_thai', '=', trang_thai_hoan_thanh.id)]) if trang_thai_hoan_thanh else 0
        self.cong_viec_dang_xu_ly = self.env['cong_viec'].search_count([('trang_thai', '=', trang_thai_dang_xu_ly.id)]) if trang_thai_dang_xu_ly else 0
        self.cong_viec_hoan_thanh_muon = self.env['cong_viec'].search_count([('trang_thai', '=', trang_thai_hoan_thanh_qua_han.id)]) if trang_thai_hoan_thanh_qua_han else 0
        self.cong_viec_da_nhan = self.env['cong_viec'].search_count([('trang_thai', '=', trang_thai_da_nhan.id)]) if trang_thai_da_nhan else 0
        # region agent log
        try:
            payload = {
                "sessionId": "debug-session",
                "runId": "run1",
                "hypothesisId": "H4",
                "location": "dashboard.py:_compute_statistics",
                "message": "Computing statistics - end",
                "data": {
                    "tong_van_ban_den": self.tong_van_ban_den,
                    "tong_van_ban_di": self.tong_van_ban_di,
                    "tong_nhan_su": self.tong_nhan_su,
                    "trang_thai_ids": {
                        "hoan_thanh": trang_thai_hoan_thanh.id if trang_thai_hoan_thanh else None,
                        "dang_xu_ly": trang_thai_dang_xu_ly.id if trang_thai_dang_xu_ly else None,
                        "hoan_thanh_qua_han": trang_thai_hoan_thanh_qua_han.id if trang_thai_hoan_thanh_qua_han else None,
                        "da_nhan": trang_thai_da_nhan.id if trang_thai_da_nhan else None,
                    },
                    "cong_viec": {
                        "hoan_thanh": self.cong_viec_hoan_thanh,
                        "dang_xu_ly": self.cong_viec_dang_xu_ly,
                        "hoan_thanh_muon": self.cong_viec_hoan_thanh_muon,
                        "da_nhan": self.cong_viec_da_nhan,
                    },
                },
                "timestamp": int(time.time() * 1000),
            }
            with open(r"\\wsl.localhost\Ubuntu-22.04\home\trungduc\BTL\.cursor\debug.log", "a", encoding="utf-8") as debug_file:
                debug_file.write(json.dumps(payload, ensure_ascii=False) + "\n")
        except Exception:
            pass
        # endregion


    def action_view_van_ban_den(self):
        return {
            'name': 'Văn bản đến',
            'type': 'ir.actions.act_window',
            'res_model': 'van_ban_den',
            'view_mode': 'tree,form',
        }

    def action_view_van_ban_di(self):
        return {
            'name': 'Văn bản đi',
            'type': 'ir.actions.act_window',
            'res_model': 'van_ban_di',
            'view_mode': 'tree,form',
        }

    def action_view_nhan_su(self):
        return {
            'name': 'Nhân sự',
            'type': 'ir.actions.act_window',
            'res_model': 'nhan_vien',
            'view_mode': 'tree,form',
        }

    def action_view_cong_viec_chi_tiet(self):
        return {
            'name': 'Công việc',
            'type': 'ir.actions.act_window',
            'res_model': 'cong_viec',
            'view_mode': 'tree,form',
        }


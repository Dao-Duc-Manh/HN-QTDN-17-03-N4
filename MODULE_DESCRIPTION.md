# Mô Tả Module: Quản Lý Văn Bản và Quản Lý Khách Hàng

## 1. MODULE QUẢN LÝ VĂN BẢN (quan_ly_van_ban)

### 1.1. Tổng quan
Module quản lý văn bản là module cơ sở để quản lý toàn bộ hệ thống văn bản đi, văn bản đến, công việc và các thông tin liên quan trong tổ chức.

**Dependencies:** `base`, `nhan_su`

### 1.2. Các chức năng chính

#### 1.2.1. Quản lý Văn bản Đi (van_ban_di)
- **Mục đích:** Quản lý các văn bản được gửi đi từ tổ chức
- **Thông tin chính:**
  - Tiêu đề, trích yếu
  - Ngày đi, số hiệu (tự động tạo)
  - Loại văn bản (Công văn, Quyết định, Chỉ thị)
  - Độ mật (Tuyệt mật, Mật, Thường)
  - Cơ quan ban hành (phòng ban)
  - Người ký (nhân viên)
  - Nơi nhận
  - Năm, Hồ sơ
- **Tính năng đặc biệt:**
  - Tự động tạo số hiệu theo format: `{count}_{ngay_di_YYYYMMDD}`
  - Liên kết với phòng ban và nhân viên từ module `nhan_su`

#### 1.2.2. Quản lý Văn bản Đến (van_ban_den)
- **Mục đích:** Quản lý các văn bản nhận được từ bên ngoài
- **Thông tin chính:**
  - Tiêu đề, trích yếu
  - Ngày đến, số hiệu (tự động tạo)
  - Cơ quan ban hành (text)
  - Cơ quan nhận (phòng ban)
  - Người nhận (nhân viên)
  - Loại văn bản, độ mật, năm, hồ sơ
- **Tính năng đặc biệt:**
  - Tự động tạo số hiệu theo format: `{count}_{ngay_den_YYYYMMDD}`
  - Liên kết với công việc (One2many) - một văn bản đến có thể tạo nhiều công việc

#### 1.2.3. Quản lý Công việc (cong.viec)
- **Mục đích:** Quản lý các công việc phát sinh từ văn bản đến
- **Thông tin chính:**
  - Tên công việc, yêu cầu xử lý
  - Ngày tạo, hạn xử lý, ngày hoàn thành
  - Tình trạng (Đã nhận, Hủy)
  - Trạng thái (tự động tính toán): Hoàn thành, Hoàn thành quá hạn, Đã nhận, Đang xử lý, Hủy
  - Chỉ đạo, Chủ trì giải quyết (nhân viên)
  - Văn bản đến liên quan (Many2one)
- **Tính năng đặc biệt:**
  - **Tự động tính toán trạng thái** dựa trên:
    - Ngày hoàn thành: Nếu có → "Hoàn thành" hoặc "Hoàn thành quá hạn"
    - Tình trạng: Nếu "Hủy" → "Hủy"
    - Hạn xử lý: So sánh với ngày hiện tại để xác định "Đang xử lý" hoặc "Đã nhận"
  - Tự động set `tinh_trang = 'da_nhan'` và `ngay_tao = today()` khi tạo mới
  - Tự động tính lại trạng thái khi có thay đổi

#### 1.2.4. Quản lý Danh mục
- **Trạng thái (trang_thai):** Hoàn thành, Hoàn thành quá hạn, Đã nhận, Đang xử lý, Hủy
- **Loại văn bản (loai_van_ban):** Công văn, Quyết định, Chỉ thị
- **Độ mật (do_mat):** Tuyệt mật, Mật, Thường
- **Năm (nam):** Quản lý theo năm
- **Hồ sơ (ho_so):** Quản lý hồ sơ văn bản theo thời gian

#### 1.2.5. Dashboard Quản lý Văn bản
- **Thống kê:**
  - Tổng văn bản đến
  - Tổng văn bản đi
  - Tổng nhân sự
  - Công việc đã hoàn thành
  - Công việc đang xử lý
  - Công việc hoàn thành muộn
  - Công việc đã nhận
- **Tính năng:**
  - Tự động tính toán khi mở dashboard
  - Các nút "Xem thêm" để xem chi tiết từng loại
  - Liên kết trực tiếp đến các danh sách tương ứng

---

## 2. MODULE QUẢN LÝ KHÁCH HÀNG (quan_ly_khach_hang)

### 2.1. Tổng quan
Module quản lý khách hàng mở rộng chức năng của module quản lý văn bản bằng cách thêm khả năng quản lý khách hàng, hợp đồng và liên kết chúng với văn bản.

**Dependencies:** `base`, `quan_ly_van_ban`

### 2.2. Các chức năng chính

#### 2.2.1. Quản lý Khách hàng (khach_hang)
- **Mục đích:** Quản lý thông tin khách hàng và các mối quan hệ
- **Thông tin chính:**
  - Mã khách hàng (tự động: `KH{count:05d}`)
  - Tên khách hàng, địa chỉ, số điện thoại, email
  - Mã số thuế, ghi chú
  - Loại khách hàng (VIP, Thường, Mới)
- **Mối quan hệ:**
  - **One2many với Hợp đồng:** Một khách hàng có nhiều hợp đồng
  - **One2many với Văn bản đi:** Văn bản đi liên quan đến khách hàng
  - **One2many với Văn bản đến:** Văn bản đến liên quan đến khách hàng
  - **One2many với Công việc:** Công việc liên quan đến khách hàng
- **Tính năng:**
  - Đếm số lượng văn bản đi/đến (computed fields)
  - Action buttons để xem danh sách văn bản đi/đến của khách hàng
  - Hiển thị hợp đồng và công việc liên quan trong form view

#### 2.2.2. Quản lý Hợp đồng (hop_dong)
- **Mục đích:** Quản lý hợp đồng với khách hàng
- **Thông tin chính:**
  - Số hợp đồng (tự động: `HD{count:05d}_{ngay_ky_YYYYMMDD}`)
  - Tên hợp đồng, mô tả
  - Ngày ký, ngày bắt đầu, ngày kết thúc
  - Giá trị hợp đồng (Monetary field)
  - Tình trạng: Đang thực hiện, Hoàn thành, Hủy, Tạm dừng
  - Trạng thái (tự động tính toán): Đang thực hiện, Sắp hết hạn, Quá hạn, Hoàn thành, Hủy, Tạm dừng
  - Khách hàng (Many2one, required)
  - Người quản lý (res.users)
  - Tệp đính kèm
- **Tính năng đặc biệt:**
  - **Tự động tính toán trạng thái** dựa trên:
    - Tình trạng: Nếu "Hủy" → "Hủy", "Tạm dừng" → "Tạm dừng", "Hoàn thành" → "Hoàn thành"
    - Ngày kết thúc: So sánh với ngày hiện tại
      - Quá hạn (< 0 ngày) → "Quá hạn"
      - Sắp hết hạn (≤ 30 ngày) → "Sắp hết hạn"
      - Còn thời gian (> 30 ngày) → "Đang thực hiện"
  - Hiển thị văn bản liên quan (computed từ khách hàng)

#### 2.2.3. Mở rộng Văn bản (van_ban_ext)
- **Mục đích:** Thêm field `id_khach_hang` vào văn bản đi và văn bản đến
- **Cách hoạt động:**
  - Sử dụng `_inherit` để mở rộng model `van_ban_di` và `van_ban_den`
  - Thêm field `id_khach_hang` (Many2one) để liên kết với khách hàng
  - Cho phép theo dõi văn bản theo khách hàng

#### 2.2.4. Mở rộng Công việc (cong_viec_ext)
- **Mục đích:** Thêm field `khach_hang_id` vào công việc
- **Cách hoạt động:**
  - Sử dụng `_inherit` để mở rộng model `cong.viec`
  - Thêm field `khach_hang_id` (Many2one, computed)
  - Tự động lấy khách hàng từ văn bản đến liên quan
  - Logic: `khach_hang_id = van_ban_den_id.id_khach_hang`

#### 2.2.5. Quản lý Danh mục
- **Loại khách hàng (loai_khach_hang):** VIP, Thường, Mới
- **Trạng thái hợp đồng (trang_thai_hop_dong):** Đang thực hiện, Sắp hết hạn, Quá hạn, Hoàn thành, Hủy, Tạm dừng

#### 2.2.6. Dashboard Quản lý Khách hàng
- **Thống kê:**
  - Tổng khách hàng
  - Tổng hợp đồng
  - Tổng văn bản đến (có liên kết khách hàng)
  - Tổng văn bản đi (có liên kết khách hàng)
  - Hợp đồng đang thực hiện
  - Hợp đồng sắp hết hạn
  - Hợp đồng quá hạn
- **Tính năng:**
  - Tự động tính toán khi mở dashboard
  - Các nút "Xem thêm" để xem chi tiết từng loại
  - Liên kết trực tiếp đến các danh sách tương ứng

---

## 3. MỐI QUAN HỆ GIỮA 2 MODULE

### 3.1. Quan hệ Dependency
```
quan_ly_khach_hang → depends on → quan_ly_van_ban
```
- Module `quan_ly_khach_hang` phụ thuộc vào `quan_ly_van_ban`
- Không thể cài đặt `quan_ly_khach_hang` mà không có `quan_ly_van_ban`

### 3.2. Quan hệ Kế thừa (Inheritance)

#### 3.2.1. Văn bản Đi/Đến
```
van_ban_di (quan_ly_van_ban)
    ↓ _inherit
VanBanDiCustomer (quan_ly_khach_hang)
    + id_khach_hang (Many2one → khach_hang)

van_ban_den (quan_ly_van_ban)
    ↓ _inherit
VanBanDenCustomer (quan_ly_khach_hang)
    + id_khach_hang (Many2one → khach_hang)
```

#### 3.2.2. Công việc
```
cong.viec (quan_ly_van_ban)
    ↓ _inherit
CongViecCustomer (quan_ly_khach_hang)
    + khach_hang_id (Many2one → khach_hang, computed)
    Logic: khach_hang_id = van_ban_den_id.id_khach_hang
```

### 3.3. Quan hệ Dữ liệu

#### 3.3.1. Khách hàng ↔ Văn bản
```
khach_hang (1) ←→ (N) van_ban_di
khach_hang (1) ←→ (N) van_ban_den
```
- Một khách hàng có thể có nhiều văn bản đi và văn bản đến
- Văn bản đi/đến có thể liên kết với một khách hàng (hoặc không)

#### 3.3.2. Khách hàng ↔ Hợp đồng
```
khach_hang (1) ←→ (N) hop_dong
```
- Một khách hàng có thể có nhiều hợp đồng
- Mỗi hợp đồng thuộc về một khách hàng (required)

#### 3.3.3. Khách hàng ↔ Công việc
```
khach_hang (1) ←→ (N) cong.viec
```
- Một khách hàng có thể có nhiều công việc
- Công việc tự động liên kết với khách hàng thông qua văn bản đến

#### 3.3.4. Văn bản đến ↔ Công việc
```
van_ban_den (1) ←→ (N) cong.viec
```
- Một văn bản đến có thể tạo nhiều công việc
- Mỗi công việc liên kết với một văn bản đến (required)

### 3.4. Luồng Dữ liệu

#### 3.4.1. Luồng từ Văn bản đến Công việc
```
Văn bản đến (van_ban_den)
    ↓ (có id_khach_hang)
    ↓ (tạo công việc)
Công việc (cong.viec)
    ↓ (van_ban_den_id → id_khach_hang)
    ↓ (tự động tính toán)
khach_hang_id (trong cong_viec_ext)
```

#### 3.4.2. Luồng từ Khách hàng đến Hợp đồng
```
Khách hàng (khach_hang)
    ↓ (tạo hợp đồng)
Hợp đồng (hop_dong)
    ↓ (id_khach_hang)
    ↓ (tính toán trạng thái)
Trạng thái hợp đồng (tự động)
    ↓ (hiển thị văn bản liên quan)
Văn bản đi/đến của khách hàng
```

### 3.5. Tích hợp Dashboard

#### 3.5.1. Dashboard Văn bản
- Hiển thị thống kê về văn bản và công việc
- Không phụ thuộc vào module khách hàng
- Có thể hoạt động độc lập

#### 3.5.2. Dashboard Khách hàng
- Hiển thị thống kê về khách hàng, hợp đồng
- Sử dụng dữ liệu từ cả 2 module
- Hiển thị văn bản có liên kết với khách hàng

---

## 4. TỔNG KẾT

### 4.1. Module Quản lý Văn bản
- **Vai trò:** Module cơ sở, quản lý văn bản và công việc nội bộ
- **Độc lập:** Có thể hoạt động độc lập
- **Mở rộng:** Có thể được mở rộng bởi các module khác

### 4.2. Module Quản lý Khách hàng
- **Vai trò:** Module mở rộng, thêm chức năng quản lý khách hàng và hợp đồng
- **Phụ thuộc:** Phụ thuộc vào module quản lý văn bản
- **Mở rộng:** Mở rộng các model của module quản lý văn bản thông qua `_inherit`

### 4.3. Lợi ích của Kiến trúc
1. **Tách biệt chức năng:** Mỗi module có trách nhiệm rõ ràng
2. **Tái sử dụng:** Module quản lý văn bản có thể được sử dụng độc lập
3. **Mở rộng dễ dàng:** Module khách hàng mở rộng mà không thay đổi code gốc
4. **Tích hợp mượt mà:** Dữ liệu được liên kết tự động và logic
5. **Quản lý tập trung:** Dashboard cung cấp cái nhìn tổng quan

### 4.4. Các Tính năng Nổi bật
- ✅ Tự động tính toán trạng thái công việc
- ✅ Tự động tính toán trạng thái hợp đồng
- ✅ Tự động liên kết công việc với khách hàng
- ✅ Tự động tạo mã số (văn bản, hợp đồng, khách hàng)
- ✅ Dashboard tự động cập nhật
- ✅ Quản lý văn bản theo khách hàng
- ✅ Theo dõi hợp đồng và cảnh báo hết hạn

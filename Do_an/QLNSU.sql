create database QLNSU
on(
	name=QLNSU_mdf,
	filename =  'D:\SQL\QLNSU\QLNSU.mdf',
	size=10,
	maxsize=50,
	filegrowth = 5)
log on(
	name=QLNSU_log,
	filename =  'D:\SQL\QLNSU\QLNSU.ldf',
	size=10,
	maxsize=50,
	filegrowth = 5)

USE QLNSU

CREATE TABLE ChucVu (
    MaCV		VARCHAR(5) PRIMARY KEY,
    TenCV       NVARCHAR(50) NOT NULL,
    LuongCoBan  DECIMAL(18,2) NOT NULL,
    HeSoLuong   DECIMAL(5,2) NOT NULL,
    PhuCap      DECIMAL(18,2) NOT NULL
)

CREATE TABLE NhanVien (
    MaNV        VARCHAR(5) PRIMARY KEY,
    TenNV       NVARCHAR(50) NOT NULL,
    NamSinh		INT NOT NULL,
    GioiTinh    NVARCHAR(5),
    DiaChi      NVARCHAR(200),
    ChucVu      VARCHAR(5) NOT NULL FOREIGN KEY REFERENCES ChucVu(MaCV),
)

CREATE TABLE ChamCong (
    MaCC            VARCHAR(10) PRIMARY KEY,
    MaNV            VARCHAR(5) FOREIGN KEY REFERENCES NhanVien(MaNV) ON DELETE CASCADE,
    NgayChamCong     DATETIME NOT NULL,
    GioVao           TIME NOT NULL,
    GioRa            TIME NULL
)

CREATE TABLE TongKetCC (
    MaTKCC      int Identity PRIMARY KEY,
    MaNV        VARCHAR(5),
    KyLuong     CHAR(6) NOT NULL,     -- dạng YYYYMM
    TongNgayLam INT NOT NULL DEFAULT 0,
    TongGioLam  DECIMAL(10,2) NOT NULL DEFAULT 0,
    NgayTongKet DATE NOT NULL DEFAULT GETDATE(),

    CONSTRAINT FK_TKCC_NhanVien FOREIGN KEY (MaNV)
        REFERENCES NhanVien(MaNV) ON DELETE CASCADE,
    CONSTRAINT UQ_TongKetCC UNIQUE (MaNV, KyLuong)
)
CREATE TABLE TinhLuong (
    MaNV         VARCHAR(5) NOT NULL,
    KyLuong      CHAR(6) NOT NULL,       
    LuongCoBan   DECIMAL(18,2) NOT NULL,
    HeSoLuong    DECIMAL(4,2) NOT NULL,
    PhuCap       DECIMAL(18,2) DEFAULT 0,
    TongLuong    DECIMAL(18,2) NOT NULL,

	CONSTRAINT PK_TinhLuong PRIMARY KEY (MaNV,KyLuong),
    CONSTRAINT FK_TL_NhanVien FOREIGN KEY (MaNV)
        REFERENCES NhanVien(MaNV) ON DELETE CASCADE
)

drop table CHUCVU
drop table NhanVien
drop table ChamCong
drop table TONGKETCC
drop table TINHLUONG
-- Dữ liệu bảng: ChucVu
INSERT INTO ChucVu (MaCV, TenCV, LuongCoBan, HeSoLuong, PhuCap) VALUES ('NVPT', N'Nhân viên phổ thông', 8000000, 1.5, 1000000)
INSERT INTO ChucVu (MaCV, TenCV, LuongCoBan, HeSoLuong, PhuCap) VALUES ('NVCC', N'Nhân viên cao cấp', 12000000, 2, 2000000)
INSERT INTO ChucVu (MaCV, TenCV, LuongCoBan, HeSoLuong, PhuCap) VALUES ('PPH', N'Phó phòng', 18000000, 2.5, 3000000)
INSERT INTO ChucVu (MaCV, TenCV, LuongCoBan, HeSoLuong, PhuCap) VALUES ('TP', N'Trưởng phòng', 25000000, 3, 4000000)
INSERT INTO ChucVu (MaCV, TenCV, LuongCoBan, HeSoLuong, PhuCap) VALUES ('GD', N'Giám đốc', 30000000, 4, 8000000)
SELECT * FROM CHUCVU

-- Dữ liệu bảng: NhanVien
INSERT INTO NhanVien (MaNV, TenNV, NamSinh, GioiTinh, DiaChi, ChucVu) VALUES ('NV001', N'Nguyễn Văn An', 1998, N'Nam', N'Quận 1, TP.HCM', 'NVPT')
INSERT INTO NhanVien (MaNV, TenNV, NamSinh, GioiTinh, DiaChi, ChucVu) VALUES ('NV002', N'Trần Thị Bích', 2001, N'Nữ', N'Quận 3, TP.HCM', 'NVPT')
INSERT INTO NhanVien (MaNV, TenNV, NamSinh, GioiTinh, DiaChi, ChucVu) VALUES ('NV003', N'Phạm Thị Dung', 1999, N'Nữ', N'Quận 7, TP.HCM', 'NVCC')
INSERT INTO NhanVien (MaNV, TenNV, NamSinh, GioiTinh, DiaChi, ChucVu) VALUES ('NV004', N'Hoàng Văn Hùng', 1988, N'Nam', N'Hà Đông, Hà Nội', 'PPH')
INSERT INTO NhanVien (MaNV, TenNV, NamSinh, GioiTinh, DiaChi, ChucVu) VALUES ('NV005', N'Võ Thị Lan', 1992, N'Nữ', N'Thanh Xuân, Hà Nội', 'PPH')
INSERT INTO NhanVien (MaNV, TenNV, NamSinh, GioiTinh, DiaChi, ChucVu) VALUES ('NV006', N'Đặng Văn Nam', 1990, N'Nam', N'Quận 10, TP.HCM', 'TP')
INSERT INTO NhanVien (MaNV, TenNV, NamSinh, GioiTinh, DiaChi, ChucVu) VALUES ('NV007', N'Nguyễn Thị Hạnh', 2000, N'Nữ', N'Ba Đình, Hà Nội', 'NVCC')
INSERT INTO NhanVien (MaNV, TenNV, NamSinh, GioiTinh, DiaChi, ChucVu) VALUES ('NV008', N'Lê Thị Thanh', 1997, N'Nữ', N'Quận 4, TP.HCM', 'NVPT')
INSERT INTO NhanVien (MaNV, TenNV, NamSinh, GioiTinh, DiaChi, ChucVu) VALUES ('NV009', N'Phan Văn Sơn', 1994, N'Nam', N'Quận 6, TP.HCM', 'NVCC')
INSERT INTO NhanVien (MaNV, TenNV, NamSinh, GioiTinh, DiaChi, ChucVu) VALUES ('NV010', N'Đỗ Thị Lan', 1998, N'Nữ', N'Quận 11, TP.HCM', 'NVPT')
INSERT INTO NhanVien (MaNV, TenNV, NamSinh, GioiTinh, DiaChi, ChucVu) VALUES ('NV011', N'Hoàng Văn Quang', 1991, N'Nam', N'Quận 1, TP.HCM', 'TP')
INSERT INTO NhanVien (MaNV, TenNV, NamSinh, GioiTinh, DiaChi, ChucVu) VALUES ('NV012', N'Lê Văn Phúc', 1995, N'Nam', N'Cầu Giấy, Hà Nội', 'NVCC')
INSERT INTO NhanVien (MaNV, TenNV, NamSinh, GioiTinh, DiaChi, ChucVu) VALUES ('NV013', N'Nguyễn Thị Mai', 1985, N'Nữ', N'Quận 3, TP.HCM', 'GD')
SELECT * FROM NHANVIEN

-- Dữ liệu bảng: ChamCong 
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C001250611', 'NV001', '2025-06-11', '08:08:00', '17:10:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C002250611', 'NV002', '2025-06-11', '08:52:00', '17:05:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C003250611', 'NV003', '2025-06-11', '08:15:00', '17:58:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C004250611', 'NV004', '2025-06-11', '08:33:00', '17:42:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C005250611', 'NV005', '2025-06-11', '08:41:00', '17:15:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C006250611', 'NV006', '2025-06-11', '08:29:00', '17:33:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C007250611', 'NV007', '2025-06-11', '08:05:00', '17:50:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C008250611', 'NV008', '2025-06-11', '08:59:00', '17:28:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C009250611', 'NV009', '2025-06-11', '08:12:00', '17:45:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C010250611', 'NV010', '2025-06-11', '08:44:00', '17:09:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C011250611', 'NV011', '2025-06-11', '08:36:00', '17:55:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C012250611', 'NV012', '2025-06-11', '08:22:00', '17:30:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C013250611', 'NV013', '2025-06-11', '08:07:00', '17:18:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C001250612', 'NV001', '2025-06-12', '08:35:00', '17:48:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C002250612', 'NV002', '2025-06-12', '08:19:00', '17:22:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C003250612', 'NV003', '2025-06-12', '08:50:00', '17:06:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C004250612', 'NV004', '2025-06-12', '08:04:00', '17:55:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C005250612', 'NV005', '2025-06-12', '08:28:00', '17:39:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C006250612', 'NV006', '2025-06-12', '08:16:00', '17:14:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C007250612', 'NV007', '2025-06-12', '08:42:00', '17:28:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C008250612', 'NV008', '2025-06-12', '08:55:00', '17:02:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C009250612', 'NV009', '2025-06-12', '08:09:00', '17:46:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C010250612', 'NV010', '2025-06-12', '08:33:00', '17:59:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C011250612', 'NV011', '2025-06-12', '08:47:00', '17:34:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C012250612', 'NV012', '2025-06-12', '08:12:00', '17:11:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C013250612', 'NV013', '2025-06-12', '08:25:00', '17:50:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C001250613', 'NV001', '2025-06-13', '08:59:00', '17:20:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C002250613', 'NV002', '2025-06-13', '08:14:00', '17:58:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C003250613', 'NV003', '2025-06-13', '08:38:00', '17:35:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C004250613', 'NV004', '2025-06-13', '08:25:00', '17:10:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C005250613', 'NV005', '2025-06-13', '08:02:00', '17:48:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C006250613', 'NV006', '2025-06-13', '08:49:00', '17:26:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C007250613', 'NV007', '2025-06-13', '08:18:00', '17:05:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C008250613', 'NV008', '2025-06-13', '08:55:00', '17:39:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C009250613', 'NV009', '2025-06-13', '08:31:00', '17:52:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C010250613', 'NV010', '2025-06-13', '08:07:00', '17:15:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C011250613', 'NV011', '2025-06-13', '08:43:00', '17:44:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C012250613', 'NV012', '2025-06-13', '08:56:00', '17:03:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C013250613', 'NV013', '2025-06-13', '08:12:00', '17:29:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C001250616', 'NV001', '2025-06-16', '08:01:00', '17:32:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C002250616', 'NV002', '2025-06-16', '08:44:00', '17:56:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C003250616', 'NV003', '2025-06-16', '08:29:00', '17:19:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C004250616', 'NV004', '2025-06-16', '08:52:00', '17:45:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C005250616', 'NV005', '2025-06-16', '08:17:00', '17:08:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C006250616', 'NV006', '2025-06-16', '08:35:00', '17:27:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C007250616', 'NV007', '2025-06-16', '08:58:00', '17:54:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C008250616', 'NV008', '2025-06-16', '08:09:00', '17:41:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C009250616', 'NV009', '2025-06-16', '08:41:00', '17:13:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C010250616', 'NV010', '2025-06-16', '08:25:00', '17:39:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C011250616', 'NV011', '2025-06-16', '08:12:00', '17:02:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C012250616', 'NV012', '2025-06-16', '08:47:00', '17:51:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C013250616', 'NV013', '2025-06-16', '08:33:00', '17:24:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C001250617', 'NV001', '2025-06-17', '08:55:00', '17:17:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C002250617', 'NV002', '2025-06-17', '08:31:00', '17:01:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C003250617', 'NV003', '2025-06-17', '08:31:00', '17:36:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C004250617', 'NV004', '2025-06-17', '08:11:00', '17:24:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C005250617', 'NV005', '2025-06-17', '08:48:00', '17:01:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C006250617', 'NV006', '2025-06-17', '08:00:00', '17:45:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C007250617', 'NV007', '2025-06-17', '08:25:00', '17:30:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C008250617', 'NV008', '2025-06-17', '08:06:00', '17:53:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C009250617', 'NV009', '2025-06-17', '08:29:00', '17:39:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C010250617', 'NV010', '2025-06-17', '08:19:00', '17:17:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C011250617', 'NV011', '2025-06-17', '08:29:00', '17:39:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C012250617', 'NV012', '2025-06-17', '08:58:00', '17:26:00')
INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES ('C013250617', 'NV013', '2025-06-17', '08:44:00', '17:41:00')
SELECT * FROM CHAMCONG

-- Dữ liệu bảng: TongKetCC
SELECT * FROM TONGKETCC

-- Dữ liệu bảng: TinhLuong
SELECT * FROM TINHLUONG

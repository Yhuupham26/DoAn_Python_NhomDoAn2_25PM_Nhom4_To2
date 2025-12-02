import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import pyodbc
from datetime import datetime
import pandas as pd

# Cấu hình kết nối SQL Server
DATABASE_CONFIG = {
    'server': 'LAPTOP-BFT3IU81\\SQLEXPRESS',
    'database': 'QLNSU',
    'driver': '{ODBC Driver 17 for SQL Server}',
    'trusted_connection': 'yes'
}

def db_build_connection_string():# Hàm xây dựng chuỗi kết nối đến SQL Server
    return (
        f"DRIVER={DATABASE_CONFIG['driver']};"
        f"SERVER={DATABASE_CONFIG['server']};"
        f"DATABASE={DATABASE_CONFIG['database']};"
        "Trusted_Connection=yes;"
    )

def db_get_connection():# Hàm kết nối đến cơ sở dữ liệu SQL Server
    try:
        conn_str = db_build_connection_string()
        return pyodbc.connect(conn_str)
    except pyodbc.Error as e:
        raise Exception(f"Lỗi kết nối SQL Server: {e}")
    
''' Quản lý chức vụ '''
# Hàm tải dữ liệu chức vụ từ cơ sở dữ liệu
def db_load_ChucVu():
    try:
        conn = db_get_connection()
        cur = conn.cursor()
        cur.execute("SELECT MaCV, TenCV, LuongCoBan, HeSoLuong, PhuCap FROM ChucVu ORDER BY MaCV")
        rows = cur.fetchall()
        result = [
            {
                "MaCV": row[0],
                "TenCV": row[1],
                "LuongCoBan": row[2],
                "HeSoLuong": row[3],
                "PhuCap": row[4]
            }
            for row in rows
        ]
        conn.close()
        return result
    except pyodbc.Error as e:
        raise Exception(f"Lỗi tải chức vụ: {e}")

# Hàm tái tính lương cho nhân viên theo chức vụ
def TinhLai_luong_chucvu(ma_cv):
    try:
        conn = db_get_connection()
        cur = conn.cursor()
        cur.execute("SELECT MaNV FROM NhanVien WHERE chucvu = ?", (ma_cv,))
        rows = cur.fetchall()
        conn.close()
        for r in rows:
            db_TinhLai_nv_all_kyLuong(r[0])
    except Exception:
        pass

#Hàm thêm chức vụ mới vào cơ sở dữ liệu 
def db_Them_ChucVu(ChucVu_list):
    try:
        conn = db_get_connection()
        cur = conn.cursor()
        query = "INSERT INTO ChucVu (MaCV, TenCV, LuongCoBan, HeSoLuong, PhuCap) VALUES (?, ?, ?, ?, ?)"
        cur.execute(query, ChucVu_list)
        conn.commit()
        conn.close()
        # Tái tính lương cho nhân viên thuộc chức vụ này
        TinhLai_luong_chucvu(ChucVu_list[0])
    except pyodbc.Error as e:
        raise Exception(f"Lỗi thêm chức vụ: {e}")

#Hàm cập nhật thông tin chức vụ trong cơ sở dữ liệu
def db_CapNhat_ChucVu(ChucVu_list):
    try:
        conn = db_get_connection()
        cur = conn.cursor()
        query = """
            UPDATE ChucVu
            SET TenCV = ?, LuongCoBan = ?, HeSoLuong = ?, PhuCap = ?
            WHERE MaCV = ?
        """
        cur.execute(query, (ChucVu_list[1], ChucVu_list[2], ChucVu_list[3], ChucVu_list[4], ChucVu_list[0]))
        conn.commit()
        conn.close()
        # Tái tính lương cho nhân viên thuộc chức vụ này
        TinhLai_luong_chucvu(ChucVu_list[0])
    except pyodbc.Error as e:
        raise Exception(f"Lỗi cập nhật chức vụ: {e}")

#Hàm xóa chức vụ khỏi cơ sở dữ liệu
def db_Xoa_ChucVu(MaCV):
    try:
        conn = db_get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM ChucVu WHERE MaCV = ?", (MaCV,))
        conn.commit() 
        conn.close()
    except pyodbc.Error as e:
        raise Exception(f"Lỗi xóa chức vụ: {e}")

''' Quản lý nhân viên'''
# Hàm tải dữ liệu nhân viên từ cơ sở dữ liệu 
def db_load_NhanVien():
    try:
        conn = db_get_connection()
        cur = conn.cursor()
        cur.execute("SELECT MaNV, TenNV, Namsinh, gioitinh, diachi, chucvu FROM NhanVien ORDER BY MaNV")
        rows = cur.fetchall()
        result = [
            {
                "MaNV": row[0],
                "TenNV": row[1],
                "Namsinh": row[2],
                "gioitinh": row[3],
                "diachi": row[4],
                "chucvu": row[5],
            }
            for row in rows
        ]
        conn.close()
        return result
    except pyodbc.Error as e:
        raise Exception(f"Lỗi tải nhân viên: {e}")

# Hàm thêm nhân viên mới vào cơ sở dữ liệu    
def db_Them_NhanVien(NhanVien_list):
    try:
        conn = db_get_connection()
        cur = conn.cursor()
        query = "INSERT INTO NhanVien (MaNV, TenNV, Namsinh, gioitinh, diachi, chucvu) VALUES (?, ?, ?, ?, ?, ?)"
        cur.execute(query, NhanVien_list)
        conn.commit()
        conn.close()
        # Tái tính lương cho nhân viên mới
        db_TinhLai_nv_all_kyLuong(NhanVien_list[0])
    except pyodbc.Error as e:
        raise Exception(f"Lỗi thêm nhân viên: {e}")

# Hàm cập nhật thông tin nhân viên trong cơ sở dữ liệu
def db_CapNhat_NhanVien(NhanVien_list):
    try:
        conn = db_get_connection()
        cur = conn.cursor()
        query = """
            UPDATE NhanVien
            SET TenNV = ?, Namsinh = ?, gioitinh = ?, diachi = ?, chucvu = ?
            WHERE MaNV = ?
        """
        cur.execute(query, (NhanVien_list[1], NhanVien_list[2], NhanVien_list[3], 
                            NhanVien_list[4], NhanVien_list[5], NhanVien_list[0]))
        conn.commit()
        conn.close()
        # Tái tính lương cho nhân viên
        db_TinhLai_nv_all_kyLuong(NhanVien_list[0])
    except pyodbc.Error as e:
        raise Exception(f"Lỗi cập nhật nhân viên: {e}")

# Hàm xóa nhân viên khỏi cơ sở dữ liệu
def db_Xoa_NhanVien(MaNV):
    try:
        conn = db_get_connection()
        cur = conn.cursor()
        # Xóa các bản ghi liên quan trước
        cur.execute("SELECT COUNT(*) FROM ChamCong WHERE MaNV = ?", (MaNV,))
        chamcong_count = cur.fetchone()[0]
        if chamcong_count > 0:
            cur.execute("DELETE FROM TinhLuong WHERE MaNV = ?", (MaNV,))
            cur.execute("DELETE FROM TongKetCC WHERE MaNV = ?", (MaNV,))
            cur.execute("DELETE FROM ChamCong WHERE MaNV = ?", (MaNV,))
        cur.execute("DELETE FROM NhanVien WHERE MaNV = ?", (MaNV,))
        conn.commit() 
        conn.close()
    except pyodbc.Error as e:
        raise Exception(f"Lỗi xóa nhân viên: {e}")

# Hàm tìm kiếm nhân viên trong cơ sở dữ liệu
def db_TimKiem_NhanVien(keyword):
    try:
        conn = db_get_connection()
        cur = conn.cursor()
        query = """
            SELECT MaNV, TenNV, Namsinh, gioitinh, diachi, chucvu
            FROM NhanVien
            WHERE MaNV LIKE ? OR TenNV LIKE ?
            ORDER BY MaNV
        """
        like_keyword = f"%{keyword}%"
        cur.execute(query, (like_keyword, like_keyword))
        rows = cur.fetchall()
        result = [
            {
                "MaNV": row[0],
                "TenNV": row[1],
                "Namsinh": row[2],
                "gioitinh": row[3],
                "diachi": row[4],
                "chucvu": row[5],
            }
            for row in rows
        ]
        conn.close()
        return result
    except pyodbc.Error as e:
        raise Exception(f"Lỗi tìm kiếm nhân viên: {e}")

''' Quản lý chấm công '''
# Hàm tải dữ liệu chấm công từ cơ sở dữ liệu
def db_load_ChamCong():
    try:
        conn = db_get_connection()
        cur = conn.cursor()
        cur.execute("SELECT MaCC, MaNV, NgayChamCong, GioVao, GioRa FROM ChamCong ORDER BY MaCC")
        rows = cur.fetchall()
        result = [
            {
                "MaCC": row[0],
                "MaNV": row[1],
                "NgayChamCong": row[2],
                "GioVao": row[3],
                "GioRa": row[4]
            }
            for row in rows
        ]
        conn.close()
        return result
    except pyodbc.Error as e:
        raise Exception(f"Lỗi tải chấm công: {e}")

# Hàm parse ngày từ string
def DinhDang_date(ngay):
    try:
        return datetime.strptime(str(ngay), "%Y-%m-%d")
    except Exception:
        try:
            return datetime.strptime(str(ngay), "%Y-%m-%d %H:%M:%S")
        except Exception:
            return None

# Hàm tái tính lương theo ngày chấm công
def TinhLai_luong_Ngay(ma_nv, ngay):
    dt = DinhDang_date(ngay)
    if dt:
        db_Tinh_Luong_Thang(dt.month, dt.year, ma_nv)
    else:
        db_TinhLai_nv_all_kyLuong(ma_nv)

# Hàm thêm bản ghi chấm công mới vào cơ sở dữ liệu
def db_Them_ChamCong(ChamCong_list):
    try:
        conn = db_get_connection()
        cur = conn.cursor()
        query = "INSERT INTO ChamCong (MaCC, MaNV, NgayChamCong, GioVao, GioRa) VALUES (?, ?, ?, ?, ?)"
        cur.execute(query, ChamCong_list)
        conn.commit()
        conn.close()
        # Tái tính lương cho tháng tương ứng
        TinhLai_luong_Ngay(ChamCong_list[1], ChamCong_list[2])
    except pyodbc.Error as e:
        raise Exception(f"Lỗi thêm chấm công: {e}")

# Hàm cập nhật bản ghi chấm công trong cơ sở dữ liệu
def db_CapNhat_ChamCong(ChamCong_list):
    try:
        conn = db_get_connection()
        cur = conn.cursor()
        query = """
            UPDATE ChamCong
            SET MaNV = ?, NgayChamCong = ?, GioVao = ?, GioRa = ?
            WHERE MaCC = ?
        """
        cur.execute(query, (ChamCong_list[1], ChamCong_list[2], ChamCong_list[3], 
                            ChamCong_list[4], ChamCong_list[0]))
        conn.commit()
        conn.close()
        # Tái tính lương cho tháng tương ứng
        TinhLai_luong_Ngay(ChamCong_list[1], ChamCong_list[2])
    except pyodbc.Error as e:
        raise Exception(f"Lỗi cập nhật chấm công: {e}")

# Hàm xóa bản ghi chấm công khỏi cơ sở dữ liệu
def db_Xoa_ChamCong(MaCC):
    try:
        conn = db_get_connection()
        cur = conn.cursor()
        # Lấy thông tin trước khi xóa để tái tính lương
        cur.execute("SELECT MaNV, NgayChamCong FROM ChamCong WHERE MaCC = ?", (MaCC,))
        row = cur.fetchone()
        Ma_nv, date_CC = (row[0], row[1]) if row else (None, None)
        
        cur.execute("DELETE FROM ChamCong WHERE MaCC = ?", (MaCC,))
        conn.commit() 
        conn.close()
        
        # Tái tính lương nếu biết nhân viên và ngày
        if Ma_nv and date_CC:
            TinhLai_luong_Ngay(Ma_nv, date_CC)
    except pyodbc.Error as e:
        raise Exception(f"Lỗi xóa chấm công: {e}")

# Hàm tìm kiếm bản ghi chấm công trong cơ sở dữ liệu
def db_TimKiem_ChamCong(keyword):
    try:
        conn = db_get_connection()
        cur = conn.cursor()
        query = """
            SELECT MaCC, MaNV, NgayChamCong, GioVao, GioRa
            FROM ChamCong
            WHERE MaCC LIKE ? OR MaNV LIKE ?
            ORDER BY MaCC
        """
        like_keyword = f"%{keyword}%"
        cur.execute(query, (like_keyword, like_keyword))
        rows = cur.fetchall()
        result = [
            {
                "MaCC": row[0],
                "MaNV": row[1],
                "NgayChamCong": row[2],
                "GioVao": row[3],
                "GioRa": row[4]
            }
            for row in rows
        ]
        conn.close()
        return result
    except pyodbc.Error as e:
        raise Exception(f"Lỗi tìm kiếm chấm công: {e}")

# Hàm xuất dữ liệu chấm công ra file CSV
def db_Xuat_CSV_ChamCong(file_path):    
    try:
        conn = db_get_connection()
        cur = conn.cursor()
        cur.execute("SELECT MaCC, MaNV, NgayChamCong, GioVao, GioRa FROM ChamCong ORDER BY MaCC")
        rows = cur.fetchall()
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["MaCC", "MaNV", "NgayChamCong", "GioVao", "GioRa"])
            for row in rows:
                writer.writerow(row)
        conn.close()
    except pyodbc.Error as e:
        raise Exception(f"Lỗi xuất CSV chấm công: {e}")
    
# Hàm xuất dữ liệu chấm công ra file Excel
def db_Xuat_Excel_ChamCong(file_path):    
    try:
        conn = db_get_connection()
        query = "SELECT MaCC, MaNV, NgayChamCong, GioVao, GioRa FROM ChamCong ORDER BY MaCC"
        df = pd.read_sql(query, conn)
        df.to_excel(file_path, index=False)
        conn.close()
    except pyodbc.Error as e:
        raise Exception(f"Lỗi xuất Excel chấm công: {e}")

''' Tổng kết chấm công '''
# Hàm tải dữ liệu tổng kết chấm công từ cơ sở dữ liệu
def db_load_TongKetCC():
    try:
        conn = db_get_connection()
        cur = conn.cursor()
        cur.execute("SELECT MaTKCC, MaNV, KyLuong, TongNgayLam, TongGioLam, NgayTongKet FROM TongKetCC ORDER BY MaTKCC")
        rows = cur.fetchall()
        result = [
            {
                "MaTKCC": row[0],
                "MaNV": row[1],
                "KyLuong": row[2],
                "TongNgayLam": row[3],
                "TongGioLam": row[4],
                "NgayTongKet": row[5]
            }
            for row in rows
        ]
        conn.close()
        return result
    except pyodbc.Error as e:
        raise Exception(f"Lỗi tải tổng kết chấm công: {e}")

# Hàm tính tổng kết chấm công của một nhân viên
def db_Tinh_TongKetCC(MaNV, Thang, Nam):
    try:
        conn = db_get_connection()
        cur = conn.cursor()
        query = """
            SELECT 
                COUNT(DISTINCT NgayChamCong) AS TongNgayLam,
                CAST(SUM(DATEDIFF(MINUTE, GioVao, GioRa)) / 60.0 AS DECIMAL(10,2)) AS TongGioLam
            FROM ChamCong
            WHERE MaNV = ? AND MONTH(NgayChamCong) = ? AND YEAR(NgayChamCong) = ?
        """
        cur.execute(query, (MaNV, Thang, Nam))
        row = cur.fetchone()
        conn.close()
        return (row[0], row[1]) if row else (0, 0)
    except pyodbc.Error as e:
        raise Exception(f"Lỗi tính tổng kết chấm công: {e}")

# Hàm tự động tạo bản ghi tổng kết chấm công cho tất cả nhân viên trong tháng
def db_Tao_TongKetCC_Thang(Thang, Nam):
    try:
        conn = db_get_connection()
        cur = conn.cursor()
        cur.execute("SELECT MaNV FROM NhanVien")
        ds_nv = cur.fetchall()
        
        for row in ds_nv:
            MaNV = row[0]
            TongNgayLam, TongGioLam = db_Tinh_TongKetCC(MaNV, Thang, Nam)
            KyLuong = f"{Nam}{Thang:02d}"
            insert_query = """
                INSERT INTO TongKetCC (MaNV, KyLuong, TongNgayLam, TongGioLam, NgayTongKet)
                VALUES (?, ?, ?, ?, GETDATE())
            """
            cur.execute(insert_query, (MaNV, KyLuong, TongNgayLam, TongGioLam))
        conn.commit()
        conn.close()
    except pyodbc.Error as e:
        raise Exception(f"Lỗi tạo tổng kết chấm công tháng: {e}")

# Tạo bản ghi tổng kết chấm công cho một nhân viên cụ thể
def db_Tao_TongKetCC_ChoNV(Thang, Nam, MaNV):
    try:
        conn = db_get_connection()
        cur = conn.cursor()
        TongNgayLam, TongGioLam = db_Tinh_TongKetCC(MaNV, Thang, Nam)
        KyLuong = f"{Nam}{Thang:02d}"
        
        # Kiểm tra đã tồn tại chưa
        cur.execute("SELECT COUNT(1) FROM TongKetCC WHERE MaNV = ? AND KyLuong = ?", (MaNV, KyLuong))
        exists = cur.fetchone()[0]
        
        if exists:
            update_q = "UPDATE TongKetCC SET TongNgayLam = ?, TongGioLam = ?, NgayTongKet = GETDATE() WHERE MaNV = ? AND KyLuong = ?"
            cur.execute(update_q, (TongNgayLam, TongGioLam, MaNV, KyLuong))
        else:
            insert_query = "INSERT INTO TongKetCC (MaNV, KyLuong, TongNgayLam, TongGioLam, NgayTongKet) VALUES (?, ?, ?, ?, GETDATE())"
            cur.execute(insert_query, (MaNV, KyLuong, TongNgayLam, TongGioLam))
        conn.commit()
        conn.close()
    except pyodbc.Error as e:
        raise Exception(f"Lỗi tạo/tái tạo tổng kết chấm công cho nhân viên: {e}")

# Hàm xóa bản ghi tổng kết chấm công khỏi cơ sở dữ liệu
def db_Xoa_TongKetCC(MaTK):
    try:
        conn = db_get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM TongKetCC WHERE MaTKCC = ?", (MaTK,))
        conn.commit() 
        conn.close()
    except pyodbc.Error as e:
        raise Exception(f"Lỗi xóa tổng kết chấm công: {e}")

# Hàm xóa tất cả bản ghi tổng kết chấm công
def db_Xoa_TongKetCC_All():
    try:
        conn = db_get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM TongKetCC")
        conn.commit()
        conn.close()
    except pyodbc.Error as e:
        raise Exception(f"Lỗi xóa tất cả tổng kết chấm công: {e}")

# Hàm tìm kiếm bản ghi tổng kết chấm công trong cơ sở dữ liệu
def db_TimKiem_TongKetCC(keyword):
    try:
        conn = db_get_connection()
        cur = conn.cursor()
        query = """
            SELECT MaTKCC, MaNV, KyLuong, TongNgayLam, TongGioLam, NgayTongKet
            FROM TongKetCC
            WHERE MaTKCC LIKE ? OR MaNV LIKE ?
            ORDER BY MaTKCC
        """
        like_keyword = f"%{keyword}%"
        cur.execute(query, (like_keyword, like_keyword))
        rows = cur.fetchall()
        result = [
            {
                "MaTKCC": row[0],
                "MaNV": row[1],
                "KyLuong": row[2],
                "TongNgayLam": row[3],
                "TongGioLam": row[4],
                "NgayTongKet": row[5]
            }
            for row in rows
        ]
        conn.close()
        return result
    except pyodbc.Error as e:
        raise Exception(f"Lỗi tìm kiếm tổng kết chấm công: {e}")

# Hàm xuất dữ liệu tổng kết chấm công ra file CSV
def db_Xuat_CSV_TongKetCC(file_path):    
    try:
        conn = db_get_connection()
        cur = conn.cursor()
        cur.execute("SELECT MaTKCC, MaNV, KyLuong, TongNgayLam, TongGioLam, NgayTongKet FROM TongKetCC ORDER BY MaTKCC")
        rows = cur.fetchall()
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["MaTKCC", "MaNV", "KyLuong", "TongNgayLam", "TongGioLam", "NgayTongKet"])
            for row in rows:
                writer.writerow(row)
        conn.close()
    except pyodbc.Error as e:
        raise Exception(f"Lỗi xuất CSV tổng kết chấm công: {e}")
    
# Hàm xuất dữ liệu tổng kết chấm công ra file Excel
def db_Xuat_Excel_TongKetCC(file_path):    
    try:
        conn = db_get_connection()
        query = "SELECT MaTKCC, MaNV, KyLuong, TongNgayLam, TongGioLam, NgayTongKet FROM TongKetCC ORDER BY MaTKCC"
        df = pd.read_sql(query, conn)
        df.to_excel(file_path, index=False)
        conn.close()
    except pyodbc.Error as e:
        raise Exception(f"Lỗi xuất Excel tổng kết chấm công: {e}")

def db_TinhLai_nv_all_kyLuong(MaNV):
    """Tái tính lại tất cả các kỳ lương hiện có cho một nhân viên."""
    try:
        conn = db_get_connection()
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT KyLuong FROM TinhLuong WHERE MaNV = ?", (MaNV,))
        rows = cur.fetchall()
        ks = [r[0] for r in rows]
        conn.close()
        
        if not ks:
            # Nếu không có kỳ lương, tính cho tháng hiện tại
            thang = datetime.now().month
            nam = datetime.now().year
            db_Tinh_Luong_Thang(thang, nam, MaNV)
        else:
            for kyLuong in ks:
                try:
                    if len(kyLuong) == 6:
                        nam = int(kyLuong[:4])
                        thang = int(kyLuong[4:6])
                        db_Tinh_Luong_Thang(thang, nam, MaNV)
                except Exception:
                    continue
    except Exception:
        pass

''' Quản lý tính lương '''
# Hàm tải dữ liệu tính lương từ cơ sở dữ liệu
def db_load_TinhLuong():
    try:
        conn = db_get_connection()
        cur = conn.cursor()
        cur.execute("SELECT MaNV, KyLuong, LuongCoBan, HeSoLuong, PhuCap, TongLuong FROM TinhLuong ORDER BY MaNV, KyLuong")
        rows = cur.fetchall()
        result = [
            {
                "MaNV": row[0],
                "KyLuong": row[1],
                "LuongCoBan": row[2],
                "HeSoLuong": row[3],
                "PhuCap": row[4],
                "TongLuong": row[5]
            }
            for row in rows
        ]
        conn.close()
        return result
    except pyodbc.Error as e:
        raise Exception(f"Lỗi tải tính lương: {e}")

def db_Tao_KyLuong(Thang, Nam):# Tạo định dạng KyLuong YYYYMM
    return f"{Nam}{Thang:02d}"

def db_Tinh_Luong_Thang(Thang, Nam, MaNV=None):# Hàm tính lương cho tất cả nhân viên và tự động cập nhật vào cơ sở dữ liệu
    try:
        conn = db_get_connection()
        cur = conn.cursor()
        # Lấy danh sách nhân viên
        if MaNV:
            query = """
                SELECT NV.MaNV, CV.LuongCoBan, CV.HeSoLuong, CV.PhuCap
                FROM NhanVien NV
                JOIN ChucVu CV ON NV.chucvu = CV.MaCV
                WHERE NV.MaNV = ?
            """
            cur.execute(query, (MaNV,))
        else:
            query = """
                SELECT NV.MaNV, CV.LuongCoBan, CV.HeSoLuong, CV.PhuCap
                FROM NhanVien NV
                JOIN ChucVu CV ON NV.chucvu = CV.MaCV
            """
            cur.execute(query)
        
        ds_nv = cur.fetchall()   
        for row in ds_nv:
            nv_ma = row[0]
            LuongCoBan = row[1]
            HeSoLuong = row[2]
            PhuCap = row[3] or 0
            
            # Tính tổng giờ làm
            TongGioLam = db_Tinh_TongKetCC(nv_ma, Thang, Nam)[1] or 0
            
            # Tính tổng lương
            tien_cong_gio = (float(LuongCoBan) / 26.0 / 8.0) * float(HeSoLuong) * float(TongGioLam)
            TongLuong = tien_cong_gio + float(PhuCap)
            KyLuong = db_Tao_KyLuong(Thang, Nam)   
            
            # Xóa bản ghi cũ nếu tồn tại
            cur.execute("DELETE FROM TinhLuong WHERE MaNV = ? AND KyLuong = ?", (nv_ma, KyLuong))  
            
            # Chèn bản ghi mới
            cur.execute("""
                INSERT INTO TinhLuong (MaNV, KyLuong, LuongCoBan, HeSoLuong, PhuCap, TongLuong)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (nv_ma, KyLuong, LuongCoBan, HeSoLuong, PhuCap, TongLuong))  
        
        conn.commit()
        conn.close()
    except pyodbc.Error as e:
        raise Exception(f"Lỗi tính lương tháng: {e}")

# Hàm xóa bản ghi tính lương khỏi cơ sở dữ liệu
def db_Xoa_TinhLuong(MaNV):
    try:
        conn = db_get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM TinhLuong WHERE MaNV = ?", (MaNV,))
        conn.commit() 
        conn.close()
    except pyodbc.Error as e:
        raise Exception(f"Lỗi xóa tính lương: {e}")

# Hàm xóa bản ghi tính lương theo MaNV và KyLuong
def db_Xoa_TinhLuong_TheoKy(MaNV, KyLuong):
    try:
        conn = db_get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM TinhLuong WHERE MaNV = ? AND KyLuong = ?", (MaNV, KyLuong))
        conn.commit()
        conn.close()
    except pyodbc.Error as e:
        raise Exception(f"Lỗi xóa tính lương theo kỳ: {e}")

# Hàm xóa tất cả bản ghi tính lương
def db_Xoa_TinhLuong_All():
    try:
        conn = db_get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM TinhLuong")
        conn.commit()
        conn.close()
    except pyodbc.Error as e:
        raise Exception(f"Lỗi xóa tất cả tính lương: {e}")

# Hàm tìm kiếm bản ghi tính lương trong cơ sở dữ liệu
def db_TimKiem_TinhLuong(keyword):
    try:
        conn = db_get_connection()
        cur = conn.cursor()
        query = """
            SELECT MaNV, KyLuong, LuongCoBan, HeSoLuong, PhuCap, TongLuong
            FROM TinhLuong
            WHERE MaNV LIKE ?
            ORDER BY MaNV, KyLuong
        """
        like_keyword = f"%{keyword}%"
        cur.execute(query, (like_keyword,))
        rows = cur.fetchall()
        result = [
            {
                "MaNV": row[0],
                "KyLuong": row[1],
                "LuongCoBan": row[2],
                "HeSoLuong": row[3],
                "PhuCap": row[4],
                "TongLuong": row[5]
            }
            for row in rows
        ]
        conn.close()
        return result
    except pyodbc.Error as e:
        raise Exception(f"Lỗi tìm kiếm tính lương: {e}")

# Hàm xuất dữ liệu tính lương ra file Excel
def db_Xuat_Excel_TinhLuong(file_path):    
    try:
        conn = db_get_connection()
        query = "SELECT MaNV, KyLuong, LuongCoBan, HeSoLuong, PhuCap, TongLuong FROM TinhLuong ORDER BY MaNV, KyLuong"
        df = pd.read_sql(query, conn)
        df.to_excel(file_path, index=False)
        conn.close()
    except pyodbc.Error as e:
        raise Exception(f"Lỗi xuất Excel tính lương: {e}")

# Hàm xuất dữ liệu tính lương ra file CSV
def db_Xuat_CSV_TinhLuong(file_path):    
    try:
        conn = db_get_connection()
        cur = conn.cursor()
        cur.execute("SELECT MaNV, KyLuong, LuongCoBan, HeSoLuong, PhuCap, TongLuong FROM TinhLuong ORDER BY MaNV, KyLuong")
        rows = cur.fetchall()
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["MaNV", "KyLuong", "LuongCoBan", "HeSoLuong", "PhuCap", "TongLuong"])
            for row in rows:
                writer.writerow(row)
        conn.close()
    except pyodbc.Error as e:
        raise Exception(f"Lỗi xuất CSV tính lương: {e}")

# Dinh dang tien te
def DinhDang_Tien(tien):# Hàm định dạng tiền tệ
    try:
        if tien is None:
            return "0"
        return "{:,}".format(int(tien)).replace(",", " ")
    except Exception:
        return tien

class QLNSU_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hệ Thống Quản Lý Nhân Sự")
        self.root.geometry("1200x700")
        self.root.resizable(True, True)
        
        # Tạo style cho ứng dụng
        self.style = ttk.Style()
        try:
            self.style.theme_use('clam')
        except:
            pass
        
        # Cấu hình màu sắc
        self.style.configure('TFrame', background="#34495e")
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#2c3e50', foreground='white')
        self.style.configure('Header.TLabel', font=('Arial', 12, 'bold'), background='#34495e', foreground='white')
        
        # Tạo layout chính
        self.create_main_layout()
        
    def create_main_layout(self):
        """Tạo layout chính của giao diện"""
        # Panel trên - Tiêu đề
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title_label = ttk.Label(header_frame, text="QUẢN LÝ NHÂN SỰ", style='Header.TLabel', font=('TIME NEW ROMA', 20, 'bold'))
        title_label.pack(pady=10)
        
        # Frame chính chứa notebook
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Tạo Notebook (Tab)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tạo các tab
        self.tao_chuc_vu_tab()
        self.tao_nhan_vien_tab()
        self.tao_cham_cong_tab()
        self.tao_tong_ket_tab()
        self.tao_tinh_luong_tab()

    def tao_chuc_vu_tab(self):
        """Tab quản lý chức vụ"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Chức Vụ")
        
        # Frame bảng dữ liệu
        table_frame = ttk.LabelFrame(frame, text="Danh Sách Chức Vụ", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Frame input
        input_frame = ttk.LabelFrame(frame, text="Thông Tin Chức Vụ", padding=10)
        input_frame.pack(fill=tk.Y, padx=10, pady=5)
        
        ttk.Label(input_frame, text="Mã CV:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.cv_macv = ttk.Entry(input_frame, width=20)
        self.cv_macv.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Tên CV:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.cv_tencv = ttk.Entry(input_frame, width=20)
        self.cv_tencv.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Lương Cơ Bản:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.cv_luongcb = ttk.Entry(input_frame, width=20)
        self.cv_luongcb.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Hệ Số Lương:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        self.cv_hesolg = ttk.Entry(input_frame, width=20)
        self.cv_hesolg.grid(row=1, column=3, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Phụ Cấp:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.cv_phucap = ttk.Entry(input_frame, width=20)
        self.cv_phucap.grid(row=2, column=1, padx=5, pady=5)
        
        # Frame nút bấm
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=3, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame, text="Thêm", command=self.Them_chucvu).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cập Nhật", command=self.CapNhat_chucvu).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Xóa", command=self.Xoa_chucvu).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Làm Mới", command=self.LamMoi_chucvu).pack(side=tk.LEFT, padx=5)
        
        
        # Tạo Treeview
        self.cv_tree = ttk.Treeview(table_frame, columns=('MaCV', 'TenCV', 'LuongCoBan', 'HeSoLuong', 'PhuCap'), 
                                     height=15, show='headings')
        self.cv_tree.column('MaCV', width=80, anchor=tk.CENTER)
        self.cv_tree.column('TenCV', width=150, anchor=tk.W)
        self.cv_tree.column('LuongCoBan', width=120, anchor=tk.E)
        self.cv_tree.column('HeSoLuong', width=100, anchor=tk.E)
        self.cv_tree.column('PhuCap', width=100, anchor=tk.E)
        
        self.cv_tree.heading('MaCV', text='Mã CV')
        self.cv_tree.heading('TenCV', text='Tên CV')
        self.cv_tree.heading('LuongCoBan', text='Lương Cơ Bản')
        self.cv_tree.heading('HeSoLuong', text='Hệ Số Lương')
        self.cv_tree.heading('PhuCap', text='Phụ Cấp')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.cv_tree.yview)
        self.cv_tree.configure(yscroll=scrollbar.set)
        
        self.cv_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double click để chọn dữ liệu
        self.cv_tree.bind('<Double-1>', self.Chon_chucvu)
        
        # Load dữ liệu
        self.load_chucvu_data()

    def tao_nhan_vien_tab(self):
        """Tab quản lý nhân viên"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Nhân Viên")
        
        # Frame input
        input_frame = ttk.LabelFrame(frame, text="Thông Tin Nhân Viên", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(input_frame, text="Mã NV:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.nv_manv = ttk.Entry(input_frame, width=20)
        self.nv_manv.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Tên NV:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.nv_tennv = ttk.Entry(input_frame, width=20)
        self.nv_tennv.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Năm Sinh:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.nv_namsinh = ttk.Entry(input_frame, width=20)
        self.nv_namsinh.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Giới Tính:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        self.nv_gioitinh = ttk.Combobox(input_frame, values=['Nam', 'Nữ'], width=18)
        self.nv_gioitinh.grid(row=1, column=3, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Địa Chỉ:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.nv_diachi = ttk.Entry(input_frame, width=20)
        self.nv_diachi.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky=tk.W+tk.E)
        
        ttk.Label(input_frame, text="Chức Vụ:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.nv_chucvu = ttk.Combobox(input_frame, width=18)
        self.nv_chucvu.grid(row=3, column=1, padx=5, pady=5)
        self.load_chucvu_combo()
        
        # Frame nút bấm
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=4, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame, text="Thêm", command=self.Them_nhanvien).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cập Nhật", command=self.CapNhat_nhanvien).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Xóa", command=self.Xoa_nhanvien).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Tìm Kiếm", command=self.Tim_nhanvien).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Làm Mới", command=self.LamMoi_nhanvien).pack(side=tk.LEFT, padx=5)
        
        # Frame tìm kiếm
        search_frame = ttk.Frame(input_frame)
        search_frame.grid(row=5, column=0, columnspan=4, pady=5, sticky=tk.W+tk.E)
        ttk.Label(search_frame, text="Tìm kiếm:").pack(side=tk.LEFT, padx=5)
        self.nv_search = ttk.Entry(search_frame, width=30)
        self.nv_search.pack(side=tk.LEFT, padx=5)
        
        # Frame bảng dữ liệu
        table_frame = ttk.LabelFrame(frame, text="Danh Sách Nhân Viên", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.nv_tree = ttk.Treeview(table_frame, columns=('MaNV', 'TenNV', 'Namsinh', 'gioitinh', 'diachi', 'chucvu'), 
                                     height=15, show='headings')
        self.nv_tree.column('MaNV', width=80, anchor=tk.CENTER)
        self.nv_tree.column('TenNV', width=120, anchor=tk.W)
        self.nv_tree.column('Namsinh', width=80, anchor=tk.CENTER)
        self.nv_tree.column('gioitinh', width=80, anchor=tk.CENTER)
        self.nv_tree.column('diachi', width=200, anchor=tk.W)
        self.nv_tree.column('chucvu', width=100, anchor=tk.CENTER)
        
        self.nv_tree.heading('MaNV', text='Mã NV')
        self.nv_tree.heading('TenNV', text='Tên NV')
        self.nv_tree.heading('Namsinh', text='Năm Sinh')
        self.nv_tree.heading('gioitinh', text='Giới Tính')
        self.nv_tree.heading('diachi', text='Địa Chỉ')
        self.nv_tree.heading('chucvu', text='Chức Vụ')
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.nv_tree.yview)
        self.nv_tree.configure(yscroll=scrollbar.set)
        
        self.nv_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.nv_tree.bind('<Double-1>', self.Chon_nhanvien)
        
        self.load_nhanvien_data()
        
    def tao_cham_cong_tab(self):
        """Tab quản lý chấm công"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Chấm Công")
        
        # Frame input
        input_frame = ttk.LabelFrame(frame, text="Thông Tin Chấm Công", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(input_frame, text="Mã CC:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.cc_macc = ttk.Entry(input_frame, width=20)
        self.cc_macc.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Mã NV:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.cc_manv = ttk.Combobox(input_frame, width=18)
        self.cc_manv.grid(row=0, column=3, padx=5, pady=5)
        self.load_nhanvien_combo()
        
        ttk.Label(input_frame, text="Ngày Chấm Công:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.cc_ngay = ttk.Entry(input_frame, width=20)
        self.cc_ngay.grid(row=2, column=1, padx=5, pady=5)
        self.cc_ngay.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        ttk.Label(input_frame, text="Giờ Vào:").grid(row=2, column=2, sticky=tk.W, padx=5, pady=5)
        self.cc_giovao = ttk.Entry(input_frame, width=20)
        self.cc_giovao.grid(row=2, column=3, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Giờ Ra:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.cc_giora = ttk.Entry(input_frame, width=20)
        self.cc_giora.grid(row=3, column=1, padx=5, pady=5)
        
        # Frame nút bấm
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=4, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame, text="Thêm", command=self.Them_chamcong).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cập Nhật", command=self.CapNhat_chamcong).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Xóa", command=self.Xoa_chamcong).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Tìm Kiếm", command=self.Tim_chamcong).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Làm Mới", command=self.LamMoi_chamcong).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Xuất Excel", command=self.Xuatexcel_chamcong).pack(side=tk.LEFT, padx=5)
        
        # Frame tìm kiếm
        search_frame = ttk.Frame(input_frame)
        search_frame.grid(row=5, column=0, columnspan=4, pady=5, sticky=tk.W+tk.E)
        ttk.Label(search_frame, text="Tìm kiếm:").pack(side=tk.LEFT, padx=5)
        self.cc_search = ttk.Entry(search_frame, width=30)
        self.cc_search.pack(side=tk.LEFT, padx=5)
        
        # Frame bảng dữ liệu
        table_frame = ttk.LabelFrame(frame, text="Danh Sách Chấm Công", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.cc_tree = ttk.Treeview(table_frame, columns=('MaCC', 'MaNV', 'NgayChamCong', 'GioVao', 'GioRa'), 
                                     height=15, show='headings')
        self.cc_tree.column('MaCC', width=80, anchor=tk.CENTER)
        self.cc_tree.column('MaNV', width=80, anchor=tk.CENTER)
        self.cc_tree.column('NgayChamCong', width=120, anchor=tk.CENTER)
        self.cc_tree.column('GioVao', width=120, anchor=tk.CENTER)
        self.cc_tree.column('GioRa', width=120, anchor=tk.CENTER)
        
        self.cc_tree.heading('MaCC', text='Mã CC')
        self.cc_tree.heading('MaNV', text='Mã NV')
        self.cc_tree.heading('NgayChamCong', text='Ngày Chấm Công')
        self.cc_tree.heading('GioVao', text='Giờ Vào')
        self.cc_tree.heading('GioRa', text='Giờ Ra')
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.cc_tree.yview)
        self.cc_tree.configure(yscroll=scrollbar.set)
        
        self.cc_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.cc_tree.bind('<Double-1>', self.Chon_chamcong)
        
        self.load_chamcong_data()
        
    def tao_tong_ket_tab(self):
        """Tab tổng kết chấm công"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Tổng Kết CC")
        
        # Frame tính toán
        input_frame = ttk.LabelFrame(frame, text="Tính Tổng Kết Chấm Công Theo Tháng", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(input_frame, text="Tháng:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.tk_thang = ttk.Spinbox(input_frame, from_=1, to=12, width=10)
        self.tk_thang.set(datetime.now().month)
        self.tk_thang.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Năm:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.tk_nam = ttk.Spinbox(input_frame, from_=2020, to=2050, width=10)
        self.tk_nam.set(datetime.now().year)
        self.tk_nam.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Mã NV:").grid(row=0, column=4, sticky=tk.W, padx=5, pady=5)
        self.tk_manv = ttk.Combobox(input_frame, width=18)
        self.tk_manv.grid(row=0, column=5, padx=5, pady=5)
        
        # Populate combobox
        try:
            data_nv = db_load_NhanVien()
            nv_values = ['Tất cả'] + [item['MaNV'] for item in data_nv]
            self.tk_manv['values'] = nv_values
            self.tk_manv.set('Tất cả')
        except Exception:
            pass
        
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=1, column=0, columnspan=8, pady=10)
        
        ttk.Button(button_frame, text="Tính Tổng Kết", command=self.tinh_tongket).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Tìm Kiếm", command=self.Tim_tongket).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Làm Mới", command=self.LamMoi_tongket).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Xuất Excel", command=self.Xuatexcel_tongket).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Xóa Tổng Kết", command=self.Xoa_tongket).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Xóa Tất Cả Tổng Kết", command=self.Xoa_all_tongket).pack(side=tk.LEFT, padx=5)
        
        search_frame = ttk.Frame(input_frame)
        search_frame.grid(row=2, column=0, columnspan=4, pady=5, sticky=tk.W+tk.E)
        ttk.Label(search_frame, text="Tìm kiếm:").pack(side=tk.LEFT, padx=5)
        self.tk_search = ttk.Entry(search_frame, width=30)
        self.tk_search.pack(side=tk.LEFT, padx=5)
        
        # Frame bảng dữ liệu
        table_frame = ttk.LabelFrame(frame, text="Danh Sách Tổng Kết Chấm Công", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.tk_tree = ttk.Treeview(table_frame, columns=('MaTKCC', 'MaNV', 'KyLuong', 'TongNgayLam', 'TongGioLam', 'NgayTongKet'), 
                                     height=15, show='headings')
        self.tk_tree.column('MaTKCC', width=80, anchor=tk.CENTER)
        self.tk_tree.column('MaNV', width=80, anchor=tk.CENTER)
        self.tk_tree.column('KyLuong', width=80, anchor=tk.CENTER)
        self.tk_tree.column('TongNgayLam', width=100, anchor=tk.CENTER)
        self.tk_tree.column('TongGioLam', width=100, anchor=tk.CENTER)
        self.tk_tree.column('NgayTongKet', width=120, anchor=tk.CENTER)
        
        self.tk_tree.heading('MaTKCC', text='Mã TK')
        self.tk_tree.heading('MaNV', text='Mã NV')
        self.tk_tree.heading('KyLuong', text='Kỳ Lương')
        self.tk_tree.heading('TongNgayLam', text='Tổng Ngày Làm')
        self.tk_tree.heading('TongGioLam', text='Tổng Giờ Làm')
        self.tk_tree.heading('NgayTongKet', text='Ngày Tổng Kết')
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tk_tree.yview)
        self.tk_tree.configure(yscroll=scrollbar.set)
        
        self.tk_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.load_tongket_data()
        
    def tao_tinh_luong_tab(self):
        """Tab tính lương"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Tính Lương")
        
        # Frame tính toán
        input_frame = ttk.LabelFrame(frame, text="Tính Lương Theo Tháng", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(input_frame, text="Tháng:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.tl_thang = ttk.Spinbox(input_frame, from_=1, to=12, width=10)
        self.tl_thang.set(datetime.now().month)
        self.tl_thang.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Năm:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.tl_nam = ttk.Spinbox(input_frame, from_=2020, to=2050, width=10)
        self.tl_nam.set(datetime.now().year)
        self.tl_nam.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Mã NV:").grid(row=0, column=4, sticky=tk.W, padx=5, pady=5)
        self.tl_manv = ttk.Entry(input_frame, width=15)
        self.tl_manv.grid(row=0, column=5, padx=5, pady=5)

        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=1, column=0, columnspan=6, pady=10)
        
        ttk.Button(button_frame, text="Tính Lương", command=self.tinhluong).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Tìm Kiếm", command=self.Tim_tinhluong).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Làm Mới", command=self.LamMoi_tinhluong).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Xuất Excel", command=self.Xuatexcel_tinhluong).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Xóa Tính Lương", command=self.Xoa_tinhluong).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Xóa Tất Cả Tính Lương", command=self.Xoa_all_tinhluong ).pack(side=tk.LEFT, padx=5)
        
        search_frame = ttk.Frame(input_frame)
        search_frame.grid(row=2, column=0, columnspan=6, pady=5, sticky=tk.W+tk.E)
        ttk.Label(search_frame, text="Tìm kiếm:").pack(side=tk.LEFT, padx=5)
        self.tl_search = ttk.Entry(search_frame, width=30)
        self.tl_search.pack(side=tk.LEFT, padx=5)
        
        # Frame bảng dữ liệu
        table_frame = ttk.LabelFrame(frame, text="Danh Sách Tính Lương", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.tl_tree = ttk.Treeview(table_frame, columns=('MaNV', 'KyLuong', 'LuongCoBan', 'HeSoLuong', 'PhuCap', 'TongLuong'), 
                                     height=15, show='headings')
        self.tl_tree.column('MaNV', width=80, anchor=tk.CENTER)
        self.tl_tree.column('KyLuong', width=80, anchor=tk.CENTER)
        self.tl_tree.column('LuongCoBan', width=100, anchor=tk.E)
        self.tl_tree.column('HeSoLuong', width=80, anchor=tk.E)
        self.tl_tree.column('PhuCap', width=80, anchor=tk.E)
        self.tl_tree.column('TongLuong', width=100, anchor=tk.E)
        
        self.tl_tree.heading('MaNV', text='Mã NV')
        self.tl_tree.heading('KyLuong', text='Kỳ Lương')
        self.tl_tree.heading('LuongCoBan', text='Lương Cơ Bản')
        self.tl_tree.heading('HeSoLuong', text='Hệ Số Lương')
        self.tl_tree.heading('PhuCap', text='Phụ Cấp')
        self.tl_tree.heading('TongLuong', text='Tổng Lương')
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tl_tree.yview)
        self.tl_tree.configure(yscroll=scrollbar.set)
        
        self.tl_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.load_tinhluong_data()

    def load_chucvu_data(self):
        """Load dữ liệu chức vụ"""
        try:
            for item in self.cv_tree.get_children():
                self.cv_tree.delete(item)
            
            data = db_load_ChucVu()
            for item in data:
                values = (item['MaCV'], item['TenCV'], DinhDang_Tien(item['LuongCoBan']), item['HeSoLuong'], DinhDang_Tien(item['PhuCap']))
                self.cv_tree.insert('', tk.END, values=values)
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def load_chucvu_combo(self):
        """Load chức vụ vào combobox"""
        try:
            data = db_load_ChucVu()
            cv_values = [f"{item['MaCV']}" for item in data]
            self.nv_chucvu['values'] = cv_values
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def Them_chucvu(self):
        """Thêm chức vụ mới"""
        try:
            if not (self.cv_macv.get() and self.cv_tencv.get() and self.cv_luongcb.get() and self.cv_hesolg.get()):
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
                return
            
            cv_list = [self.cv_macv.get(), self.cv_tencv.get(), float(self.cv_luongcb.get()), 
                      float(self.cv_hesolg.get()), float(self.cv_phucap.get() or 0)]
            db_Them_ChucVu(cv_list)
            messagebox.showinfo("Thành công", "Thêm chức vụ thành công!")
            self.LamMoi_chucvu()
            self.load_chucvu_data()
            self.load_chucvu_combo()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def CapNhat_chucvu(self):
        """Cập nhật chức vụ"""
        try:
            if not (self.cv_macv.get() and self.cv_tencv.get()):
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
                return
            
            cv_list = [self.cv_macv.get(), self.cv_tencv.get(), float(self.cv_luongcb.get()), 
                      float(self.cv_hesolg.get()), float(self.cv_phucap.get() or 0)]
            db_CapNhat_ChucVu(cv_list)
            messagebox.showinfo("Thành công", "Cập nhật chức vụ thành công!")
            self.LamMoi_chucvu()
            self.load_chucvu_data()
            self.load_chucvu_combo()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def Xoa_chucvu(self):
        """Xóa chức vụ"""
        try:
            if not self.cv_macv.get():
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn chức vụ cần xóa!")
                return
            
            if messagebox.askyesno("Xác nhận", "Bạn chắc chắn muốn xóa chức vụ này?"):
                db_Xoa_ChucVu(self.cv_macv.get())
                messagebox.showinfo("Thành công", "Xóa chức vụ thành công!")
                self.LamMoi_chucvu()
                self.load_chucvu_data()
                self.load_chucvu_combo()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def LamMoi_chucvu(self):
        """Xóa dữ liệu input chức vụ"""
        self.cv_macv.delete(0, tk.END)
        self.cv_tencv.delete(0, tk.END)
        self.cv_luongcb.delete(0, tk.END)
        self.cv_hesolg.delete(0, tk.END)
        self.cv_phucap.delete(0, tk.END)
    
    def Chon_chucvu(self, event):
        """Chọn chức vụ từ bảng"""
        selection = self.cv_tree.selection()
        if selection:
            item = self.cv_tree.item(selection[0])
            values = item['values']
            self.cv_macv.delete(0, tk.END)
            self.cv_macv.insert(0, values[0])
            self.cv_tencv.delete(0, tk.END)
            self.cv_tencv.insert(0, values[1])
            self.cv_luongcb.delete(0, tk.END)
            self.cv_luongcb.insert(0, values[2])
            self.cv_hesolg.delete(0, tk.END)
            self.cv_hesolg.insert(0, values[3])
            self.cv_phucap.delete(0, tk.END)
            self.cv_phucap.insert(0, values[4])

    def load_nhanvien_data(self):
        """Load dữ liệu nhân viên"""
        try:
            for item in self.nv_tree.get_children():
                self.nv_tree.delete(item)
            
            data = db_load_NhanVien()
            for item in data:
                values = (item['MaNV'], item['TenNV'], item['Namsinh'], item['gioitinh'], item['diachi'], item['chucvu'])
                self.nv_tree.insert('', tk.END, values=values)
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def load_nhanvien_combo(self):
        """Load nhân viên vào combobox"""
        try:
            data = db_load_NhanVien()
            nv_values = [f"{item['MaNV']}" for item in data]
            self.cc_manv['values'] = nv_values
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def Them_nhanvien(self):
        """Thêm nhân viên mới"""
        try:
            if not (self.nv_manv.get() and self.nv_tennv.get() and self.nv_namsinh.get() and self.nv_chucvu.get()):
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
                return
            
            chucvu = self.nv_chucvu.get().split(' - ')[0]
            nv_list = [self.nv_manv.get(), self.nv_tennv.get(), int(self.nv_namsinh.get()), 
                      self.nv_gioitinh.get(), self.nv_diachi.get(), chucvu]
            db_Them_NhanVien(nv_list)
            messagebox.showinfo("Thành công", "Thêm nhân viên thành công!")
            self.LamMoi_nhanvien()
            self.load_nhanvien_data()
            self.load_nhanvien_combo()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def CapNhat_nhanvien(self):
        """Cập nhật nhân viên"""
        try:
            if not (self.nv_manv.get() and self.nv_tennv.get()):
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
                return
            
            chucvu = self.nv_chucvu.get().split(' - ')[0]
            nv_list = [self.nv_manv.get(), self.nv_tennv.get(), int(self.nv_namsinh.get()), 
                      self.nv_gioitinh.get(), self.nv_diachi.get(), chucvu]
            db_CapNhat_NhanVien(nv_list)
            messagebox.showinfo("Thành công", "Cập nhật nhân viên thành công!")
            self.LamMoi_nhanvien()
            self.load_nhanvien_data()
            self.load_nhanvien_combo()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def Xoa_nhanvien(self):
        """Xóa nhân viên"""
        try:
            if not self.nv_manv.get():
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn nhân viên cần xóa!")
                return
            
            if messagebox.askyesno("Xác nhận", "Bạn chắc chắn muốn xóa nhân viên này?"):
                db_Xoa_NhanVien(self.nv_manv.get())
                messagebox.showinfo("Thành công", "Xóa nhân viên thành công!")
                self.LamMoi_nhanvien()
                self.load_nhanvien_data()
                self.load_nhanvien_combo()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def Tim_nhanvien(self):
        """Tìm kiếm nhân viên"""
        try:
            keyword = self.nv_search.get()
            if not keyword:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập từ khóa tìm kiếm!")
                return
            
            for item in self.nv_tree.get_children():
                self.nv_tree.delete(item)
            
            data = db_TimKiem_NhanVien(keyword)
            for item in data:
                values = (item['MaNV'], item['TenNV'], item['Namsinh'], item['gioitinh'], item['diachi'], item['chucvu'])
                self.nv_tree.insert('', tk.END, values=values)
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def LamMoi_nhanvien(self):
        """Xóa dữ liệu input nhân viên"""
        self.nv_manv.delete(0, tk.END)
        self.nv_tennv.delete(0, tk.END)
        self.nv_namsinh.delete(0, tk.END)
        self.nv_gioitinh.set('')
        self.nv_diachi.delete(0, tk.END)
        self.nv_chucvu.set('')
        self.nv_search.delete(0, tk.END)
        self.load_nhanvien_data()
    
    def Chon_nhanvien(self, event):
        """Chọn nhân viên từ bảng"""
        selection = self.nv_tree.selection()
        if selection:
            item = self.nv_tree.item(selection[0])
            values = item['values']
            self.nv_manv.delete(0, tk.END)
            self.nv_manv.insert(0, values[0])
            self.nv_tennv.delete(0, tk.END)
            self.nv_tennv.insert(0, values[1])
            self.nv_namsinh.delete(0, tk.END)
            self.nv_namsinh.insert(0, values[2])
            self.nv_gioitinh.set(values[3])
            self.nv_diachi.delete(0, tk.END)
            self.nv_diachi.insert(0, values[4])
            data = db_load_ChucVu()
            for item in data:
                if item['MaCV'] == values[5]:
                    self.nv_chucvu.set(f"{item['MaCV']} - {item['TenCV']}")
                    break

    def load_chamcong_data(self):
        """Load dữ liệu chấm công"""
        try:
            for item in self.cc_tree.get_children():
                self.cc_tree.delete(item)
            
            data = db_load_ChamCong()
            for item in data:
                values = (item['MaCC'], item['MaNV'], item['NgayChamCong'], item['GioVao'], item['GioRa'])
                self.cc_tree.insert('', tk.END, values=values)
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def Them_chamcong(self):
        """Thêm bản ghi chấm công"""
        try:
            if not (self.cc_macc.get() and self.cc_manv.get() and self.cc_ngay.get() and self.cc_giovao.get() and self.cc_giora.get()):
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
                return
            
            manv = self.cc_manv.get().split(' - ')[0]
            cc_list = [self.cc_macc.get(), manv, self.cc_ngay.get(), self.cc_giovao.get(), self.cc_giora.get()]
            db_Them_ChamCong(cc_list)
            messagebox.showinfo("Thành công", "Thêm bản ghi chấm công thành công!")
            self.LamMoi_chamcong()
            self.load_chamcong_data()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def CapNhat_chamcong(self):
        """Cập nhật bản ghi chấm công"""
        try:
            if not self.cc_macc.get():
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn bản ghi cần cập nhật!")
                return
            
            manv = self.cc_manv.get().split(' - ')[0]
            cc_list = [self.cc_macc.get(), manv, self.cc_ngay.get(), self.cc_giovao.get(), self.cc_giora.get()]
            db_CapNhat_ChamCong(cc_list)
            messagebox.showinfo("Thành công", "Cập nhật bản ghi chấm công thành công!")
            self.LamMoi_chamcong()
            self.load_chamcong_data()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def Xoa_chamcong(self):
        """Xóa bản ghi chấm công"""
        try:
            if not self.cc_macc.get():
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn bản ghi cần xóa!")
                return
            
            if messagebox.askyesno("Xác nhận", "Bạn chắc chắn muốn xóa bản ghi này?"):
                db_Xoa_ChamCong(self.cc_macc.get())
                messagebox.showinfo("Thành công", "Xóa bản ghi chấm công thành công!")
                self.LamMoi_chamcong()
                self.load_chamcong_data()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def Tim_chamcong(self):
        """Tìm kiếm chấm công"""
        try:
            keyword = self.cc_search.get()
            if not keyword:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập từ khóa tìm kiếm!")
                return
            
            for item in self.cc_tree.get_children():
                self.cc_tree.delete(item)
            
            data = db_TimKiem_ChamCong(keyword)
            for item in data:
                values = (item['MaCC'], item['MaNV'], item['NgayChamCong'], item['GioVao'], item['GioRa'])
                self.cc_tree.insert('', tk.END, values=values)
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def LamMoi_chamcong(self):
        """Xóa dữ liệu input chấm công"""
        self.cc_macc.delete(0, tk.END)
        self.cc_manv.set('')
        self.cc_ngay.delete(0, tk.END)
        self.cc_ngay.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.cc_giovao.delete(0, tk.END)
        self.cc_giora.delete(0, tk.END)
        self.cc_search.delete(0, tk.END)
        self.load_chamcong_data()
    
    def Chon_chamcong(self, event):
        """Chọn bản ghi chấm công từ bảng"""
        selection = self.cc_tree.selection()
        if selection:
            item = self.cc_tree.item(selection[0])
            values = item['values']
            self.cc_macc.delete(0, tk.END)
            self.cc_macc.insert(0, values[0])
            self.cc_manv.set(f"{values[1]} - ")
            self.cc_ngay.delete(0, tk.END)
            self.cc_ngay.insert(0, values[2])
            self.cc_giovao.delete(0, tk.END)
            self.cc_giovao.insert(0, values[3])
            self.cc_giora.delete(0, tk.END)
            self.cc_giora.insert(0, values[4])
    
    def XuatCSV_chamcong(self):
        """Xuất dữ liệu chấm công ra CSV"""
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", 
                                                     filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
            if file_path:
                db_Xuat_CSV_ChamCong(file_path)
                messagebox.showinfo("Thành công", f"Xuất dữ liệu thành công!\nĐường dẫn: {file_path}")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def Xuatexcel_chamcong(self):
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", 
                                                     filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
            if file_path:
                db_Xuat_Excel_ChamCong(file_path)
                messagebox.showinfo("Thành công", f"Xuất dữ liệu thành công!\nĐường dẫn: {file_path}")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def load_tongket_data(self):
        """Load dữ liệu tổng kết chấm công"""
        try:
            for item in self.tk_tree.get_children():
                self.tk_tree.delete(item)
            
            data = db_load_TongKetCC()
            for item in data:
                values = (item['MaTKCC'], item['MaNV'], item['KyLuong'], item['TongNgayLam'], item['TongGioLam'], item['NgayTongKet'])
                self.tk_tree.insert('', tk.END, values=values)
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def tinh_tongket(self):
        """Tính tổng kết chấm công"""
        try:
            thang = int(self.tk_thang.get())
            nam = int(self.tk_nam.get())
            
            manv = None
            sel = self.tk_manv.get().strip()
            if sel and sel != 'Tất cả':
                manv = sel

            if manv:
                db_Tao_TongKetCC_ChoNV(thang, nam, manv)
            else:
                db_Tao_TongKetCC_Thang(thang, nam)

            messagebox.showinfo("Thành công", f"Tính tổng kết chấm công tháng {thang}/{nam} thành công!")
            self.load_tongket_data()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def Tim_tongket(self):
        """Tìm kiếm tổng kết"""
        try:
            keyword = self.tk_search.get().strip()
            if not keyword:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập từ khóa tìm kiếm!")
                return

            for item in self.tk_tree.get_children():
                self.tk_tree.delete(item)

            data = db_TimKiem_TongKetCC(keyword)
            for item in data:
                values = (item['MaTKCC'], item['MaNV'], item['KyLuong'], item['TongNgayLam'], item['TongGioLam'], item['NgayTongKet'])
                self.tk_tree.insert('', tk.END, values=values)
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def  Xoa_tongket(self):
        """Xóa bản ghi tổng kết chấm công được chọn"""
        try:
            sel = self.tk_tree.selection()
            if not sel:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn bản ghi tổng kết để xóa!")
                return
            item = self.tk_tree.item(sel[0])
            vals = item.get('values', [])
            if not vals:
                messagebox.showerror("Lỗi", "Dữ liệu bản ghi không hợp lệ")
                return
            matk = vals[0]
            if messagebox.askyesno("Xác nhận", f"Xóa tổng kết mã {matk}?"):
                db_Xoa_TongKetCC(matk)
                messagebox.showinfo("Thành công", "Đã xóa bản ghi tổng kết.")
                self.load_tongket_data()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def Xoa_all_tongket(self):
        """Xóa tất cả bản ghi tổng kết chấm công"""
        try:
            if not messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa tất cả bản ghi tổng kết chấm công không?"):
                return
            db_Xoa_TongKetCC_All()
            messagebox.showinfo("Thành công", "Đã xóa tất cả bản ghi tổng kết chấm công.")
            self.load_tongket_data()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def LamMoi_tongket(self):
        """Xóa dữ liệu tìm kiếm"""
        self.tk_search.delete(0, tk.END)
        self.load_tongket_data()

    def XuatCSV_tongket(self):
        '''Xuất dữ liệu tổng kết chấm công ra CSV'''
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", 
                                                     filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
            if file_path:
                db_Xuat_CSV_TongKetCC(file_path)
                messagebox.showinfo("Thành công", f"Xuất dữ liệu thành công!\nĐường dẫn: {file_path}")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def Xuatexcel_tongket(self):
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", 
                                                     filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
            if file_path:
                db_Xuat_Excel_TongKetCC(file_path)
                messagebox.showinfo("Thành công", f"Xuất dữ liệu thành công!\nĐường dẫn: {file_path}")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def load_tinhluong_data(self):
        """Load dữ liệu tính lương"""
        try:
            for item in self.tl_tree.get_children():
                self.tl_tree.delete(item)
            
            data = db_load_TinhLuong()
            for item in data:
                values = (item['MaNV'], item['KyLuong'], DinhDang_Tien(item['LuongCoBan']), 
                         item['HeSoLuong'], DinhDang_Tien(item['PhuCap']), DinhDang_Tien(item['TongLuong']))
                self.tl_tree.insert('', tk.END, values=values)
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def tinhluong(self):
        """Tính lương"""
        try:
            thang = int(self.tl_thang.get())
            nam = int(self.tl_nam.get())
            
            manv = None
            manu = self.tl_manv.get().strip()
            if manu:
                manv = manu

            db_Tinh_Luong_Thang(thang, nam, MaNV=manv)
            messagebox.showinfo("Thành công", f"Tính lương tháng {thang}/{nam} thành công!")
            self.load_tinhluong_data()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def Tim_tinhluong(self):
        """Tìm kiếm tính lương"""
        try:
            keyword = self.tl_search.get()
            if not keyword:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập từ khóa tìm kiếm!")
                return
            
            for item in self.tl_tree.get_children():
                self.tl_tree.delete(item)
            
            data = db_TimKiem_TinhLuong(keyword)
            for item in data:
                values = (item['MaNV'], item['KyLuong'], item['LuongCoBan'], 
                         item['HeSoLuong'], item['PhuCap'], f"{item['TongLuong']:,.0f}")
                self.tl_tree.insert('', tk.END, values=values)
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def LamMoi_tinhluong(self):
        """Xóa dữ liệu tìm kiếm"""
        self.tl_search.delete(0, tk.END)
        self.tl_manv.delete(0, tk.END)
        self.load_tinhluong_data()

    def Xoa_tinhluong(self):
        """Xóa bản ghi tính lương được chọn"""
        try:
            sel = self.tl_tree.selection()
            if not sel:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn bản ghi tính lương để xóa!")
                return
            item = self.tl_tree.item(sel[0])
            vals = item.get('values', [])
            if not vals or len(vals) < 2:
                messagebox.showerror("Lỗi", "Dữ liệu bản ghi không hợp lệ")
                return
            manv = vals[0]
            kyluong = vals[1]
            if messagebox.askyesno("Xác nhận", f"Xóa tính lương của {manv} kỳ {kyluong}?"):
                db_Xoa_TinhLuong_TheoKy(manv, kyluong)
                messagebox.showinfo("Thành công", "Đã xóa bản ghi tính lương.")
                self.load_tinhluong_data()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def Xoa_all_tinhluong(self):
        """Xóa tất cả bản ghi tính lương"""
        try:
            if not messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa tất cả bản ghi tính lương không?"):
                return
            db_Xoa_TinhLuong_All()
            messagebox.showinfo("Thành công", "Đã xóa tất cả bản ghi tính lương.")
            self.load_tinhluong_data()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def XuatCSV_tinhluong(self):
        '''Xuất dữ liệu tính lương ra CSV'''
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", 
                                                     filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
            if file_path:
                db_Xuat_CSV_TinhLuong(file_path)
                messagebox.showinfo("Thành công", f"Xuất dữ liệu thành công!\nĐường dẫn: {file_path}")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def Xuatexcel_tinhluong(self):
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", 
                                                     filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
            if file_path:
                db_Xuat_Excel_TinhLuong(file_path)
                messagebox.showinfo("Thành công", f"Xuất dữ liệu thành công!\nĐường dẫn: {file_path}")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = QLNSU_GUI(root)
    root.mainloop()   
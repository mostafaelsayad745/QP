#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database Manager for QB Academy Quality Management System
Handles all database operations and file management
"""

import sqlite3
import os
import shutil
import hashlib
from datetime import datetime
import json
from pathlib import Path

class DatabaseManager:
    def __init__(self, db_path="qb_academy.db"):
        self.db_path = db_path
        self.files_dir = "uploaded_files"
        self.ensure_files_directory()
        self.init_database()
    
    def ensure_files_directory(self):
        """إنشاء مجلد الملفات المرفوعة إذا لم يكن موجوداً"""
        if not os.path.exists(self.files_dir):
            os.makedirs(self.files_dir)
            # إنشاء مجلدات فرعية للتنظيم
            subdirs = ['documents', 'procedures', 'forms', 'certificates', 'reports']
            for subdir in subdirs:
                os.makedirs(os.path.join(self.files_dir, subdir), exist_ok=True)
    
    def init_database(self):
        """إنشاء قاعدة البيانات والجداول"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # جدول المستخدمين
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    email TEXT,
                    role TEXT NOT NULL DEFAULT 'user',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            ''')
            
            # جدول الإجراءات
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS procedures (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    purpose TEXT,
                    scope TEXT,
                    content TEXT,
                    version TEXT DEFAULT '1.0',
                    status TEXT DEFAULT 'draft',
                    created_by INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (created_by) REFERENCES users (id)
                )
            ''')
            
            # جدول النماذج
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS forms (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    fields_structure TEXT,
                    created_by INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (created_by) REFERENCES users (id)
                )
            ''')
            
            # جدول بيانات النماذج
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS form_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    form_name TEXT NOT NULL,
                    form_data TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    created_by INTEGER,
                    FOREIGN KEY (created_by) REFERENCES users (id)
                )
            ''')
            
            # Check if the form_name column exists before creating index
            try:
                cursor.execute("SELECT form_name FROM form_data LIMIT 1")
                # If no error, create index for faster searches
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_form_name ON form_data(form_name)
                ''')
            except sqlite3.OperationalError:
                # Column doesn't exist, might be old structure - recreate table
                cursor.execute('DROP TABLE IF EXISTS form_data')
                cursor.execute('''
                    CREATE TABLE form_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        form_name TEXT NOT NULL,
                        form_data TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        created_by INTEGER,
                        FOREIGN KEY (created_by) REFERENCES users (id)
                    )
                ''')
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_form_name ON form_data(form_name)
                ''')
            
            # جدول الملفات المرفوعة
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS uploaded_files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    original_name TEXT NOT NULL,
                    stored_name TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    file_type TEXT,
                    file_size INTEGER,
                    file_hash TEXT,
                    category TEXT DEFAULT 'general',
                    related_table TEXT,
                    related_id INTEGER,
                    uploaded_by INTEGER,
                    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    description TEXT,
                    FOREIGN KEY (uploaded_by) REFERENCES users (id)
                )
            ''')
            
            # جدول الشهادات
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS certificates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    certificate_number TEXT UNIQUE NOT NULL,
                    candidate_name TEXT NOT NULL,
                    certificate_type TEXT NOT NULL,
                    issue_date DATE NOT NULL,
                    expiry_date DATE,
                    status TEXT DEFAULT 'active',
                    issued_by INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (issued_by) REFERENCES users (id)
                )
            ''')
            
            # جدول التقييمات
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS assessments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    candidate_name TEXT NOT NULL,
                    assessment_type TEXT NOT NULL,
                    assessment_date DATE NOT NULL,
                    assessor_id INTEGER,
                    score REAL,
                    result TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (assessor_id) REFERENCES users (id)
                )
            ''')
            
            # جدول سجل النشاطات
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS activity_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    action TEXT NOT NULL,
                    table_name TEXT,
                    record_id INTEGER,
                    old_values TEXT,
                    new_values TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ip_address TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # إنشاء مستخدم افتراضي (admin)
            self.create_default_admin()
            
            conn.commit()
    
    def create_default_admin(self):
        """إنشاء مستخدم admin افتراضي"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # التحقق من وجود مستخدم admin
                cursor.execute("SELECT id FROM users WHERE username = 'admin'")
                if not cursor.fetchone():
                    # إنشاء كلمة مرور مشفرة
                    password_hash = hashlib.sha256("admin123".encode()).hexdigest()
                    
                    cursor.execute('''
                        INSERT INTO users (username, password_hash, full_name, email, role)
                        VALUES (?, ?, ?, ?, ?)
                    ''', ("admin", password_hash, "مدير النظام", "admin@qbacademy.com", "admin"))
                    
                    conn.commit()
                    print("تم إنشاء المستخدم الافتراضي: admin / admin123")
                else:
                    print("المستخدم الافتراضي موجود مسبقاً")
                    
        except Exception as e:
            print(f"خطأ في إنشاء المستخدم الافتراضي: {str(e)}")
            # محاولة إنشاؤه مرة أخرى بطريقة مختلفة
            try:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    password_hash = hashlib.sha256("admin123".encode()).hexdigest()
                    cursor.execute('''
                        INSERT OR IGNORE INTO users (username, password_hash, full_name, email, role)
                        VALUES (?, ?, ?, ?, ?)
                    ''', ("admin", password_hash, "مدير النظام", "admin@qbacademy.com", "admin"))
                    conn.commit()
                    print("تم إنشاء المستخدم الافتراضي بالطريقة البديلة")
            except Exception as e2:
                print(f"فشل في إنشاء المستخدم الافتراضي: {str(e2)}")
    
    def authenticate_user(self, username, password):
        """التحقق من صحة بيانات المستخدم"""
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        print(f"محاولة مصادقة المستخدم: '{username}'")
        print(f"Hash كلمة المرور: {password_hash[:10]}...")
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # التحقق من وجود المستخدم أولاً
            cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
            user_exists = cursor.fetchone()
            print(f"المستخدم موجود: {user_exists is not None}")
            
            cursor.execute('''
                SELECT id, username, full_name, role, is_active 
                FROM users 
                WHERE username = ? AND password_hash = ? AND is_active = 1
            ''', (username, password_hash))
            
            user = cursor.fetchone()
            print(f"نتيجة المصادقة: {user is not None}")
            
            if user:
                # تحديث آخر تسجيل دخول
                cursor.execute('''
                    UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?
                ''', (user[0],))
                conn.commit()
                
                return {
                    'id': user[0],
                    'username': user[1],
                    'full_name': user[2],
                    'role': user[3],
                    'is_active': user[4]
                }
            return None
    
    def save_file(self, file_path, category='general', related_table=None, related_id=None, user_id=None, description=None):
        """حفظ ملف وتسجيله في قاعدة البيانات"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"الملف غير موجود: {file_path}")
        
        # الحصول على معلومات الملف
        original_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        file_type = os.path.splitext(original_name)[1].lower()
        
        # إنشاء hash للملف
        file_hash = self.calculate_file_hash(file_path)
        
        # إنشاء اسم فريد للملف
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        stored_name = f"{timestamp}_{file_hash[:8]}_{original_name}"
        
        # تحديد المجلد الفرعي حسب الفئة
        category_dir = os.path.join(self.files_dir, category)
        if not os.path.exists(category_dir):
            os.makedirs(category_dir)
        
        # المسار النهائي للملف
        final_path = os.path.join(category_dir, stored_name)
        
        try:
            # نسخ الملف
            shutil.copy2(file_path, final_path)
            
            # تسجيل الملف في قاعدة البيانات
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO uploaded_files 
                    (original_name, stored_name, file_path, file_type, file_size, file_hash, 
                     category, related_table, related_id, uploaded_by, description)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (original_name, stored_name, final_path, file_type, file_size, file_hash,
                      category, related_table, related_id, user_id, description))
                
                file_id = cursor.lastrowid
                conn.commit()
                
                return {
                    'file_id': file_id,
                    'original_name': original_name,
                    'stored_name': stored_name,
                    'file_path': final_path,
                    'file_size': file_size,
                    'file_type': file_type
                }
                
        except Exception as e:
            # حذف الملف إذا فشل الحفظ في قاعدة البيانات
            if os.path.exists(final_path):
                os.remove(final_path)
            raise e
    
    def get_file_info(self, file_id):
        """الحصول على معلومات ملف من قاعدة البيانات"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, original_name, stored_name, file_path, file_type, file_size,
                       category, upload_date, description
                FROM uploaded_files 
                WHERE id = ?
            ''', (file_id,))
            
            result = cursor.fetchone()
            if result:
                return {
                    'id': result[0],
                    'original_name': result[1],
                    'stored_name': result[2],
                    'file_path': result[3],
                    'file_type': result[4],
                    'file_size': result[5],
                    'category': result[6],
                    'upload_date': result[7],
                    'description': result[8]
                }
            return None
    
    def get_files_by_category(self, category):
        """الحصول على جميع الملفات في فئة معينة"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, original_name, stored_name, file_path, file_size, upload_date, description
                FROM uploaded_files 
                WHERE category = ?
                ORDER BY upload_date DESC
            ''', (category,))
            
            files = []
            for row in cursor.fetchall():
                files.append({
                    'id': row[0],
                    'original_name': row[1],
                    'stored_name': row[2],
                    'file_path': row[3],
                    'file_size': row[4],
                    'upload_date': row[5],
                    'description': row[6]
                })
            return files
    
    def calculate_file_hash(self, file_path):
        """حساب hash للملف"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def log_activity(self, user_id, action, table_name=None, record_id=None, old_values=None, new_values=None, details=None, **kwargs):
        """تسجيل نشاط في سجل النشاطات"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO activity_log (user_id, action, table_name, record_id, old_values, new_values)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, action, table_name, record_id, 
                  json.dumps(old_values, ensure_ascii=False) if old_values else None,
                  json.dumps(new_values, ensure_ascii=False) if new_values else None))
            conn.commit()
    
    def backup_database(self, backup_path=None):
        """إنشاء نسخة احتياطية من قاعدة البيانات"""
        if not backup_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"backup_qb_academy_{timestamp}.db"
        
        try:
            shutil.copy2(self.db_path, backup_path)
            return backup_path
        except Exception as e:
            raise Exception(f"فشل في إنشاء النسخة الاحتياطية: {str(e)}")
    
    def delete_file(self, file_id):
        """حذف ملف من النظام وقاعدة البيانات"""
        file_info = self.get_file_info(file_id)
        if not file_info:
            return False
        
        try:
            # حذف الملف من النظام
            if os.path.exists(file_info['file_path']):
                os.remove(file_info['file_path'])
            
            # حذف السجل من قاعدة البيانات
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM uploaded_files WHERE id = ?", (file_id,))
                conn.commit()
            
            return True
        except Exception as e:
            print(f"خطأ في حذف الملف: {str(e)}")
            return False
    
    def get_database_stats(self):
        """إحصائيات قاعدة البيانات"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            stats = {}
            
            # عدد المستخدمين
            cursor.execute("SELECT COUNT(*) FROM users WHERE is_active = 1")
            stats['active_users'] = cursor.fetchone()[0]
            
            # عدد الإجراءات
            cursor.execute("SELECT COUNT(*) FROM procedures")
            stats['procedures'] = cursor.fetchone()[0]
            
            # عدد النماذج
            cursor.execute("SELECT COUNT(*) FROM forms")
            stats['forms'] = cursor.fetchone()[0]
            
            # عدد الملفات المرفوعة
            cursor.execute("SELECT COUNT(*) FROM uploaded_files")
            stats['uploaded_files'] = cursor.fetchone()[0]
            
            # حجم الملفات الإجمالي
            cursor.execute("SELECT SUM(file_size) FROM uploaded_files")
            total_size = cursor.fetchone()[0]
            stats['total_file_size'] = total_size if total_size else 0
            
            # عدد الشهادات
            cursor.execute("SELECT COUNT(*) FROM certificates")
            stats['certificates'] = cursor.fetchone()[0]
            
            return stats
    
    def create_forms_table(self):
        """Ensure forms table exists - this method ensures the table structure is correct"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if table exists with correct structure
                cursor.execute('''
                    SELECT sql FROM sqlite_master 
                    WHERE type='table' AND name='form_data'
                ''')
                result = cursor.fetchone()
                
                if result and 'form_name' not in result[0]:
                    # Drop old table with wrong structure and recreate
                    cursor.execute('DROP TABLE IF EXISTS form_data')
                    
                    cursor.execute('''
                        CREATE TABLE form_data (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            form_name TEXT NOT NULL,
                            form_data TEXT NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            created_by INTEGER,
                            FOREIGN KEY (created_by) REFERENCES users (id)
                        )
                    ''')
                    
                    # Create index for faster searches
                    cursor.execute('''
                        CREATE INDEX IF NOT EXISTS idx_form_name ON form_data(form_name)
                    ''')
                
                conn.commit()
                print("Forms table structure verified/updated successfully")
                
        except Exception as e:
            print(f"Error creating forms table: {e}")

    def save_form_data(self, form_name=None, data=None, user_id=None):
        """Save form data to database"""
        try:
            import json
            import time
            
            # Convert data to JSON string
            if isinstance(data, (list, dict)):
                data_json = json.dumps(data, ensure_ascii=False, indent=2)
            else:
                data_json = str(data)
            
            # Small delay to avoid database lock issues
            time.sleep(0.1)
            
            conn = None
            try:
                conn = sqlite3.connect(self.db_path, timeout=30.0)
                conn.execute('PRAGMA journal_mode=WAL')  # Use WAL mode for better concurrency
                cursor = conn.cursor()
                
                # Check if form already exists
                cursor.execute('SELECT id FROM form_data WHERE form_name = ?', (form_name,))
                existing = cursor.fetchone()
                
                if existing:
                    # Update existing form
                    cursor.execute('''
                        UPDATE form_data 
                        SET form_data = ?, updated_at = CURRENT_TIMESTAMP 
                        WHERE form_name = ?
                    ''', (data_json, form_name))
                    record_id = existing[0]
                    action = "تحديث بيانات النموذج"
                    
                else:
                    # Insert new form
                    cursor.execute('''
                        INSERT INTO form_data (form_name, form_data, created_by)
                        VALUES (?, ?, ?)
                    ''', (form_name, data_json, user_id))
                    record_id = cursor.lastrowid
                    action = "إضافة بيانات نموذج جديد"
                
                conn.commit()
                
                # Log activity in a separate connection to avoid locks
                self._log_activity_async(user_id, action, "form_data", record_id)
                
                return True
                
            finally:
                if conn:
                    conn.close()
                
        except Exception as e:
            print(f"Error saving form data: {e}")
            return False

    def _log_activity_async(self, user_id, action, table_name, record_id):
        """Log activity in a separate connection to avoid locks"""
        try:
            import time
            time.sleep(0.05)  # Small delay
            conn = sqlite3.connect(self.db_path, timeout=30.0)
            conn.execute('PRAGMA journal_mode=WAL')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO activity_log (user_id, action, table_name, record_id)
                VALUES (?, ?, ?, ?)
            ''', (user_id, action, table_name, record_id))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Warning: Could not log activity: {e}")
            # Don't fail the main operation if logging fails

    def load_form_data(self, form_name):
        """Load form data from database"""
        try:
            import json
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT form_data FROM form_data WHERE form_name = ?
                ''', (form_name,))
                
                result = cursor.fetchone()
                if result:
                    try:
                        return json.loads(result[0])
                    except json.JSONDecodeError:
                        return result[0]  # Return as string if not JSON
                return None
                
        except Exception as e:
            print(f"Error loading form data: {e}")
            return None

    def get_all_forms_data(self):
        """Get all forms data from database"""
        try:
            import json
            import time
            
            # Small delay to avoid database lock issues
            time.sleep(0.1)
            
            conn = None
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT form_name, form_data, created_at, updated_at 
                    FROM form_data 
                    ORDER BY form_name
                ''')
                
                results = cursor.fetchall()
                forms_data = {}
                
                for row in results:
                    form_name, data_str, created_at, updated_at = row
                    try:
                        data = json.loads(data_str)
                    except json.JSONDecodeError:
                        data = data_str
                        
                    forms_data[form_name] = {
                        'data': data,
                        'created_at': created_at,
                        'updated_at': updated_at
                    }
                
                return forms_data
                
            finally:
                if conn:
                    conn.close()
                
        except Exception as e:
            print(f"Error getting all forms data: {e}")
            return {}

    def delete_form_data(self, form_name=None, user_id=None):
        """Delete form data from database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get form ID for logging
                cursor.execute('SELECT id FROM form_data WHERE form_name = ?', (form_name,))
                result = cursor.fetchone()
                
                if result:
                    form_id = result[0]
                    
                    # Delete the form
                    cursor.execute('DELETE FROM form_data WHERE form_name = ?', (form_name,))
                    conn.commit()
                    
                    # Log the activity
                    self.log_activity(user_id, "حذف بيانات النموذج", "form_data", form_id)
                    
                    return True
                return False
                
        except Exception as e:
            print(f"Error deleting form data: {e}")
            return False

    def update_form_data(self, form_name=None, data=None, user_id=None):
        """Update existing form data in database"""
        try:
            import json
            import time
            
            # Convert data to JSON string
            if isinstance(data, (list, dict)):
                data_json = json.dumps(data, ensure_ascii=False, indent=2)
            else:
                data_json = str(data)
            
            # Small delay to avoid database lock issues
            time.sleep(0.1)
            
            conn = None
            try:
                conn = sqlite3.connect(self.db_path, timeout=30.0)
                conn.execute('PRAGMA journal_mode=WAL')
                cursor = conn.cursor()
                
                # Check if form exists
                cursor.execute('SELECT id FROM form_data WHERE form_name = ?', (form_name,))
                existing = cursor.fetchone()
                
                if existing:
                    # Update existing form
                    cursor.execute('''
                        UPDATE form_data 
                        SET form_data = ?, updated_at = CURRENT_TIMESTAMP 
                        WHERE form_name = ?
                    ''', (data_json, form_name))
                    record_id = existing[0]
                    action = "تحديث بيانات النموذج"
                    
                    conn.commit()
                    
                    # Log activity
                    self._log_activity_async(user_id, action, "form_data", record_id)
                    
                    return True
                else:
                    print(f"Form {form_name} not found for update")
                    return False
                
            finally:
                if conn:
                    conn.close()
                
        except Exception as e:
            print(f"Error updating form data: {e}")
            return False

    def backup_forms_data(self):
        """Create backup of all forms data"""
        try:
            import json
            from datetime import datetime
            
            backup_data = self.get_all_forms_data()
            
            # Create backup file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"forms_backup_{timestamp}.json"
            
            with open(backup_filename, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, ensure_ascii=False, indent=2)
            
            return backup_filename
            
        except Exception as e:
            print(f"Error creating forms backup: {e}")
            return None

import csv
import os
from Bill import IncomeBill, ExpenseBill, bill_hash
from User import User, VipUser

# 数据持久化类，实现csv读写
class DataPersistence:
    def __init__(self, user_file="users.csv", bill_file="bills.csv"):
        self.__user_file = user_file
        self.__bill_file = bill_file
        # 初始化文件（不存在则创建）
        self._init_file(user_file, ["user_id", "name", "balance", "type", "budget_limit", "points"])
        self._init_file(bill_file, ["bill_id", "type", "amount", "date", "category", "remark"])

    # 私有方法：初始化csv文件，添加表头
    def _init_file(self, file_path, header):
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(header)

    # 保存用户数据到csv
    def save_user(self, user):
        # 判断用户类型：普通/VIP
        user_type = "VIP" if isinstance(user, VipUser) else "NORMAL"
        budget_limit = user._VipUser__budget_limit if user_type == "VIP" else ""
        points = user.get_points() if user_type == "VIP" else ""
        # 写入数据
        with open(self.__user_file, "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                user.get_user_id(), user.get_name(), user.get_balance(),
                user_type, budget_limit, points
            ])
        return f"✅ 用户[{user.get_name()}]已保存到本地"

    # 保存账单数据到csv
    def save_bill(self, bill):
        with open(self.__bill_file, "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                bill.get_bill_id(), bill.get_type(), bill.get_amount(),
                bill.get_date(), bill.get_category(), bill.get_remark()
            ])
        # 同时添加到哈希表
        bill_hash.add_bill(bill.get_category(), bill)
        bill_hash.add_bill(bill.get_date()[:7], bill)  # 按年月建键（如2026-03）
        return f"✅ 账单[{bill.get_bill_id()}]已保存到本地并加入哈希表"

    # 读取本地账单数据（拓展用，可加载到哈希表）
    def load_bills(self):
        if not os.path.exists(self.__bill_file):
            return []
        bills = []
        with open(self.__bill_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                amount = float(row["amount"])
                date = row["date"]
                cate = row["category"]
                remark = row["remark"]
                # 重建账单对象
                if row["type"] == "收入":
                    bill = IncomeBill(amount, date, cate, remark)
                else:
                    bill = ExpenseBill(amount, date, cate, remark)
                bills.append(bill)
        return bills

    # 导出统计结果为csv（拓展用）
    def export_stat(self, stat_data, file_name="stat_result.csv"):
        with open(file_name, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            for k, v in stat_data.items():
                if isinstance(v, dict):
                    for sk, sv in v.items():
                        writer.writerow([k, sk, sv])
                else:
                    writer.writerow([k, v])
        return f"✅ 统计结果已导出为：{file_name}"

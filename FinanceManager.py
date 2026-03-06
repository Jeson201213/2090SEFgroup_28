from Bill import bill_hash, IncomeBill, ExpenseBill
from datetime import datetime

# 希尔排序实现，Task2自学的新算法
def shell_sort(bills, key="amount"):
    """
    希尔排序：按金额/日期排序
    :param bills: 账单列表
    :param key: 排序键，amount=金额，date=日期
    :return: 排序后的账单列表
    """
    n = len(bills)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = bills[i]
            j = i
            # 按金额排序（从大到小）
            if key == "amount":
                while j >= gap and bills[j - gap].get_amount() < temp.get_amount():
                    bills[j] = bills[j - gap]
                    j -= gap
            # 按日期排序（从新到旧）
            elif key == "date":
                while j >= gap and bills[j - gap].get_date() < temp.get_date():
                    bills[j] = bills[j - gap]
                    j -= gap
            bills[j] = temp
        gap = gap // 2
    return bills

# 财务统计核心类，封装所有统计逻辑
class FinanceManager:
    def __init__(self, user):
        self.__user = user  # 关联用户对象
        self.__all_bills = self._get_all_bills()  # 加载所有账单

    # 私有方法：从哈希表获取所有账单
    def _get_all_bills(self):
        all_bills = []
        for bucket in bill_hash.table:
            all_bills.extend([bill for _, bill in bucket])
        return all_bills

    # 刷新账单数据
    def refresh_bills(self):
        self.__all_bills = self._get_all_bills()

    # 按时间筛选账单（月度/年度）
    def filter_bills_by_time(self, year=None, month=None):
        self.refresh_bills()
        filtered = []
        for bill in self.__all_bills:
            bill_date = datetime.strptime(bill.get_date(), "%Y-%m-%d")
            if year and bill_date.year != int(year):
                continue
            if month and bill_date.month != int(month):
                continue
            filtered.append(bill)
        return filtered

    # 收支总额统计
    def total_income_expense(self, year=None, month=None):
        bills = self.filter_bills_by_time(year, month)
        total_income = sum(b.get_amount() for b in bills if isinstance(b, IncomeBill))
        total_expense = sum(b.get_amount() for b in bills if isinstance(b, ExpenseBill))
        return round(total_income, 2), round(total_expense, 2), round(total_income + total_expense, 2)

    # 分类统计收支
    def category_stat(self, year=None, month=None):
        bills = self.filter_bills_by_time(year, month)
        stat = {"收入": {}, "支出": {}}
        for bill in bills:
            bill_type = bill.get_type()
            cate = bill.get_category()
            amount = bill.get_amount()
            if cate not in stat[bill_type]:
                stat[bill_type][cate] = 0
            stat[bill_type][cate] += amount
        # 保留两位小数
        for t in stat:
            for c in stat[t]:
                stat[t][c] = round(stat[t][c], 2)
        return stat

    # 消费TOP N排序（调用希尔排序）
    def top_n_expense(self, n=5, year=None, month=None):
        expense_bills = [b for b in self.filter_bills_by_time(year, month) if isinstance(b, ExpenseBill)]
        sorted_bills = shell_sort(expense_bills, key="amount")  # 按金额从大到小排序
        return sorted_bills[:n]

    def __str__(self):
        total_i, total_e, total = self.total_income_expense()
        return f"[{self.__user.get_name()}] 总收支统计：收入{total_i}元，支出{total_e}元，结余{total}元"

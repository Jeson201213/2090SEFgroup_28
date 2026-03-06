from abc import ABC, abstractmethod
from datetime import datetime
# 自定义哈希表类，实现Task2自学的新数据结构
class BillHashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]  # 链地址法解决哈希冲突

    # 哈希函数：以分类/年月为键，计算哈希值
    def _hash(self, key):
        return hash(key) % self.size

    # 新增账单：键=分类/年月，值=账单对象
    def add_bill(self, key, bill):
        index = self._hash(key)
        self.table[index].append((key, bill))

    # 查询账单：根据键获取所有对应账单
    def get_bills(self, key):
        index = self._hash(key)
        return [bill for k, bill in self.table[index] if k == key]

    # 删除账单：根据账单ID删除
    def delete_bill(self, bill_id):
        for bucket in self.table:
            for i, (k, bill) in enumerate(bucket):
                if bill.get_bill_id() == bill_id:
                    del bucket[i]
                    return True
        return False

# 抽象账单基类，定义抽象方法体现OOP抽象性
class Bill(ABC):
    _bill_count = 0  # 类属性，生成唯一账单ID

    def __init__(self, amount, date, category, remark=""):
        Bill._bill_count += 1
        self.__bill_id = f"BILL{Bill._bill_count:04d}"
        self.__amount = self._validate_amount(amount)  # 金额校验
        # 日期格式化，默认当前时间
        self.__date = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
        self.__category = category.strip()
        self.__remark = remark.strip()

    # 抽象方法：获取收支类型，子类必须实现（多态核心）
    @abstractmethod
    def get_type(self):
        pass

    # 私有方法：金额基础校验
    def _validate_amount(self, amount):
        if not isinstance(amount, (int, float)):
            raise ValueError("金额必须为数字！")
        return round(amount, 2)

    # 公共getter方法
    def get_bill_id(self):
        return self.__bill_id

    def get_amount(self):
        return self.__amount

    def get_date(self):
        return self.__date.strftime("%Y-%m-%d")

    def get_category(self):
        return self.__category

    def get_remark(self):
        return self.__remark

    def __str__(self):
        return f"[{self.__bill_id}] {self.get_type()} | {self.get_date()} | {self.__category} | {self.__amount}元 | {self.__remark}"

# 收入账单子类，实现抽象方法
class IncomeBill(Bill):
    def __init__(self, amount, date, category, remark=""):
        super().__init__(amount, date, category, remark)

    def get_type(self):
        return "收入"

    # 重写金额校验：收入必须为正数
    def _validate_amount(self, amount):
        amount = super()._validate_amount(amount)
        if amount <= 0:
            raise ValueError("收入金额必须大于0！")
        return amount

# 支出账单子类，实现抽象方法
class ExpenseBill(Bill):
    def __init__(self, amount, date, category, remark=""):
        super().__init__(amount, date, category, remark)

    def get_type(self):
        return "支出"

    # 重写金额校验：支出必须为负数
    def _validate_amount(self, amount):
        amount = super()._validate_amount(amount)
        if amount >= 0:
            raise ValueError("支出金额必须小于0！")
        return amount

# 哈希表实例化，全局账单存储
bill_hash = BillHashTable()

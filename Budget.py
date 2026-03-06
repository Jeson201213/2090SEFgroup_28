from FinanceManager import FinanceManager

# 预算管理类，与财务统计强关联
class Budget:
    def __init__(self, user, month_budget=None):
        self.__user = user
        self.__month_budget = month_budget if month_budget else 5000.0  # 默认月度预算5000
        self.__finance_manager = FinanceManager(user)  # 关联统计类

    # 设置/修改月度预算
    def set_month_budget(self, new_budget):
        if isinstance(new_budget, (int, float)) and new_budget > 0:
            self.__month_budget = round(new_budget, 2)
            return f"✅ 月度预算已设置为：{self.__month_budget}元"
        raise ValueError("预算金额必须为正数！")

    # 获取当月预算使用情况
    def month_budget_usage(self, year, month):
        _, total_expense, _ = self.__finance_manager.total_income_expense(year, month)
        total_expense = abs(total_expense)  # 支出取绝对值
        usage_rate = total_expense / self.__month_budget
        surplus = self.__month_budget - total_expense
        # VIP用户调用专属预警方法
        if hasattr(self.__user, "budget_remind"):
            return self.__user.budget_remind(total_expense)
        # 普通用户基础提醒
        if usage_rate >= 1:
            return f"⚠️ 普通用户预警：本月已超支！消费{total_expense}元，超预算{usage_rate*100-100:.1f}%"
        return f"✅ 本月预算使用{usage_rate*100:.1f}%，消费{total_expense}元，剩余{surplus:.2f}元"

    # 分类预算设置（拓展用）
    def set_cate_budget(self, cate, amount):
        if not hasattr(self, "__cate_budget"):
            self.__cate_budget = {}
        if isinstance(amount, (int, float)) and amount > 0:
            self.__cate_budget[cate] = round(amount, 2)
            return f"✅ 【{cate}】分类预算已设置为：{amount}元"
        raise ValueError("分类预算必须为正数！")

    def get_month_budget(self):
        return self.__month_budget

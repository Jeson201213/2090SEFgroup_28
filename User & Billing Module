# 封装用户基础类，子类实现VIP用户多态
class User:
    def __init__(self, user_id, name, balance=0.0):
        # 私有属性封装，仅通过方法访问/修改
        self.__user_id = user_id
        self.__name = name
        self.__balance = balance  # 账户总余额

    # 公共getter/setter方法，控制属性访问
    def get_user_id(self):
        return self.__user_id

    def get_name(self):
        return self.__name

    def get_balance(self):
        return round(self.__balance, 2)

    def update_balance(self, amount):
        """更新余额，amount为正收入/负支出"""
        if isinstance(amount, (int, float)):
            self.__balance += amount
            self.__balance = round(self.__balance, 2)

    def __str__(self):
        return f"用户[{self.__user_id}]：{self.__name}，账户余额：{self.get_balance()}元"


# 子类VIPUser，继承User并实现多态
class VipUser(User):
    def __init__(self, user_id, name, balance=0.0, budget_limit=5000.0, remind_threshold=0.8):
        super().__init__(user_id, name, balance)
        self.__budget_limit = budget_limit  # 月度预算额度
        self.__remind_threshold = remind_threshold  # 预算预警阈值（80%）
        self.__points = 0  # 消费积分

    # 重写父类方法，实现多态：消费累计积分
    def update_balance(self, amount):
        super().update_balance(amount)
        if amount < 0:  # 支出才累计积分，1元=1积分
            self.__points += abs(int(amount))

    # 预算预警方法，VIP专属功能
    def budget_remind(self, month_spend):
        spend_rate = month_spend / self.__budget_limit
        if spend_rate >= self.__remind_threshold:
            return f"⚠️ VIP预警：本月已消费{month_spend}元，超预算{spend_rate*100:.1f}%，请控制消费！"
        return f"✅ 本月消费{month_spend}元，预算剩余{self.__budget_limit - month_spend}元"

    def get_points(self):
        return self.__points

    def __str__(self):
        return f"VIP用户[{self.get_user_id()}]：{self.get_name()}，余额：{self.get_balance()}元，积分：{self.__points}分"

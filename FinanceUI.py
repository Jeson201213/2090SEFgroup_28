from User import User, VipUser
from Bill import IncomeBill, ExpenseBill
from FinanceManager import FinanceManager, shell_sort
from Budget import Budget
from DataPersistence import DataPersistence

# 控制台界面类，所有功能入口
class FinanceUI:
    def __init__(self):
        self.__dp = DataPersistence()  # 关联数据持久化
        self.__current_user = None  # 当前登录用户
        self.__fm = None  # 当前用户的统计对象
        self.__budget = None  # 当前用户的预算对象

    # 主菜单
    def main_menu(self):
        while True:
            print("\n===== 个人财务管理系统 =====")
            print("1. 用户注册 | 2. 账单录入 | 3. 财务统计")
            print("4. 预算管理 | 5. 数据导出 | 0. 退出系统")
            choice = input("请输入功能编号：").strip()
            if choice == "0":
                print("👋 感谢使用，再见！")
                break
            elif choice == "1":
                self.register_user()
            elif choice == "2":
                self.add_bill()
            elif choice == "3":
                self.show_stat()
            elif choice == "4":
                self.manage_budget()
            elif choice == "5":
                self.export_data()
            else:
                print("❌ 输入错误，请重新输入！")

    # 1. 用户注册
    def register_user(self):
        user_id = input("请输入用户ID：").strip()
        name = input("请输入用户名：").strip()
        balance = float(input("请输入初始余额：").strip())
        is_vip = input("是否注册VIP用户（y/n）：").strip().lower()
        try:
            if is_vip == "y":
                budget = float(input("请输入月度预算额度：").strip())
                user = VipUser(user_id, name, balance, budget)
            else:
                user = User(user_id, name, balance)
            # 保存用户
            print(self.__dp.save_user(user))
            self.__current_user = user
            self.__fm = FinanceManager(user)
            self.__budget = Budget(user, user._VipUser__budget_limit if is_vip == "y" else None)
            print(f"✅ 欢迎{user.get_name()}，已自动登录！")
        except Exception as e:
            print(f"❌ 注册失败：{e}")

    # 2. 账单录入
    def add_bill(self):
        if not self.__current_user:
            print("❌ 请先注册/登录用户！")
            return
        try:
            bill_type = input("请选择账单类型（收入/支出）：").strip()
            amount = float(input("请输入金额：").strip())
            date = input("请输入日期（yyyy-mm-dd，默认当前）：").strip()
            cate = input("请输入收支分类：").strip()
            remark = input("请输入备注（可选）：").strip()
            # 创建账单对象
            if bill_type == "收入":
                bill = IncomeBill(amount, date, cate, remark)
            elif bill_type == "支出":
                bill = ExpenseBill(-abs(amount), date, cate, remark)  # 统一转为负数
            else:
                raise ValueError("账单类型只能是「收入」或「支出」")
            # 保存账单+更新用户余额
            print(self.__dp.save_bill(bill))
            self.__current_user.update_balance(bill.get_amount())
            print(f"✅ 账户余额已更新：{self.__current_user.get_balance()}元")
        except Exception as e:
            print(f"❌ 录入失败：{e}")

    # 3. 财务统计（核心功能展示）
    def show_stat(self):
        if not self.__fm:
            print("❌ 请先注册/登录用户！")
            return
        print("\n===== 财务统计 =====")
        year = input("请输入统计年份（留空则全部）：").strip()
        month = input("请输入统计月份（留空则全部）：").strip()
        # 总收支
        total_i, total_e, total = self.__fm.total_income_expense(year, month)
        print(f"📊 总统计：收入{total_i}元 | 支出{abs(total_e)}元 | 结余{total}元")
        # 分类统计
        cate_stat = self.__fm.category_stat(year, month)
        print("\n📈 分类统计：")
        for t in cate_stat:
            print(f"【{t}】：{cate_stat[t]}")
        # 支出TOP3
        top3 = self.__fm.top_n_expense(3, year, month)
        print("\n🔥 支出TOP3：")
        for i, b in enumerate(top3, 1):
            print(f"{i}. {b}")

    # 4. 预算管理
    def manage_budget(self):
        if not self.__budget:
            print("❌ 请先注册/登录用户！")
            return
        year = input("请输入年份：").strip()
        month = input("请输入月份：").strip()
        new_budget = input(f"是否修改月度预算（当前{self.__budget.get_month_budget()}元），输入新金额/留空不修改：").strip()
        if new_budget:
            print(self.__budget.set_month_budget(float(new_budget)))
        # 查看预算使用情况
        print(self.__budget.month_budget_usage(year, month))

    # 5. 数据导出
    def export_data(self):
        if not self.__fm:
            print("❌ 请先注册/登录用户！")
            return
        stat_data = self.__fm.category_stat()
        print(self.__dp.export_stat(stat_data))

# 程序入口，直接运行即可启动系统
if __name__ == "__main__":
    ui = FinanceUI()
    ui.main_menu()

# 2090SEFgroup_28_TASK1

2090SEF_group_28 project

Member 1: Core Data Layer - Development of Billing and User Modules (Lead: Implementation of Hash Table)          (YE Zeyang)
Core Responsible Modules (2 independent Python files)
User.py: Design the user class system, embodying OOP inheritance / polymorphism
Base class: User (encapsulating user ID, name, account balance, basic information);
Subclass: VipUser (inheriting from User, adding budget limit, consumption reminder threshold, points system), embodying polymorphism (overriding points calculation and budget warning methods).
Bill.py: Design the bill class system, encapsulating core revenue and expenditure data
Base class: Bill (encapsulating bill ID, amount, date, category, remarks, and abstract method get_type());
Subclasses: IncomeBill/ExpenseBill (inheriting from Bill, implementing get_type(), overriding amount verification methods), embodying abstraction + polymorphism.
Supporting Development Tasks
Implement basic verification of revenue and expenditure data (non-negative amount, valid date format, standardized category);
Lead the implementation of Task 2 hash table (self-learned data structure): encapsulate a custom hash table class, realize quick query of bills by category / month, quick retrieval of user information, and integrate the hash table into the query methods of the Bill/User modules;
Write test cases for this module (such as creation of different types of bills, addition, deletion, modification and query of user information, test of hash table query efficiency).
Collaboration Points
Provide Member 2 with instantiation methods and data calling interfaces of the Bill/User classes for use in the statistics module;
Provide Member 3 with original bill / user data for saving and display by the data persistence and visualization module.

Member 2: Business Logic Layer - Development of Financial Statistics and Budget Module (Leading: Implementation of Shell Sort)         (LI Yichen)
Core Responsible Modules (2 independent Python files)
FinanceManager.py: Core business logic class that encapsulates all statistical/budget functions, embodying OOP encapsulation.
Core functions: Statistics of total income and expenditure, classification statistics, monthly/quarterly/annual summaries, consumption TOP N filtering, budget setting and overspending warning;
Provides a unified statistical method interface externally, hiding internal calculation logic.
Budget.py: Budget management class, supporting FinanceManager to implement budget control.
Functions: Classification budget setting (e.g., 500 per month for catering), total budget setting, real-time overspending reminders, calculation of budget usage progress.
Supporting Development Tasks
Implement multi-dimensional financial statistical logic, complete various summary calculations based on the Bill data provided by Member 1;
Lead the implementation of Task 2 Shell Sort (self-learned algorithm): Integrate Shell Sort into the statistical module to sort income and expenditure records by amount/date, and sort classified consumption by amount, and compare the efficiency with the sorting algorithms covered in the course;
Optimize statistical query efficiency in combination with Member 1's hash table (e.g., first filter by category through the hash table, then sort with Shell Sort);
Write test cases for this module (such as monthly statistics, budget overspending reminders, sorting function tests).
Collaboration Points
Obtain standardized Bill/User data from Member 1 and call the query interface provided by them;
Provide processed statistical result data (such as monthly income and expenditure summaries, classification proportion data) to Member 3 for visualization and storage.




Member 3: Interaction and Implementation Layer - Data Persistence + Visualization + Interface Module Development (Lead: Integration and Testing of Self-Learned Content)                  (SHI Yuanming)
Core Responsible Modules (2 independent Python files)
DataPersistence.py: Data persistence class, realizing permanent data storage to avoid loss when the program exits
Functions: Based on the csv library (self-learned), realizing the writing/reading/modification of Bill/User/statistical results, supporting bill import/export;
Compatible with Member 1's Bill class and Member 2's statistical results, automatically formatting data into a format savable by csv.
FinanceUI.py: System interaction interface class, realizing interaction between users and the system
Basic version: Realizing a console interaction interface (main menu, function selection, input and output) based on print(), including entrances to all functions (such as bill entry, query and statistics, budget setting);

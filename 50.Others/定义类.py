#定义类：
class Student(object):
    #类变量：与具体对象无关
    sum = 0

    # 实例方法:关联的是对象,self代表对象本身
    def __init__(self,name,age):    #构造函数
        # 实例变量
        self.name = name
        self.age = age
        self.__score = 0            #可以对实例变量进行初始赋值
        self.__class__.sum +=1      #实例方法中调用类变量，方法二
        # print('当前学生人数为：'+ str(Student.sum))     #实例方法中调用类变量，方法一
    #实例方法，可以调用实例变量
    def __do_homework(self):        #变量或函数名前有双下划线，表示其为私有的，外部无法访问
        print('Homework')           #私有变量，Python内部自动添加了类名：_Student__do_homework()
                                    #变量或函数名后加双下划线，不为私有

    def marking(self,score):        #所有修改类变量均应该通过方法来完成
        if score < 0:
            return '不能打负分'
        self.__score = score
        print(self.name + '同学本次考试成绩为:%s'%self.__score)

    #类方法:通过cls关联的是类本身，需在函数前添加@classmethod
    @classmethod
    def plus_sum(cls):
        cls.sum +=1                 #类方法中调用类变量
        print(cls.sum)

    #静态方法:无关键词,可同时被类和对象调用
    @staticmethod
    def add(x,y):
        print(Student.sum)          #静态方法中调用类变量
        print('This is a staticmethod.')




#实例化类创建对象
student1 = Student('Bart Simpson', 18)   #调用定义实例方法时不需要self变量
result = student1.marking(30)
student1.__score = 1                     #相当于新生成了一个实例变量属性，与构造函数里的不同
print(student1.__score)
# print(result)
# Student.plus_sum()
# student1.add(1,2)
# # Student.plus_sum()
# student2 = Student('sd2fs dfon', 22)
# Student.plus_sum()
# student3 = Student('xhl dfon', 12)
# Student.plus_sum()
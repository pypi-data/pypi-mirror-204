from dateutil import parser
import time

class MyTime():
    def __init__(self):
        self.current_time = parser.parse(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    def currentTime(self):
        return self.current_time

    # 计算距离今日的天数
    def current_diffTime(self, before_time):
        diffTime = self.current_time - before_time
        return diffTime.days

    # 计算自定义两个的时间差
    def before_after_time(self, before_time, after_time):
        diffTime = after_time - before_time
        return diffTime.days

    # 计算你多大了
    def howOld(self, birthYear):
        currentYear = self.currentTime().year
        old = int(currentYear) - int(birthYear)
        return old

if __name__ == '__main__':
    myTime = MyTime()
    before_time = parser.parse('2021/08/31 08:53:01')
    diffDays = myTime.current_diffTime(before_time)
    print(diffDays)

    after_time = parser.parse('2021/09/30')  # 之后时间
    diffDays = myTime.before_after_time(before_time, after_time)
    print(diffDays)

    print(myTime.currentTime())

    old = myTime.howOld('1988')
    print(old)




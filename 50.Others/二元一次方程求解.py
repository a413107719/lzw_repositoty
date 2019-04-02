import math

def EYYCFC(a,b,c):
    x1 = (-b + math.sqrt(b * b-4 * a * c))/(2 * a)
    x2 = (-b - math.sqrt(b * b-4 * a * c))/(2 * a)

    delta = b * b - 4 * a * c
    if delta <= 0:
        print("无解")
    elif delta == 0:
        print("一元二次方程的解是:" + str(x1))
    else:
        print("一元二次方程的解是:" + "x1="+str(x1)+","+ "x1=" + str(x2))
while(1):
    print("请输入二次方参数a:")
    x = float(input())
    if x == 0:
        print("二次方参数不为零")
        continue
    else:
        break
print("请输入一次方参数b:")
y = float(input())
print("请输入常数项参数c:")
z = float(input())
EYYCFC(x , y , z)

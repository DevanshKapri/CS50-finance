def cac(n, m, t):
    if t == 1:
        return n + m
    elif t == 2:
        return n - m


n1 = int(input("Enter the first Number "))
m1 = int(input("Enter the Second  Number "))
t1 = int(input("Enter the 1 for addition Or 2 for Subtraction "))
print(cac(n1, m1, t1))

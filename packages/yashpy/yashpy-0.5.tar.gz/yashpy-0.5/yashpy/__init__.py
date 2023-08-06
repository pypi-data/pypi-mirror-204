def add(num1,num2):
    a=num1+num2
    return a
def sub(num1,num2):
    return num1-num2
def mult(num1,num2):
    return num1*num2
def div(num1,num2):
    return num2 / num1
def gcd(x, y):

	if x > y:
		small = y
	else:
		small = x
	for i in range(1, small + 1):
		if((x % i == 0) and (y % i == 0)):
			gcd = i
			
	return gcd


def is_prime(n):
    for i in range(2,int(n**0.5)+1):
        if n%i==0:
            return False
        
    return True


def even_odd(n):
    if(n%2==0):
        print("number is even:")
    else:
        print("number is odd:")
        
def lcm(a, b):
    greater = max(a, b)
    smallest = min(a, b)
    for i in range(greater, a*b+1, greater):
        if i % smallest == 0:
            return i
 
def factorial(n):
    fact = 1

    for i in range(1,n+1):
     fact = fact * i
    print (fact)
    
    
def is_negative(num):
    if num > 0:
       print("it is a Positive number")
    elif num == 0:
       print(" it is a Zero")
    else:
       print("it is a Negative number")
def is_armstrong(num):
    num_str = str(num)
    n = len(num_str)
    sum = 0
    for digit in num_str:
        sum += int(digit)**n
    if sum == num:
        return True
    else:
        return False
    
def pow(n1,n2):
    a=float(n1**n2)
    return a

def pi():
    return 22/7


def sqrt(x):
 
    # Base cases
    if (x == 0 or x == 1):
        return float(x)
 
    
    i = 1
    result = 1
    while (result <= x):
 
        i += 1
        result = i * i
 
    return float(i - 1)

def degree(x):
    pi=22/7
    degree=(x*180)/pi
    return degree


def radian(degrees):
    pi=22/7
    return degrees * pi / 180

radians = radian(180)
print(radian)
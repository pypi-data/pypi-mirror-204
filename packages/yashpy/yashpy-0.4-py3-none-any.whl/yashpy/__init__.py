def add(num1,num2):
    a=num1+num2
    print("addition of this two numbers is:")
    return a
def sub(num1,num2):
    print("subtraction of two numbers is:")
    return num1-num2
def mult(num1,num2):
    print("multilplication of the two numbers is:")
    return num1*num2
def div(num1,num2):
    print("divisio of the two numbers is:")
    return num1 % num2
def gcd(x, y):

	if x > y:
		small = y
	else:
		small = x
	for i in range(1, small + 1):
		if((x % i == 0) and (y % i == 0)):
			gcd = i
	print ("The gcd of num1 and num2 is : ", end="")		
	return gcd




# prints 12
print ("The gcd of num1 and num2 is : ", end="")


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

    print ("The factorial of number is : ",end="")
    print (fact)
    
    
def is_negative(num):
    if num > 0:
       print("it is a Positive number")
    elif num == 0:
       print(" it is a Zero")
    else:
       print("it is a Negative number")

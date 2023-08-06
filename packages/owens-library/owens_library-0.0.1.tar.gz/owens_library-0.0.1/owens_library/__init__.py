def verifyNumberRange(low,high,inputFunction):
  x=inputFunction
  while x<low and x>high:
    x=inputFunction
  return x
def numMultiplier(num, range):
  x=1
  for y in range(range):
    print(x*num)
    x+=1
def vowelCounter(text):
  y=0
  for x in text.lower():
    if x in "aeiou":
      y+=1
  return y
def averageList(list):
  x=0
  a=0
  for z in list:
    x+=z
    a+=1
    
  return x/a
def reverseString(text):
  reverse=""
  for x in text:
    reverse = x + reverse
  return x
def prime(num):
  is_prime=True
  for i in range(2,num):
    if num % i == 0:
      is_prime=False
  return is_prime
def BiggestNumInList(list):
  x=0
  for num in list:
    if x<num:
      x=0
      x+=num
  return x
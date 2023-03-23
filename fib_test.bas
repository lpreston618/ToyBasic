1 rem A program to print the Fibonacci
2 rem sequence up to 100 numbers
10 let a = 1
20 let b = 1
30 if b > 100 then goto 1000
35 print b
40 let c = a
50 let a = a+b
60 let b = c
70 goto 30
1000

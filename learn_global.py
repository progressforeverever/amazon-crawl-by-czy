a = 0  # initialize variable a
def coo():
    global a  # call a
    a += 1
    return a
 
for i in range(10):
    print(coo())
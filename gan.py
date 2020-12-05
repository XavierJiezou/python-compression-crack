f = open('pwd.txt', 'w')
l = [str(i) for i in range(10)]
for i in l:
    for j in l:
        for k in l:
            f.write(i+j+k+'\n')
f.close()

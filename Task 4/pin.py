import hashlib

x = [str(i) for i in range(10)]


#Checks all possible 6-digit pins, including ones that start with 0
for a in x:
    for b in x:
        for c in x:
            for d in x:
                for e in x:
                    for f in x:

                        X = a+b+c+d+e+f

                        H = hashlib.sha256(X.encode("utf-8")).hexdigest()

                        #Paste the bytes from the checkpin column in clientDB here
                        if H == "7f72932585059397e5dfaca5cfa77515025e0c31e6e20f70ce814e0b3690f5ee":
                            print(X,H)
                            exit()
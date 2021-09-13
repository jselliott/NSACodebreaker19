import hashlib

#Checks all possible 6-digit pins, including ones that start with 0
for x in range(999999):

    X = str(x).zfill(6)

    H = hashlib.sha256(X.encode("utf-8")).hexdigest()

    #Paste the bytes from the checkpin column in clientDB here
    if H == "7f72932585059397e5dfaca5cfa77515025e0c31e6e20f70ce814e0b3690f5ee":
        print(X,H)
        exit()

print( "\033c\033[40;37m\give the file .txt script to show ? ")
a=input()
f1=open(a,"r")
b=f1.read()
f1.close()
b=b.replace("\\\\","\\").replace("\\n","\n").replace("\\r","\r").replace("\\s"," ").replace("\\t","\t").replace("\\e",chr(27))
c=b.split("\\x")
counter=0
strings=""
for r in c:
    if counter==0:
        strings=r
    else:
        e=""
        if len(r)>1:
            e=int(r[:1],16)
            rr=r[2:]
            strings=strings+chr(e)+rr
    counter=counter+1
a=a.replace(".txt",".dat")
f1=open(a,"w")
f1.write(strings)
f1.close()

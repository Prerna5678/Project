# Read file (r) mode
f=open("file1.py","r")
data=f.read()
print(data)
f.close()

# Write 
f=open("file4.txt","w")
f.write("How are you")
print("write sucessfully")
f.close()
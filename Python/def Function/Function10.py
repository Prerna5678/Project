i=0
def main():
    global i
    print("Enter the function")
    if i<5:
        i+=1
        main()
    print("Exit")
main()
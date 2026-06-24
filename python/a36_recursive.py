def rec_fac(n):
    if n == 1:
        return 1
    else:
        return n * rec_fac(n-1)
    

def main():
    print(rec_fac(100))

if __name__ == "__main__":
    main()
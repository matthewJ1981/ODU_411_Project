import sys
if __name__ == "__main__":       
    host = "mysql"
    pw = "1234"
    for i, arg in enumerate(sys.argv):
        if arg == "root":
            host = "411orang.cpi.cs.odu.edu"
            pw = "sdafaewgaaer"
        file = open("./.cnf", "w")
        file.write("[client]\n")
        file.write("host = " + host + "\n")
        file.write("user = root\n")
        file.write("password = " + pw + "\n")
        #file.write("database = littlelearners\n")
        file.close()
        
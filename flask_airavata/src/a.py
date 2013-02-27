from sh import ls
import sh
#print(sh.ls("/"))
run = sh.Command("/home/heshan/Dev/setup/futuregrid/fgairavata/src/parser.sh")
run()



#ls = ls.bake("-la")
#print(ls) # "/usr/bin/ls -la"

# resolves to "ls -la /"
#print(ls("/"))


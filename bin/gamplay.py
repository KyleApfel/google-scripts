import subprocess
import re
import sys
import glob

# GAM Home Directory
GAM = "location/here/gam.py"

# Getting List of Users
output = subprocess.check_output(GAM + " print users suspended", shell=True)
users = output.split('\n')

# Get and Parse User Info

def userParse(users):
  output = subprocess.check_output(GAM + " info user " + users + " userview", shell=True)
  if not "Error" in output:
      firstname = re.search('First Name: (.+?)\n', output)
      if firstname:
          firstname = firstname.group(1)

      lastname = re.search('Last Name: (.+?)\n', output)
      if lastname:
          lastname = lastname.group(1)

      title = re.search('title: (.+?)\n', output)
      if title:
          title = title.group(1)
      else:
          title = ''

      number = re.search('value: (.+?)\n', output)
      if number:
          number = number.group(1)
          number = number[0:3] + '.' + number[3:6] + '.' + number[6:]
          number = "| Cell: " + number
      else:
          number = ''

      email = re.search('User: (.+?)\n', output)
      if email:
          email = email.group(1)
      
      emailTemp(firstname, lastname, title, number, email)

def emailTemp(firstname, lastname, title, number, email):
  emailtemplate = """
  <div style="font-size:small">  <font size="4" face="arial, helvetica, sans-serif" color="#000000">    %s %s  </font>   </div>   <div style="font-size:small">  <font face="arial, helvetica, sans-serif" color="#666666">    %s    <br>  </font>  <font face="arial, helvetica, sans-serif" color="#99999">    Office: 555.555.5555 %s    <br>    Email:    <a href="mailto:%s" target="_blank">     %s   </a>       <br><br>   <img src="" width="96" height="51">   <br><br>   <hr>  </font>   </div>   <font size="1" color="#999999">  This communication along with its attachments may contain confidential information belonging to the sender. This information is intended only for delivery to the individual named above. If you are not the intended recipient, you are hereby notified that any disclosure, copying, distribution, or the taking of any action in reliance on the contents of this transmission is strictly prohibited.   </font>
  """ % (firstname, lastname, title, number, email.lower(), email.lower())
  
  email = "sigs/" + email
  file = open(email.lower(), 'w')
  file.write(emailtemplate)
  file.close()
  
  print ("Created: " + firstname + " " + lastname + "'s Template File")

def updateSig():
  sigsToUpdate = glob.glob("./sigs/*")
  x = 1
  while x < len(sigsToUpdate): 
    email = sigsToUpdate[x][7:]
#   print (GAM + " user " + email + " signature file " + sigsToUpdate[x])
    output = subprocess.check_output(GAM + " user " + email + " signature file " + sigsToUpdate[x], shell=True)
    print ("Updated: " + email + "'s Signature")
    x += 1

def manUpdateSig(email):
  output = subprocess.check_output(GAM + " user " + email + " signature file ./sigs/" + email, shell=True)
  print ("Updated: " + email + "'s Signature")

def userLoop():
  x = 1
  while x < len(users)-1:
    if "True" in users[x]:
      print users[x]
      x += 1
    else:
      users[x] = users[x][:-7]
      userParse(users[x])
    x += 1

def prompt():
  print ("::Kyle's Email Signature Updater::\n")
  print ("-- Options -- ")
  print ("1 :: Loop Through All Users")
  print ("2 :: Update Specific User")
  print ("3 :: Mystery Option\n")
  prompt = raw_input("What You Wanna Do? ")
  return prompt 

def main(): 
  option = prompt()

  if option == "1":
    userLoop()
    updateSig()
  elif option == "2":
    who = raw_input("\nWhat's Their Email? ")
    userParse(who)
    manUpdateSig(who)
  elif option == "3":
    print "\nThere is no mystery, mystery solved. Now stop playing around.\n"
    main()
  else:
    print "\nTry Again\n"
    main()

main()

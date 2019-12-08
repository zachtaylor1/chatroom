from socket import AF_INET, socket, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread
import sys
import tkinter
from tkinter import *

quitcmd = '/quit'
default_port = 12345

login_info = {"test": "123"}
util_commands = {"q_user_:", "v_login_:", "r_user_:", "c_users_:", "l_users_:"}

#------------- tkinter stuff -----------------------------------------------
root = tkinter.Tk()
root.title('Please give me a good grade')

username = StringVar()
password = StringVar()
password2 = StringVar()
host_var = StringVar()
port_var = StringVar()

user = None
utility = None
port = None
host = None

def connect():
    global port
    global host
    global utility
    try:
        if not port_var.get():
            port = default_port
        else:
            port = port_var.get()
        host = host_var.get()
        utility = Utility("utility", host, port)
        utility.run_loops()
        host_frame.pack_forget()
        login_frame.pack()
    except:
        host_lbl.configure(text = "could not connect")

def try_login():
    if not username.get() or not password.get():
        login_lbl.configure(text="all fields must be filled")
    else:
        utility.send("v_login_: " + username.get() + " " + password.get())

def login(valid):
    global user
    if valid == 'True':
        user = User(username.get(), host, port)
        send_button.configure(command = user.send)
        user.run_loops()
        login_frame.pack_forget()
        main_frame.pack()
    else:
        user_entry.delete(0, END)
        pass_entry.delete(0, END)
        login_lbl.configure(text="Incorrect username/password")

def nav_register():
    user_entry.delete(0, END)
    pass_entry.delete(0, END)
    login_frame.pack_forget()
    register_frame.pack()

def nav_login():
    register_frame.pack_forget()
    login_frame.pack()

def try_register():
    if not username.get() or not password.get() or not password2.get():
        register_lbl.configure(text="all fields must be filled")
    elif password.get() != password2.get():
        register_lbl.configure(text="passwords do not match")
    else:
        utility.send("r_user_: " + username.get() + " " + password.get())

def register(valid):
    if(valid == "True"):
        nav_login()
    else:
        register_lbl.configure(text="unable to register: username may be taken")

#host_frame----------------------------------

host_frame = tkinter.Frame(root, bd=100)
host_grid = tkinter.Frame(host_frame)
Label(host_grid, text='Host:').grid(row=0)
Label(host_grid, text='Port (optional)').grid(row=1)
host_entry = Entry(host_grid, textvariable=host_var)
port_entry = Entry(host_grid, textvariable=port_var)
host_entry.grid(row=0, column=1)
port_entry.grid(row=1, column=1)
host_grid.pack()
host_btn = tkinter.Button(host_frame, text="Connect", command=connect)
host_btn.pack(pady = 10)
host_lbl = tkinter.Label(host_frame)
host_lbl.pack()

#end of host_frame---------------------------

#login_frame---------------------------------

login_frame = tkinter.Frame(root, bd=100)
login_grid = tkinter.Frame(login_frame)
Label(login_grid, text='Username').grid(row=0) 
Label(login_grid, text='Password').grid(row=1)
Label(login_grid, text='Host:').grid(row=2)
user_entry = Entry(login_grid, textvariable=username) 
pass_entry = Entry(login_grid, textvariable=password)
host_entry = Entry(login_grid, textvariable=host_var)
user_entry.grid(row=0, column=1) 
pass_entry.grid(row=1, column=1) 
host_entry.grid(row=2, column=1)
login_grid.pack()
login_btn = tkinter.Button(login_frame, text="Login", command=try_login)
login_btn.pack(pady = 10)
nav_reg_btn = tkinter.Button(login_frame, text="Register", command=nav_register)
nav_reg_btn.pack()
login_lbl = tkinter.Label(login_frame)
login_lbl.pack()

#end of login_frame------------------------

#register_frame----------------------------

register_frame = tkinter.Frame(root, bd=100)

register_grid = tkinter.Frame(register_frame)
Label(register_grid, text='Username').grid(row=0) 
Label(register_grid, text='Password').grid(row=1)
Label(register_grid, text='Reenter Password').grid(row=2)
e1 = Entry(register_grid, textvariable=username) 
e2 = Entry(register_grid, textvariable=password)
e3 = Entry(register_grid, textvariable=password2) 
e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)
register_grid.pack()
register_btn = tkinter.Button(register_frame, text="Register", command=try_register)
register_btn.pack(pady=10)
reg_back_btn = tkinter.Button(register_frame, text="Back", command=nav_login)
reg_back_btn.pack(pady=10)
register_lbl = tkinter.Label(register_frame)
register_lbl.pack()

#end of register_frame---------------------

#main_frame--------------------------------

main_frame = tkinter.Frame(root)

#display users
member_frame=tkinter.Frame(main_frame)
member_label = tkinter.Label(member_frame, text="Active users:")
member_label.pack(side=TOP)
member_sb = tkinter.Scrollbar(member_frame)
member_list = tkinter.Listbox(member_frame, yscrollcommand=member_sb.set)
member_sb.configure(command=member_list.yview)
member_sb.pack(side=RIGHT, fill=Y)
member_list.pack(side=LEFT, fill=BOTH, expand=True)


#display incoming messages
messages_frame = tkinter.Frame(main_frame)
scrollbar = tkinter.Scrollbar(messages_frame)
msg_list = tkinter.Text(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.configure(command=msg_list.yview)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)


#send messages
sender_frame = tkinter.Frame(main_frame)
sender_label=tkinter.Label(sender_frame, text="Type your message here:")
sender_label.pack(side=TOP)
text_field = tkinter.Text(sender_frame, height=3, width=50, wrap=WORD)
text_field.pack(side=LEFT, fill=BOTH)
send_button = tkinter.Button(sender_frame, text="Send")
send_button.pack(side=RIGHT)


member_frame.pack(side=RIGHT, fill=Y, expand=True)
messages_frame.pack()
sender_frame.pack()

#end main_frame--------------------------------------

class Chatting:
    def __init__(self, host, port):
        print('Chatting.__init__')
        self.addr = (host,port)
        self.BUFSIZ = 512
        self.sock = socket(AF_INET,SOCK_STREAM)
    def send_mesg(self, sock, msg):
        hdr = bytearray('00','utf-8')
        hdr[0] = len(msg) // 256
        hdr[1] = len(msg) % 256
        assert(len(hdr) == 2)
        sock.sendall(hdr)
        sock.sendall(bytes(msg,'utf-8'))
    def recv_mesg(self, sock):
        hdr = b''
        while len(hdr) < 2:
            hdr += sock.recv(2 - len(hdr))
        nbytes = hdr[0] * 256 + hdr[1]
        nbytes_read = 0
        data = b''
        while nbytes_read < nbytes:
            data += sock.recv(nbytes - nbytes_read)
            nbytes_read = len(data)
        return data.decode('utf-8')

class Server(Chatting):
    def __init__(self, host, port:int):
        super().__init__(host,port)
        print('Server.__init__')
        self.sock.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.addr = ('', port)
        self.sock.bind(self.addr)
        self.cli_info = {}
    def start(self):
        self.sock.listen(1)
        print('waiting')
        self.accept_thread = Thread(target=Server.accept_loop,
                                    args=(self,))
        self.accept_thread.start()
        self.accept_thread.join()
        self.sock.close()
    def accept_loop(self):
        while True:
            cli,caddr = self.sock.accept()
            th = Thread(target = Server.handle_cli,
                        args = (self,cli))
            self.cli_info[cli] = {'addr': caddr,
                                  'thread': th}
            th.start()
    def handle_cli(self,cli):
        name = self.recv_mesg(cli)
        role = self.recv_mesg(cli)
        mesg = "{} has joined the chat".format(name, role)
        print(mesg)
        self.cli_info[cli]['name'] = name
        self.cli_info[cli]['role'] = role
        if self.cli_info[cli]['role'] == 'utility':
            self.handle_util(cli)
        self.list_users()
        self.broadcast(mesg)
        while True:
            try:
                msg = self.recv_mesg(cli)
            except OSError:
                print('connection closed')
                break
            if msg != quitcmd:
                self.broadcast(msg)
            else:
                deleted = []
                for cli in self.cli_info:
                    cli_name = self.cli_info[cli]['name']
                    cli_role = self.cli_info[cli]['role']
                    if cli_name == name:
                        if cli_role == 'viewer' or cli_role == 'user':
                            self.send_mesg(cli,quitcmd)
                        deleted.append(cli)
                for cli in deleted:
                    cli.close()
                    del self.cli_info[cli]
                self.broadcast('client left')
                break
    def broadcast(self, msg):
        deleted = []
        for cli in self.cli_info:
            if self.cli_info[cli]['role'] == 'viewer' or self.cli_info[cli]['role'] == 'user':
                name = self.cli_info[cli]['name']
                print('broadcast', msg)
                try:
                    self.send_mesg(cli, msg)
                except OSError:
                    print('possibly closed. removed from the connections')
                    deleted.append(cli)
        for d in deleted:
            del self.cli_info[d]
    def list_users(self):
        self.broadcast("c_users_:")
        for cli in self.cli_info:
            if self.cli_info[cli]['role'] == 'user':
                msg = "l_users_: " + self.cli_info[cli]['name']
                self.broadcast(msg)
    def verify_login(self, cli, user, passw):
        if user in login_info and login_info[user] == passw:
            self.send_mesg(cli, "v_login_: True")
        else:
            self.send_mesg(cli, "v_login_: False")
    def register_user(self, cli, user, passw):
        if user in login_info:
            self.send_mesg(cli, "r_user_: False")
        else:
            login_info[user]=passw
            self.send_mesg(cli, "r_user_: True")
    def handle_util(self, cli):
        while True:
            try:
                msg = self.recv_mesg(cli)
            except OSError:
                print('connection closed')
                break
            msglist = msg.split()
            if msglist[0] in util_commands:
                if msglist[0] == "v_login_:":
                    self.verify_login(cli, msglist[1], msglist[2])
                elif msglist[0] == "r_user_:":
                    self.register_user(cli, msglist[1], msglist[2])
                elif msglist[0] == "q_user_:":
                    if self.cli_info[cli]['role'] == "user":
                        mesg = "{} has left the chat".format(self.cli_info[cli]['name'])
                        self.broadcast(mesg)
                    cli.close()
                    del self.cli_info[cli]
            else:
                print("bad command")

class Client(Chatting):
    def __init__(self, name, host, port):
        super().__init__(host,port)
        print('Client.__init__')
        self.name = name
        self.sock.connect(self.addr)
        self.send_mesg(self.sock, name)

class Viewer(Client):
    def __init__(self, name, host, port:int):
        super().__init__(name,host,port)
        print('Viewer.__init__')
        self.send_mesg(self.sock, 'viewer')
    def recv_loop(self):
        while True:
            msg = self.recv_mesg(self.sock)
            if msg == quitcmd:
                print('quit')
                break
            else:
                print(msg)

class Sender(Client):
    def __init__(self, name, host, port:int):
        super().__init__(name,host,port)
        print('Sender.__init__')
        self.name = name
        self.send_mesg(self.sock,'sender')
    def send_loop(self):
        while True:
            user_msg = input('Enter input: ')
            if user_msg != quitcmd:
                msg = self.name + ':' + user_msg
            else:
                msg = user_msg
            try:
                self.send_mesg(self.sock, msg)
            except OSError:
                print('connection closed')
                break

class Utility(Client):
    def __init__(self, name, host, port:int):
        super().__init__(name,host,port)
        print('Util.__init__')
        self.name = name
        self.send_mesg(self.sock,'utility')
    def send(self, msg):
        try:
            self.send_mesg(self.sock, msg)
        except OSError:
            print('connection closed')
    def recv_loop(self):
        while True:
            msg = self.recv_mesg(self.sock)
            print("msg: " + msg)
            msglist = msg.split()
            if msglist[0] in util_commands:
                if msglist[0] == "v_login_:":
                    login(msglist[1])
                elif msglist[0] == "r_user_:":
                    register(msglist[1])
            print(msg)
    def run_loops(self):
        recv_thread = Thread(target=self.recv_loop)
        recv_thread.start()
        return recv_thread

class User(Client):
    def __init__(self, name, host, port:int):
        super().__init__(name,host,port)
        print('User.__init__')
        self.name = name
        self.send_mesg(self.sock,'user')
    def recv_loop(self):
        while True:
            msg = self.recv_mesg(self.sock)
            if msg == quitcmd:
                print('quit')
                break
            else:
                print(msg)
                msglist = msg.split()
                if msglist[0] == "c_users_:":
                    member_list.delete(0, END)
                elif msglist[0] == "l_users_:":
                    member_list.insert(END, msglist[1])
                else:
                    msg_list.insert(END, msg)
    def send(self):
        user_msg = self.name + ': ' + text_field.get(1.0, END)
        try:
            self.send_mesg(self.sock, user_msg)
        except OSError:
            print('connection closed')
        text_field.delete(1.0, END)
    def run_loops(self):
        recv_thread = Thread(target=self.recv_loop)
        recv_thread.start()
        return recv_thread

def main(argc, argv):
    if argc<2:
        host_frame.pack()
        root.mainloop()
    elif argv[1] == 'server':
        host = argv[2]
        if argc <= 3:
            port = default_port
        else:
            port = int(argv[3])
        server = Server(host,port)
        server.start()
    elif argv[1] == 'viewer':
        name = argv[2]
        host = argv[3]
        if argc <= 4:
            port = default_port
        else:
            port = int(argv[4])
        viewer = Viewer(name,host,port)
        viewer.recv_loop()
    elif argv[1] == 'sender':
        name = argv[2]
        host = argv[3]
        if argc <= 4:
            port = default_port
        else:
            port = int(argv[4])
        viewer = Sender(name,host,port)
        viewer.send_loop()
    elif argv[1] == 'user':
        name = argv[2]
        host = argv[3]
        if argc <= 4:
            port = default_port
        else:
            port = int(argv[4])
        viewer = User(name,host,port)
        send_button.configure(command = viewer.send)
        host_frame.pack()
        viewer.run_loops()
        root.mainloop()
    else:
        print("Unknown command")

if __name__ == '__main__':
    main(len(sys.argv), sys.argv)

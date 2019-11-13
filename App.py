import wx
import File_IO as fio
import User as user
import Secreter as sec
import ISecretObject as isec

class N1PageUsers(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent=parent)
        users = fio.get_available_user_list()
        self.lb = wx.ListBox(parent=self, pos=(20, 60))
        if len(users) == 0:
            self.txt = wx.StaticText(self, label="Sorry, no users were found. Please create a user first.", pos=(20, 60))
        else:
            self.txt = wx.StaticText(self, label="Select a user and type in your password to login:", pos=(20, 20))

            self.pstxt = wx.StaticText(self, label="Password:", pos=(200, 40))
            self.tbps = wx.TextCtrl(self, pos=(200, 60), style=wx.TE_PASSWORD)
            btn = wx.Button(parent=self, label="Login", pos=(200, 100))
            btn.Bind(event=wx.EVT_BUTTON, handler=self.OnLogin)
            self.RefreshList()


    def RefreshList(self):
        user_list = fio.get_available_user_list()
        self.lb.Clear()
        for u in user_list:
            self.lb.Append(u)


    def OnLogin(self, event):
        ps = self.tbps.GetValue()
        if len(ps) == 0:
            wx.MessageBox('Please enter a valid password.', 'Error', wx.OK)
        else:
            res = self.lb.GetSelection()
            if res == 'NOT_FOUND':
                wx.MessageBox('Please select an item.', 'Error', wx.OK)
            else:
                name = self.lb.GetString(res)
                key = sec.make_key(fio.get_salt(name), str(ps))
                self.GetParent().GetParent().GetParent().key = key
                usr = fio.get_user(name, key)
                if usr.salt == 'bad':
                    wx.MessageBox('Wrong password. Try again.', 'Error', wx.OK)
                else:
                    self.GetParent().GetParent().GetParent().OnUserEnter(usr, key)



class N1PageNewUser(wx.Panel):
    tbun = None
    tbps = None
    def __init__(self, parent):
        super().__init__(parent=parent)
        untxt = wx.StaticText(self, label="Username:", pos=(20, 40))
        self.tbun = wx.TextCtrl(self, pos=(20, 60))
        pstxt = wx.StaticText(self, label="Master Password:", pos=(20, 100))
        self.tbps = wx.TextCtrl(self, pos=(20, 120), style=wx.TE_PASSWORD)
        button = wx.Button(parent=self, label="Create User", pos=(20, 160))
        button.Bind(event=wx.EVT_BUTTON, handler=self.CreateUser)



    def CreateUser(self, event):
        un = self.tbun.GetValue()
        ps = self.tbps.GetValue()

        if un != "" and ps != "":
            if len(ps) >= 10:
                users = fio.get_available_user_list()
                make_user = True
                for u in users:
                    if u == un:
                        make_user = False
                        break
                if make_user:
                    usr = user.User(un)

                    self.GetParent().GetParent().GetParent().key = sec.make_key(usr.salt, str(ps))
                    usr.control = sec.encrypt_data("jinxx", self.GetParent().GetParent().GetParent().key)
                    fio.create_user_file(usr)
                    self.GetParent().GetParent().GetParent().OnUserEnter(usr, self.GetParent().GetParent().GetParent().key)
                    self.tbun.SetValue("")
                    self.tbps.SetValue("")
                    self.GetParent().RefreshUserList()
                else:
                    wx.MessageBox('User already exists. Please enter another username.', 'Error', wx.OK)

            else:
                wx.MessageBox('Password must be at least 10 characters.', 'Error', wx.OK)
        else:
            wx.MessageBox('Please enter a username and password.', 'Error', wx.OK)



class N1PageExit(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent=parent)
        btnExit = wx.Button(parent=self, label="Exit", pos=(20, 40))
        btnExit.Bind(event=wx.EVT_BUTTON, handler=parent.GetParent().GetParent().OnClose)


class lpmN1(wx.Notebook):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.page_users = N1PageUsers(self)
        self.page_new_user = N1PageNewUser(self)
        self.page_exit = N1PageExit(self)
        self.AddPage(self.page_users, "Users")
        self.AddPage(self.page_new_user, "New User")
        self.AddPage(self.page_exit, "Exit")

    def RefreshUserList(self):
        self.page_users.RefreshList()


class N2PageUser(wx.Panel):

    def __init__(self, parent, user):
        super().__init__(parent=parent)
        wx.StaticText(self, label="Username:", pos=(20, 40))
        wx.StaticText(self, label="%s" % user.name, pos=(20, 60))
        c = len(user.secrets)
        wx.StaticText(self, label="Number of secrets:", pos=(20, 100))
        wx.StaticText(self, label="%d" % c, pos=(20, 120))
        if c == 0:
            wx.StaticText(self, label="Try adding a secret", pos=(20, 160))


class N2PageSecretList(wx.Panel):
    def __init__(self, parent, user):
        super().__init__(parent=parent)
        self.usr = user
        secrets = fio.get_available_secret_list(self.usr.name)
        self.lb = wx.ListBox(parent=self, pos=(20, 60))
        btn = wx.Button(parent=self, label="Copy To Clipboard", pos=(200, 60))
        btn.Bind(event=wx.EVT_BUTTON, handler=self.OnCopyToClipBoard)
        if len(secrets) == 0:
            txt = wx.StaticText(self, label="Sorry, no secrets were found. Please create a secret first.", pos=(20, 20))
        else:
            txt = wx.StaticText(self, label="Select a secret to copy to clipboard:", pos=(20, 20))
            self.RefreshList()

    def RefreshList(self):
        secrets = fio.get_available_secret_list(self.usr.name)
        secretscut = []
        for sec in secrets:
            se = sec.split(".txt")
            secretscut.append(se[0])
        self.lb.Clear()
        for s in secretscut:
            self.lb.Append(s)


    def OnCopyToClipBoard(self, event):
        res = self.lb.GetSelection()
        if res == wx.NOT_FOUND:
            wx.MessageBox('Please select an item.', 'Error', wx.OK)
        else:
            info = self.lb.GetString(res)
            secret = fio.get_secret(self.usr.name, info)
            ps = sec.decrypt_data(secret.data_en, self.GetParent().GetParent().GetParent().key)
            fio.copy2clip(ps)


class N2PageNewSecret(wx.Panel):
    tbin = None
    tbdt = None
    def __init__(self, parent, user):
        self.user = user
        super().__init__(parent=parent)
        wx.StaticText(self, label="Tag or some sort of information that will help you identify\n"
                                          " the data. This data will not be encrypted!\n"
                                          "Tag:", pos=(20, 10))
        self.tbin = wx.TextCtrl(self, pos=(20, 60))
        wx.StaticText(self, label="The data that will be encrypted(password, on any other string:", pos=(20, 100))
        self.tbdt = wx.TextCtrl(self, pos=(20, 120), style=wx.TE_PASSWORD)
        button = wx.Button(parent=self, label="Create Secret", pos=(20, 160))
        button.Bind(event=wx.EVT_BUTTON, handler=self.CreateSecret)


    def CreateSecret(self, event):
        info = self.tbin.GetValue()
        data = self.tbdt.GetValue()

        if info != "" and data != "":
            data_en = sec.encrypt_data(str(data), self.GetParent().GetParent().GetParent().key)
            se = isec.ISecretObject(str(info), data_en)
            fio.add_secret(self.user, se)
            self.tbin.SetValue("")
            self.tbdt.SetValue("")
            self.GetParent().RefreshSecretList()
            wx.MessageBox('Secret created.', 'Info', wx.OK)

        else:
            wx.MessageBox('Please fill in both fields!', 'Error', wx.OK)


class N2PageExit(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent=parent)
        btnExitAll = wx.Button(parent=self, label="Exit App", pos=(20, 40))
        btnExitAll.Bind(event=wx.EVT_BUTTON, handler=parent.GetParent().GetParent().OnClose)

        btnExit = wx.Button(parent=self, label="Exit User", pos=(20, 80))
        btnExit.Bind(event=wx.EVT_BUTTON, handler=parent.GetParent().GetParent().OnUserExit)


class lpmN2(wx.Notebook):
    def __init__(self, parent, user, key):
        super().__init__(parent=parent)
        self.page_user = N2PageUser(self, user)
        self.page_secret_list = N2PageSecretList(self, user)
        self.page_new_secret = N2PageNewSecret(self, user)
        self.page_exit = N2PageExit(self)
        self.AddPage(self.page_user, "User")
        self.AddPage(self.page_secret_list, "Secret List")
        self.AddPage(self.page_new_secret, "New Secret")
        self.AddPage(self.page_exit, "Exit")


    def RefreshSecretList(self):
        self.page_secret_list.RefreshList()


class lpmFirstPanel(wx.Panel):
    def __init__(self, par):
        super().__init__(parent=par)
        self.SetBackgroundColour(wx.GREEN)
        self.nb1 = lpmN1(self)


class lpmUserPanel(wx.Panel):
    def __init__(self, par, user, key):
        super().__init__(parent=par)
        self.SetBackgroundColour(wx.YELLOW)
        self.nb2 = lpmN2(self, user, key)


class lpmMainFrame(wx.Frame):

    def __init__(self, par, tit, pos):
        super().__init__(parent=par, title=tit, pos=pos)
        self.key = None
        self.user_panel = None

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.first_panel = lpmFirstPanel(self)
        self.sizer.Add(self.first_panel.nb1, 1, wx.EXPAND)
        self.first_panel.SetSizer(self.sizer)


    def OnUserEnter(self, user, key):
        if self.first_panel.IsShown():
            self.sizer1 = wx.BoxSizer(wx.HORIZONTAL)
            self.user_panel = lpmUserPanel(self, user, key)
            self.sizer1.Add(self.user_panel.nb2, 1, wx.EXPAND)
            self.user_panel.SetSizer(self.sizer1)
            self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
            self.sizer2.Add(self.user_panel, 1, wx.EXPAND)
            self.SetSizer(self.sizer2)
            self.first_panel.Hide()

            self.Layout()
    def OnUserExit(self, event):
        if self.user_panel.IsShown():
            self.user_panel.Hide()
            self.first_panel.Show()

    def OnClose(self, event):
        self.Close()


class lpmApp(wx.App):
    def __init__(self):
        super().__init__(clearSigInt=True)
        self.frame = lpmMainFrame(None, "MainWindow", pos=(0, 400))
        self.frame.Show()



from PySide6.QtCore import QObject, Property, Signal

class UserProfileStore(QObject):
    usernameChanged = Signal()
    passwordChanged = Signal()
    repeatPasswordChanged = Signal()
    hostnameChanged = Signal()
    autoLoginEnabledChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._username = ""
        self._password = ""
        self._repeat_password = ""
        self._hostname = ""
        self._autoLoginEnabled = False

    @Property(str, notify=usernameChanged)
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        if self._username != value:
            self._username = value
            self.usernameChanged.emit()
    
    @Property(str, notify=passwordChanged)
    def password(self):
        return self._password
    
    @password.setter
    def password(self, value):
        if self._password != value:
            self._password = value
            self.passwordChanged.emit()
    
    @Property(str, notify=repeatPasswordChanged)
    def repeatPassword(self):
        return self._repeat_password
    
    @repeatPassword.setter
    def repeatPassword(self, value):
        if self._repeat_password != value:
            self._repeat_password = value
            self.repeatPasswordChanged.emit()

    @Property(str, notify=hostnameChanged)
    def hostname(self):
        return self._hostname

    @hostname.setter
    def hostname(self, value):
        if self._hostname != value:
            self._hostname = value
            self.hostnameChanged.emit()

    @Property(bool, notify=autoLoginEnabledChanged)
    def automaticLogin(self):
        return self._autoLoginEnabled
    
    @automaticLogin.setter
    def automaticLogin(self, value):
        if self._autoLoginEnabled != value:
            self._autoLoginEnabled = value
            self.autoLoginEnabledChanged.emit()
    
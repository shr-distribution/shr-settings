import elementary, module, os, dbus

# Locale support
import gettext

try:
    cat = gettext.Catalog("shr-settings")
    _ = cat.gettext
except IOError:
    _ = lambda x: x


def getDbusObject (bus, busname , objectpath , interface):
        dbusObject = bus.get_object(busname, objectpath)
        return dbus.Interface(dbusObject, dbus_interface=interface)


class WifiManageBox(elementary.Box):
    """
    Class for Wifi Manager Button
    """

    def doNothing(self, obj, event, *args, **kargs):
        print "Nothing Done"

    def update(self):
        """
        """
        if self.dbusObj.GetPower():
            self.button.label_set(_("WiFi Manager"))
            self.button.clicked = self.buttonClicked
        else:
            self.button.label_set(_("WiFi Manager")+" (Off)")
            self.button.clicked = self.doNothing

    def buttonClicked(self, obj, event, *args, **kargs):
        """
        Trigger running the Wifi manager 'wifiman.py'

        !!!THIS IS ONLY FOR TESTING!!!

        Maybe in the future this will do something; currently it's GNDN.
        Must be adapted to your personal settings
        """
        print "Running wifiman.py"
        os.system("/home/root/Programs/wifiman.py")

    def __init__(self, win, dbusObj):
        """
        initialize the box and load objects
        Update the toggles to match current system settings
        """

        super(WifiManageBox, self).__init__(win)
        self.window = win
        self.dbusObj = dbusObj

        self.button = elementary.Button(self.window)
        self.button.size_hint_align_set(-1.0, 0.0)
        self.button.show()

        self.pack_start(self.button)
        self.size_hint_align_set(-1.0, 0.0)

        self.update()
        self.show()


class WifiToggleBox(elementary.Box):
    """
    Class for Wifi Connection power toggle
    """

    def update(self):
        """
        Set the toggle to the wifi power state
        """
        self.state = self.dbusObj.GetPower()
        self.toggle.state_set(self.state)

    def toggleChanged(self, obj, event, *args, **kargs):
        """
        Toggle the resource to opposite the toggle changed-to state
        Update the toggles to match current system settings
        """
        self.dbusObj.SetPower(obj.state_get())
        self.update()

    def __init__(self, win, dbusObj):
        """
        initialize the box and load objects
        Update the toggles to match current system settings
        """

        super(WifiToggleBox, self).__init__(win)
        self.window = win
        self.dbusObj = dbusObj
        self.state = None

        self.toggle = elementary.Toggle(self.window)
        self.toggle.label_set(_("WiFi radio:"))
        self.toggle.states_labels_set(_("On"),_("Off"))
        self.toggle.changed = self.toggleChanged
        self.toggle.size_hint_align_set(-1.0, 0.0)
        self.toggle.show()

        self.pack_start(self.toggle)
        self.size_hint_align_set(-1.0, 0.0)

        self.update()
        self.show()


class Wifi(module.AbstractModule):
    name = _("WiFi settings")

    def error(self):
        label = elementary.Label(self.window)
        label.label_set(_("Couldn't connect to FSO"))
        label.show()
        self.main.pack_start(label)

    def isEnabled(self):
        sysCmd = "cat /proc/cpuinfo | grep Hardware |  awk '{ print $3 }'"
        if os.popen(sysCmd).read()=="GTA01\n":
            return False
        else:
            return True

    def wifiManageCheck(self):
        if self.wifiToggle.state:
            try:
                self.wifiManage.update()
            except:
                self.wifiManage = WifiManageBox(self.window, self.dbusObj)
                self.main.pack_end(self.wifiManage)
                self.wifiManage.update()
        else:
            try:
                self.wifiManage.delete()
                del self.wifiManage
            except:
                pass

    def update(self, *args, **kargs):
        """
        """
        self.wifiToggle.update()
##        self.wifiManageCheck()

    def stopUpdate(self):
        self.signal.remove()

    def createView(self):
        self.main = elementary.Box(self.window)

        try:
            if self.isEnabled():
                # connect to dbus
                self.dbusObj = getDbusObject (self.dbus,
                    "org.freesmartphone.odeviced",
                    "/org/freesmartphone/Device/PowerControl/WiFi",
                    "org.freesmartphone.Device.PowerControl")

                # connect to dbus signals
                self.signal = self.dbusObj.connect_to_signal("Power", self.update)

                # create/pack toggle box
                self.wifiToggle = WifiToggleBox(self.window, self.dbusObj)
                self.main.pack_start(self.wifiToggle)

                self.update()
            else:
                label = elementary.Label(self.window)
                label.label_set("Wifi not available\non GTA01 Hardware")
                label.show()
                self.main.pack_start(label)

        except dbus.exceptions.DBusException, e:
            self.error()

        return self.main

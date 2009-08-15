import dircache
import module, elementary, os
from ecore import idler_add
from functools import partial

# Locale support
import gettext

try:
    cat = gettext.Catalog("shr-settings")
    _ = cat.gettext
except IOError:
    _ = lambda x: x


class ButtonServer( elementary.Button ):
    def set_osCmd( self, cmd ):
        self.osCmd = cmd

    def get_osCmd( self ):
        return self.osCmd

class Services(module.AbstractModule):
    name = _("Services settings")

    def reloadbtClick(self, obj, event, *args, **kargs):
        self.winser.hide()
        self.winser.delete()
        print "Services reloadbtClick [info]"
        self.sssbtClick( obj, event)

    def destroyInfo(self, obj, event, *args, **kargs):
        self.winser.hide()
        self.winser.delete()

    def destroyDebug(self, obj, event, *args, **kargs):
        self.windeb.hide()
        self.windeb.delete()

    def hover_hide(self, obj, event, *args, **kargs):
        self.ser_box.delete()
        self.ser_hover.delete()

    def startbtClick(self, obj, event, *args, **kargs):
        """ Callback when start/stop/reload has been pressed """
        # delete the hover with Start/stop buttons
        self.ser_box.delete()
        self.ser_hover.delete()
        self.startDebugWin( obj.get_osCmd() )

    def debugIdler(self, dia, box1, cmd):
        c = os.popen( cmd, "r" )
        while 1:
            line = c.readline().replace("\n","")
            if not line:
                break  
            print "line ["+line+"]"
            lb = elementary.Label(self.windeb)
            lb.label_set(line)
            lb.size_hint_align_set(-1.0, 0.0)
            box1.pack_end(lb)
            lb.show()
        dia.delete()
        return False

    def startDebugWin(self, cmd):
        print "Services startDebugWin [info]"
        self.windeb = elementary.Window("servicesDebug", elementary.ELM_WIN_BASIC)
        self.windeb.title_set(_("Service output"))
        self.windeb.autodel_set(True)

        self.bgdeb = elementary.Background(self.windeb)
        self.windeb.resize_object_add(self.bgdeb)
        self.bgdeb.size_hint_weight_set(1.0, 1.0)
        self.bgdeb.show()

        box0 = elementary.Box(self.windeb)
        box0.size_hint_weight_set(1.0, 1.0)
        self.windeb.resize_object_add(box0)
        box0.show()

        fr = elementary.Frame(self.windeb)
        fr.label_set(_("Service output"))
        fr.size_hint_align_set(-1.0, 0.0)
        box0.pack_end(fr)
        fr.show()

        sc = elementary.Scroller(self.windeb)
        sc.size_hint_weight_set(1.0, 1.0)
        sc.size_hint_align_set(-1.0, -1.0)
        box0.pack_end(sc)
        sc.show()

        cancelbt = elementary.Button(self.windeb)
        cancelbt.clicked = self.destroyDebug
        cancelbt.label_set(_("Close"))
        cancelbt.size_hint_align_set(-1.0, 0.0)
        cancelbt.show()
        box0.pack_end(cancelbt)

        box1 = elementary.Box(self.windeb)
        box1.size_hint_weight_set(1.0, -1.0)
        sc.content_set(box1)
        box1.show()
        
        self.windeb.show()

        dia = elementary.InnerWindow(self.windeb)
        dia.show()
        self.windeb.resize_object_add(dia)
        diala = elementary.Label(dia)
        diala.label_set(_('Executing...'))
        diala.show()
        dia.content_set(diala)
        dia.style_set('minimal')
        dia.activate()
        idler_add(partial(self.debugIdler, dia, box1, cmd))

    def sssbtClick(self, obj, event, *args, **kargs):
        print "Services sssbtClick [info]"
        self.makeWindowOrList()

    def chk_if_needToByDisplay(self, servicesList, name):
        for i in servicesList:
            if i == name:
                if name.pos('.sh')==2:
                    return 1
        return 0


    def clicked_serviceBox(self, win, event, *args, **kargs):
        service = win.name_get()

        self.ser_hover = elementary.Hover(self.win)
        self.ser_hover.size_hint_align_set(-1.0, -1.0)
        self.ser_hover.size_hint_weight_set(1.0, 1.0)
#        self.ser_hover.style_set("hoversel_vertical")
        self.ser_hover.show()
        self.ser_hover.clicked = self.hover_hide
#        self.window.resize_object_add(self.ser_hover)

        ser_box = elementary.Box(self.ser_hover)       
        ser_box.show()
#        ser_box.size_hint_align_set(-1.0, -1.0)
        ser_box.size_hint_weight_set(1.0, 1.0)
        self.ser_hover.content_set("swallow?!", ser_box)
        self.ser_hover.parent_set(ser_box)
        self.ser_hover.target_set(win)

        startbt = ButtonServer(self.win)
        startbt.set_osCmd("/etc/init.d/" + service + " start")
        startbt.clicked = self.startbtClick
        startbt.label_set(_("start") )
#        startbt.size_hint_align_set(-1.0, 0.0)
#        startbt.size_hint_weight_set(1.0, 1.0)
        startbt.show()
        ser_box.pack_start(startbt)

        restartbt = ButtonServer(self.win)
        restartbt.set_osCmd("/etc/init.d/"+ service +" restart")
        restartbt.clicked = self.startbtClick
        restartbt.label_set(_("restart"))
#        restartbt.size_hint_align_set(-1.0, 0.0)
        restartbt.show()
        ser_box.pack_end(restartbt)

        stopbt = ButtonServer(self.win)
        stopbt.set_osCmd("/etc/init.d/"+ service +" stop")
        stopbt.clicked = self.startbtClick
        stopbt.label_set(_("stop"))
#        stopbt.size_hint_align_set(-1.0, 0.0)
        stopbt.show()
        ser_box.pack_end(stopbt)
        self.ser_box = ser_box
        self.win.resize_object_add(self.ser_box)


    def createView(self):
        """ main entry to the module that creates and returns the view """
        btn = elementary.Button(self.window)
        btn.label_set(_('Services'))
        btn.clicked = self.makeWindow
        return btn

    def makeWindow(self, *args, **kwargs):
        self.win = elementary.Window('settings-services', elementary.ELM_WIN_BASIC)
        win = self.win
        bg = elementary.Background(win)
        win.resize_object_add(bg)
        win.title_set(_('Services'))
        win.autodel_set(True)
        bg.show()
        box = elementary.Box(win)
        win.resize_object_add(box)
        box.show()
        scroller = elementary.Scroller(win)
        scroller.bounce_set(0,0)
        frame = elementary.Frame(win)
        frame.label_set(self.name)
        frame.size_hint_align_set(-1.0, -1.0)
        frame.size_hint_weight_set(1.0, 0.0)
        scroller.content_set(frame)

        scroller.size_hint_align_set(-1.0, -1.0)
        scroller.size_hint_weight_set(1.0, 1.0)

        box.pack_start(scroller)

        scroller.show()

        quitbt = elementary.Button(win)
        quitbt.clicked = partial(self.windowClose, win)
        quitbt.label_set(_("Quit"))
        quitbt.size_hint_align_set(-1.0, 0.0)
        ic = elementary.Icon(quitbt)
        ic.file_set( "/usr/share/pixmaps/shr-settings/icon_quit.png" )
        ic.scale_set(1,1)
        ic.smooth_set(1)
        quitbt.icon_set(ic)
        quitbt.show()
        box.pack_end(quitbt)


        box0 = elementary.Box(win)

        label = elementary.Label(box0)
        label.label_set(_("Please wait..."))
        box0.pack_start(label)
        label.show()

        idler_add(partial(self.windowIdler, label, box0))

        box0.show()
        frame.content_set(box0)
        frame.show()
        win.show()

    def windowClose(self, win, *args, **kwargs):
        win.delete()

    def windowIdler(self, label, box0, *args, **kwargs):
        label.delete()

        dontshow = ["rc", "rcS", "reboot", "halt", "umountfs", "sendsigs", "rmnologin", "functions", "usb-gadget"]
 
        servicesList = dircache.listdir("/etc/init.d/")
        servicesList.sort()
        for i in servicesList:
            if ((len(i.split(".sh"))==1) and (not(i in dontshow))):
                boxSSS = elementary.Button(box0)
                boxSSS.label_set(i)
                boxSSS.name = i
                #boxSSS.horizontal_set(True)
                boxSSS.size_hint_align_set(-1.0, -1.0)
                boxSSS.size_hint_weight_set(1.0, 1.0)
                boxSSS.clicked = self.clicked_serviceBox
                boxSSS.show()
                box0.pack_end(boxSSS)
             
        return False

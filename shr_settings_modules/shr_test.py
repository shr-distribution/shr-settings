import elementary, module

# Locale support
import gettext

try:
    cat = gettext.Catalog("shr-settings")
    _ = cat.gettext
except IOError:
    _ = lambda x: x


class Test(module.AbstractModule):
    def totest(self, obj, event, *args, **kargs):
        print event
        print "it works!"
        obj.label_set("lol")
    def getName(self, ):
        print "name"
        return "Test"
    def isEnabled(self):
        return True
    def createView(self):

	box = elementary.Box(self.window)
	label = elementary.Label(self.window)
	label.label_set(_("test"))
	box.pack_end(label)
	label.show()

        bt = elementary.Button(self.window)
        bt.clicked = self.totest
        bt.label_set(_("Just for fun"))
        bt.size_hint_align_set(-1.0, 0.0)
        bt.show()

	bb = elementary.Bubble(self.window)

	bb.label_set("label_test")
	bb.info_set("info_test")
	bb.content_set(box)
#	bb.corner_set("corner_test")
	
	bb.show()
	box.pack_end(bt)	

	return bb

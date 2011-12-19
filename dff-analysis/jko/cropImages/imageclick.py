import gtk
import pygtk
import os

class ImageClick:

   
    def __init__(self,filename='default.tiff'):
        ''' Creates the window and listener using gtk.
        '''

        self.filename = filename
        
        self.x = None
        self.y = None
        self.x2 = None
        self.y2 = None

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        self.window.connect("destroy", self.destroy)
        self.window.connect("event", self.button_pressed)
        self.window.add_events(gtk.gdk.ALL_EVENTS_MASK)
        self.window.set_resizable(0)
        
        self.image = gtk.Image()
        self.image.set_from_file(self.filename)

        self.window.add(self.image)

        self.image.show()
        self.window.show()
        
        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        #self.window.set_position(0)
        
        #self.window.set_position((0,0))
        
    def destroy(self, widget, data=None):
        ''' Quits gtk
        '''
        self.window.destroy()
        self.image.destroy()
        gtk.main_quit()

    def button_pressed(self, widget, event):
        ''' Event handler assigned to listener. Reads and sets coordinates.
        '''
        
        if event.type == gtk.gdk.BUTTON_PRESS:
            coords = event.get_coords()
            if self.x == None:
                self.x = int(round(coords[0]))
                self.y = int(round(coords[1]))
                ###################################
                print self.filename, self.x, self.y
                self.destroy(self)
                ####################################
            else:
                self.x2 = int(round(coords[0]))
                self.y2 = int(round(coords[1]))
                ##########################################3   
                # self.printCommand()
                # self.destroy(self)
                ##########################################
                
    def printCommand(self):
        
        w = self.x2 - self.x
        h = self.y2 - self.y
        x0 = self.x
        y0 = self.y
        cmd = "mkdir -p cropped;"
        cmd += "for file in *.tiff; do "
        cmd += "convert -depth 8 -crop "
        cmd += str(w) + "x" + str(h)
        cmd += "+" + str(x0) + "+" + str(y0)
        cmd += " $file cropped/$file; done" 
        
        print cmd

    def main(self):
        ''' Starts gtk.main()
        '''
        gtk.main()
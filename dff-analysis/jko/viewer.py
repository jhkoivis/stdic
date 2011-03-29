

import wx

class JFrame(wx.Frame):
    
    def __init__(self):
        wx.Frame.__init__(self, None, -1)
        
        #self.splitter = wx.SplitterWindow(self)
        #self.tWindow = TopWindow(self.splitter)
        self.bWindow = BottomWindow(self) #self.splitter)
        #self.splitter.SplitHorizontally(self.tWindow, self.bWindow)
        
class BottomWindow(wx.Window):
    
    def __init__(self, parent):
        wx.Window.__init__(self,parent, -1)
        
        #self.panel = wx.Panel(self, -1 )
        self.text = wx.TextCtrl(self, 
                                -1, 
                                pos  = (10, 1), 
                                size = (200, 20))
        self.Update()
        self.lastId = 0
        self.idList = {'0': {'x':0, 'y':0, 'height':0, 'width':0}}
        #self.center = wxTextCtrl ( self.panel, -1, style = wxTE_CENTRE )
        
    def getPos(self,id):
        
        if self.posList.has_key(id):
            return self.posList[id]
        else:
            newPos = {}
            
            self.posList[id] = self.lastId + 1
            
        
    

class DictTextCtrl(wx.TextCtrl):
    
    def __init__(self, parent, id):
        
        self.id = id
        self.pos = parent.getPos(id)
        self.size = parent.getSize(id)
        wx.TextControl.__init__(self, -1)


class TopWindow(wx.Window):
    
    def __init__(self, parent): 
        wx.Window.__init__(self,parent, -1) 




if __name__ == "__main__":
    
    app = wx.App()
    frame = JFrame() 
    frame.Show()
    app.MainLoop()
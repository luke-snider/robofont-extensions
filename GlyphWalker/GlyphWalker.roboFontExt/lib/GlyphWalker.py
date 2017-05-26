#coding=utf-8
'''
Lukas Schneider - Revolver Type Foundry - www.revolvertype.com
GlyphWalker lets you walk trough a glyph simultaneously back and forth in all open fonts.

Reorder open fonts according to family, width, weight is based on a script by Dan Milne.
'''
from vanilla import *
from mojo.UI import *
from mojo.extensions import getExtensionDefault, setExtensionDefault
from AppKit import *
from vanilla.dialogs import message

extensionID = "GlyphWalker"

class GlyphWalker():

    def __init__(self):
         
        self.w = FloatingWindow((220, 70), '') 

        self.w.tabGlyphsButton = Button((5, 0, 105, 18), title="display settings", sizeStyle = "mini", callback=self.toggleOptions)
        self.scales = ["Fit window","Current Scale"]
        self.w.scalePopup = PopUpButton((120,0,-5,20), self.scales, sizeStyle = "mini")
        y = 15
        self.w.back = Button((5,y+5,52,25), "<", callback=self.walk, sizeStyle="regular")
        self.w.forth = Button((57,y+5,53,25), ">", callback=self.walk, sizeStyle="regular")
        self.w.scaleMinus = Button((120,y+5,47,25), "+", callback=self.scale, sizeStyle="regular")
        self.w.scalePlus = Button((167,y+5,47,25), "-", callback=self.scale, sizeStyle="regular")
        self.w.btnX = SquareButton((5,y+33,105,16), "open current (all)", callback=self.openAllFontsGlyphWindows, sizeStyle="mini")
        self.w.btnY = SquareButton((120,y+33,-5,16), "save all fonts", callback=self.saveAllFonts, sizeStyle="mini")
        y2 = -12
        self.popOver = Popover((120, 180), parentView=self.w, preferredEdge='right', behavior="applicationDefined")		
        self._popOverIsVisible = False
        self.popOver.fill = CheckBox((10,y2+15,100,20), "fill/stroke", sizeStyle = "small", callback=self.fill)
        self.popOver.blues = CheckBox((10,y2+30,100,20), "blues", sizeStyle = "small", callback=self.blues)
        self.popOver.points = CheckBox((10,y2+45,100,20), "points", sizeStyle = "small", callback=self.points)
        self.popOver.guides = CheckBox((10,y2+60,100,20), "guides", sizeStyle = "small", callback=self.guides)
        self.popOver.anchors = CheckBox((10,y2+75,100,20), "anchors", sizeStyle = "small", callback=self.anchors)
        self.popOver.metrics = CheckBox((10,y2+90,100,20), "metrics", sizeStyle = "small", callback=self.metrics)
        self.popOver.pointCoordinates = CheckBox((10,y2+105,100,20), "point coord.", sizeStyle = "small", callback=self.pointCoordinates)
        self.popOver.contourIndexes = CheckBox((10,y2+120,100,20), "contour index", sizeStyle = "small", callback=self.contourIndex)
        self.popOver.outlineErrors = CheckBox((10,y2+135,100,20), "outline errors", sizeStyle = "small", callback=self.outlineErrors)
        self.popOver.compIndex = CheckBox((10,y2+150,100,20), "comp. index", sizeStyle = "small", callback=self.compIndex)
        self.popOver.layerTransparency = CheckBox((10,y2+165,100,20), "layer transp.", sizeStyle = "small", callback=self.layerTransparency)

        self.popOver.fill.set(getExtensionDefault("%s.%s" %(extensionID, "fill/stroke"), True))
        self.popOver.blues.set(getExtensionDefault("%s.%s" %(extensionID, "blues"), False))
        self.popOver.points.set(getExtensionDefault("%s.%s" %(extensionID, "points"), False))
        self.popOver.guides.set(getExtensionDefault("%s.%s" %(extensionID, "guides"), False))
        self.popOver.anchors.set(getExtensionDefault("%s.%s" %(extensionID, "anchors"), False))
        self.popOver.metrics.set(getExtensionDefault("%s.%s" %(extensionID, "metrics"), False))
        self.popOver.pointCoordinates.set(getExtensionDefault("%s.%s" %(extensionID, "pointCoordinates"), False))
        self.popOver.contourIndexes.set(getExtensionDefault("%s.%s" %(extensionID, "contourIndexes"), False))
        self.popOver.outlineErrors.set(getExtensionDefault("%s.%s" %(extensionID, "outlineErrors"), False))
        self.popOver.compIndex.set(getExtensionDefault("%s.%s" %(extensionID, "compIndex"), False))

        self.setDisplaySettings()
        
        self.ordered_open = []
        self.w.open()

    def windowCloseCallback(self, sender):
        setExtensionDefault("%s.%s" % (extensionID, "fill/stroke"), self.popOver.fill.get())
        setExtensionDefault("%s.%s" % (extensionID, "blues"), self.popOver.blues.get())
        setExtensionDefault("%s.%s" % (extensionID, "points"), self.popOver.points.get())
        setExtensionDefault("%s.%s" % (extensionID, "guides"), self.popOver.guides.get())
        setExtensionDefault("%s.%s" % (extensionID, "anchors"), self.popOver.anchors.get())
        setExtensionDefault("%s.%s" % (extensionID, "metrics"), self.popOver.metrics.get())
        setExtensionDefault("%s.%s" % (extensionID, "pointCoordinates"), self.popOver.pointCoordinates.get())
        setExtensionDefault("%s.%s" % (extensionID, "contourIndexes"), self.popOver.contourIndexes.get())
        setExtensionDefault("%s.%s" % (extensionID, "outlineErrors"), self.popOver.outlineErrors.get())
        setExtensionDefault("%s.%s" % (extensionID, "compIndex"), self.popOver.compIndex.get())
        UpdateCurrentGlyphView()
        super(GlyphWalker, self).windowCloseCallback(sender)

    def setDisplaySettings(self):
        fill = getExtensionDefault("%s.%s" %(extensionID, "fill/stroke"), True)
        blues = getExtensionDefault("%s.%s" %(extensionID, "blues"), False)
        points = getExtensionDefault("%s.%s" %(extensionID, "points"), False)
        guides = getExtensionDefault("%s.%s" %(extensionID, "guides"), False)
        anchors = getExtensionDefault("%s.%s" %(extensionID, "anchors"), False)
        metrics = getExtensionDefault("%s.%s" %(extensionID, "metrics"), False)
        pointCoordinates = getExtensionDefault("%s.%s" %(extensionID, "pointCoordinates"), False)
        contourIndexes = getExtensionDefault("%s.%s" %(extensionID, "contourIndexes"), False)
        outlineErrors = getExtensionDefault("%s.%s" %(extensionID, "outlineErrors"), False)
        compIndex = getExtensionDefault("%s.%s" %(extensionID, "compIndex"), False)
        extensionDefaults = {"Fill": fill, "Blues":blues, "Points":points, "Guides":guides, "Anchors":anchors, "Metrics": metrics, "Point Coordinates":pointCoordinates, "Contour Indexes": contourIndexes, "Outline Errors": outlineErrors, "Components Indexes": compIndex}
        setGlyphViewDisplaySettings(extensionDefaults)


    def toggleOptions(self, sender):
		if self._popOverIsVisible:
			self.popOver.close()
			self._popOverIsVisible = False
			sender.setTitle("display settings")
		else:
			self.popOver.open(parentView=sender)
			self._popOverIsVisible = True
			sender.setTitle("close settings")
			sender.enable(True)



    def orderAllOpenFonts(self):

        allopen = AllFonts()
        ## Reorder open fonts according to family, width, weight - taken from a script by Dan Milne.
        unordered = []
        for i in range(len(allopen)):
            family = allopen[i].info.familyName
            if allopen[i].info.italicAngle is not None:
                slope = abs(allopen[i].info.italicAngle)
            else:
                slope = 0
        
            weight = allopen[i].info.openTypeOS2WeightClass
            if weight == None:
                print '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'
                print 'OpenType weight class is not defined in ' + str(family) + '. Order may be incorrect.'
                print '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'

            width = allopen[i].info.openTypeOS2WidthClass
            if width == None:
                print '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'
                print 'OpenType width class is not defined in ' + str(family) + '. Order may be incorrect.'
                print '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'
    
            unordered.append((i,family,slope,width,weight))

        ordered_weight = sorted(unordered, key=lambda tup: tup[4]) # reverse sort on weight
        ordered_width = sorted(ordered_weight, key=lambda tup: tup[3]) # reverse sort on width
        ordered_slope = sorted(ordered_width, key=lambda tup: tup[2]) # reverse sort on slope
        ordered_family = sorted(ordered_slope, key=lambda tup: tup[1]) # reverse sort on weight

        self.ordered_open = []
        #original: for item in ordered_family
        for item in reversed(ordered_family):
            self.ordered_open.append(allopen[item[0]])

            
    def openAllFontsGlyphWindows(self, sender):
        if CurrentGlyphWindow() == None:
            if CurrentFont() == None:
                message("Open font(s) first!")
            else:
                message("Open a glyph window first!")
        else:
            self.orderAllOpenFonts()
            # allfonts = AllFonts()
            if CurrentGlyph() !=None:
                glyphName = CurrentGlyph().name
                for font in self.ordered_open: #allfonts:
                    if font.has_key(glyphName):
                        OpenGlyphWindow(font[glyphName])

                self.tile()

                for glyphwin in AllGlyphWindows():
                    try:
                        currentScale = glyphwin.getGlyphViewScale()
                        glyphwin.setGlyphViewScale(currentScale-0.1)
                        glyphwin.centerGlyphInView()
                    except TypeError:
                        pass  

    def scale(self, sender):
        title = sender.getTitle()
        if title == "+":
            if CurrentGlyph() != None:
                for glyphwin in AllGlyphWindows():
                    try:
                        currentScale = glyphwin.getGlyphViewScale()
                        glyphwin.setGlyphViewScale(currentScale+0.1)
                        glyphwin.centerGlyphInView()
                    except TypeError:
                        pass            
        if title == "-":
            if CurrentGlyph() != None:
                for glyphwin in AllGlyphWindows():
                    try:
                        currentScale = glyphwin.getGlyphViewScale()
                        glyphwin.setGlyphViewScale(currentScale-0.1)
                        glyphwin.centerGlyphInView()
                    except TypeError:
                        pass  

    def walk(self, sender):
        title = sender.getTitle()        
        font = CurrentFont()
        if CurrentGlyph() != None:
            glyphname = CurrentGlyph().name
            glyphOrder = font.glyphOrder
            if len(glyphOrder) != 0:
                for i, name in enumerate(glyphOrder):
                    if name == glyphname:
                        try:
                            theGlyphNameBefore = glyphOrder[i-1]
                            theGlyphNameAfter = glyphOrder[i+1]
                        except IndexError:
                            ### last glyph in order
                            theGlyphNameAfter = glyphOrder[0]
                            theGlyphNameBefore = glyphOrder[i-1]
                if title == "<":
                    theGlyphName = theGlyphNameBefore
                if title == ">":
                    theGlyphName = theGlyphNameAfter
            
                collectedScales = []
                ### first collecting all scales to determine which one is the smallest scale
                for glyphwin in reversed(AllGlyphWindows()):   
                    try:
                        glyphwin.setGlyphByName(theGlyphName)
                        glyph = glyphwin.getGlyph()
                        scale = self.getGlyphWidthHeight(glyphwin, glyph)
                        collectedScales.append(scale)              
                    except TypeError:
                        pass
                if collectedScales != None:
                    scale = max(collectedScales)
                else:
                    scale == 0.7
                if self.w.scalePopup.get() == 0:
                    scale = scale
                if self.w.scalePopup.get() == 1:
                    scale = CurrentGlyphWindow().getGlyphViewScale()
                ### print CurrentGlyphWindow().getGlyph().getParent().info.familyName
                ## then using the scale and applying it to all wins:
                for glyphwin in reversed(AllGlyphWindows()):   
                    try:
                        glyphwin.setGlyphByName(theGlyphName)
                        glyphwin.setGlyphViewScale(scale)
                        glyphwin.centerGlyphInView()                    
                    except TypeError:
                        pass


    def getGlyphWidthHeight(self, glyphwin, glyph):
        if glyph.bounds:
            left, bottom, right, top = glyph.bounds
        else:
            left = right = bottom = top = 0
        visibleHeight = glyphwin.getVisibleRect()[-1]
        newHeight = (top-bottom)+60
        scale = visibleHeight / newHeight
        ### print "fontandscale", glyph.getParent().info.familyName, scale
        return scale


    def tile(self):
        windows = [w for w in NSApp().orderedWindows() if w.isVisible()]
        screen = NSScreen.mainScreen()
        (x, y), (w, h) = screen.visibleFrame()
        altDown = NSEvent.modifierFlags() & NSAlternateKeyMask
        NSApp().arrangeInFront_(None)
        windowsToHide = []
        windowsToTile = []
        for window in windows:
            if hasattr(window, "windowName") and window.windowName() == "GlyphWindow":
                windowsToTile.append(window)
            else:
                windowsToHide.append(window)
                break

        tileInfo = {
                    1 : [[1]],
                    2 : [[],[1, 1]],
                    3 : [[],[1, 1, 1]],
                    4 : [[], [1, 1, 1, 1]],
                    5 : [[1, 1], [1, 1, 1]],
                    6 : [[1, 1, 1], [1, 1, 1]],
                    7 : [[1, 1, 1], [1, 1, 1, 1]],
                    8 : [[1, 1, 1, 1], [1, 1, 1, 1]],
                    9 : [[1, 1, 1, 1], [1, 1, 1, 1, 1]],
                    10 : [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1]],
                    11 : [[1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1]],
                    12 : [[1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]],
                    13 : [[1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]],
                    14 : [[1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1]],
                    15 : [[1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1]],
                    16 : [[1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1]],
                    17 : [[1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1]],
                    18 : [[1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1]],
                    19 : [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1]],
                    20 : [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
                    }

        if windowsToTile:
            arrangement = tileInfo[len(windowsToTile)]
            maxHeight = len(arrangement)
            diffx = x
            diffy = y
            c = 0
            for i in arrangement:
                maxWidth = len(i)        
                for j in i:
                    window = windows[c]
                    window.setFrame_display_animate_(NSMakeRect(diffx, diffy, w/float(maxWidth), h/float(maxHeight)), True, altDown)
                    c += 1
                    diffx += w/float(maxWidth)
                diffx = x
                diffy += h/float(maxHeight)
        for window in windowsToHide:
            window.miniaturize_(None)


    def saveAllFonts(self, sender):
        for f in AllFonts():    
            f.save(destDir=None)

###########################
### PREVIEW OPTIONS #######
###########################
    def compIndex(self, sender):
        if CurrentGlyph() != None:
            if sender.get() == 0:
                setGlyphViewDisplaySettings({'Component Indexes':False})
                setGlyphViewDisplaySettings({'Component Info':False})
            if sender.get() == 1:
                setGlyphViewDisplaySettings({'Component Indexes':True})
                setGlyphViewDisplaySettings({'Component Info':True})

    def outlineErrors(self, sender):
        if CurrentGlyph() != None:
            if sender.get() == 0:
                setGlyphViewDisplaySettings({'Outline Errors':False})
            if sender.get() == 1:
                setGlyphViewDisplaySettings({'Outline Errors':True})

    def points(self, sender):
        if CurrentGlyph() != None:
            if sender.get() == 0:
                setGlyphViewDisplaySettings({'On Curve Points':False})
                setGlyphViewDisplaySettings({'Off Curve Points':False})
            if sender.get() == 1:
                setGlyphViewDisplaySettings({'On Curve Points':True})
                setGlyphViewDisplaySettings({'Off Curve Points':True})

    def fill(self, sender):
        if CurrentGlyph() != None:
            if sender.get() == 0:
                setGlyphViewDisplaySettings({'Stroke':True})
                setGlyphViewDisplaySettings({'Fill':False})
            if sender.get() == 1:
                setGlyphViewDisplaySettings({'Stroke':False})
                setGlyphViewDisplaySettings({'Fill':True})

    def blues(self, sender):
        if CurrentGlyph() != None:
            if sender.get() == 0:
                setGlyphViewDisplaySettings({'Blues':False})
            if sender.get() == 1:
                setGlyphViewDisplaySettings({'Blues':True})

    def metrics(self, sender):
        if CurrentGlyph() != None:
            if sender.get() == 0:
                setGlyphViewDisplaySettings({'Metrics':False})
            if sender.get() == 1:
                setGlyphViewDisplaySettings({'Metrics':True})

    def pointCoordinates(self, sender):
        if CurrentGlyph() != None:
            if sender.get() == 0:
                setGlyphViewDisplaySettings({'Point Coordinates':False})
            if sender.get() == 1:
                setGlyphViewDisplaySettings({'Point Coordinates':True})

    def anchors(self, sender):
        if CurrentGlyph() != None:
            if sender.get() == 0:
                setGlyphViewDisplaySettings({'Anchors':False})
            if sender.get() == 1:
                setGlyphViewDisplaySettings({'Anchors':True})

    def guides(self, sender):
        if CurrentGlyph() != None:
            if sender.get() == 0:
                setGlyphViewDisplaySettings({'Guides':False})
            if sender.get() == 1:
                setGlyphViewDisplaySettings({'Guides':True})

    def contourIndex(self, sender):
        if CurrentGlyph() != None:
            if sender.get() == 0:
                setGlyphViewDisplaySettings({'Contour Indexes':False})
            if sender.get() == 1:
                setGlyphViewDisplaySettings({'Contour Indexes':True})

    def layerTransparency(self, sender):
        if AllFonts() != None:
            if sender.get() == 0:
                for f in AllFonts():
                    for layername in f.layerOrder:
                        f.setLayerDisplay(layername, 'Fill', 0)
                        f.setLayerDisplay(layername, 'Stroke', 0)
            if sender.get() == 1:
                for f in AllFonts():
                    for layername in f.layerOrder:
                        f.setLayerDisplay(layername, 'Fill', 100)
                        f.setLayerDisplay(layername, 'Stroke', 100)


GlyphWalker()
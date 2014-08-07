"""
Interpol Steps Preview V 3.1
Lukas Schneider, 2014
with a few lines of code of Frederik Berlaen's quick interpolate script.

"""

from mojo.UI import MultiLineView
from vanilla import *
###
import vanilla
from defconAppKit.windows.baseWindow import BaseWindowController
from defconAppKit.controls.glyphLineView import GlyphLineView
from mojo import events
from mojo.tools import IntersectGlyphWithLine
from lib.UI.stepper import EditIntStepper


class InterpolateStepView(BaseWindowController):

    def __init__(self):
        self.value = 150
        self.w = vanilla.Window((700, 210), "Interpol Steps Preview", minSize=(100, 200))

        
        self.w.infoOutput = TextBox((460,8,-70,20), "Open 2 Fonts + select a glyph.", alignment= "right", sizeStyle = "mini") 
        self.w.button = Button((-65, 2, 60, 20), "Options", sizeStyle = "small", callback=self.toggleOptions)       
        self.d = Drawer((125, 200), self.w, minSize=(125,100), maxSize=(125,200), preferredEdge='right', trailingOffset=15, leadingOffset=0)
        self.d.fontSize = TextBox((8, 5, 50, 10), "FONTSIZE", sizeStyle = "mini",)
        self.d.lineHeight = TextBox((62, 5, 100, 10), "LINEHEIGHT", sizeStyle = "mini",)
        self.d.button3 = SquareButton((10,20,25,18), "-", sizeStyle = "small", callback=self.ChangePointSizeMinus)
        self.d.button4 = SquareButton((35,20,25,18), "+", sizeStyle = "small", callback=self.ChangePointSizePlus)
        self.d.button5 = SquareButton((65,20,25,18), "-", sizeStyle = "small", callback=self.ChangeLineheightMinus)
        self.d.button6 = SquareButton((90,20,25,18), "+", sizeStyle = "small", callback=self.ChangeLineheightPlus)
        self.d.interpolStepsText = TextBox((55,50,100,20), "Interpol Steps", sizeStyle = "mini")
        self.d.extrapolStepsText = TextBox((55,75,100,20), "Extrapol Steps", sizeStyle = "mini")  
        self.d.interpolStepper = EditIntStepper((10, 45, 45, 22), 4, callback=self.glyphChanged, minValue=1, maxValue=30, sizeStyle='regular')
        self.d.extrapolStepper = EditIntStepper((10, 70, 45, 22), 1, callback=self.glyphChanged, minValue=0, maxValue=20, sizeStyle='regular') 
        self.d.checkBoxInfo = TextBox((10,98,100,20), "Display Options:", sizeStyle = "mini") 
        self.d.checkBoxMetrics = CheckBox((10,110,130,20), "Metrics", sizeStyle = "small", callback=self.Metrics) 
        self.d.checkBoxR2L = CheckBox((10,125,130,20), "Right to Left", sizeStyle = "small", callback=self.R2L) 
        self.d.checkBoxInverse = CheckBox((10,140,130,20), "Inverse", sizeStyle = "small", callback=self.Inverse)
        self.d.checkBoxStroke = CheckBox((10,155,130,20), "Stroke", sizeStyle = "small", callback=self.Stroke)
        self.w.glyphLineView = MultiLineView((0, 25, 0, 0))
        self.w.stemWidthOutputText = TextBox((10,8,500,20), "Beam Y-Pos:", sizeStyle = "mini") 
        self.w.stemWidthBeamX = EditText((70,3,30,19), "200", sizeStyle = "small", callback=self.stepsCallback)
        self.w.stemWidthOutput = TextBox((105,8,-205,13), "Measurements of the 1st stem will be displayed here.", sizeStyle = "mini")

        events.addObserver(self, "glyphChanged", "currentGlyphChanged")
        self.setUpBaseWindowBehavior()
        self.w.open()
        self.d.open()


        self.listOfValues = []
                
    def toggleOptions(self, sender):
        self.d.toggle()

    def stepsCallback(self, sender):
        if CurrentGlyph() == None:
            self.w.infoOutput.set("Select a glyph !")
            return
        else:
            self.glyphChanged(CurrentGlyph())
                        
    def windowCloseCallback(self, sender):
        events.removeObserver(self, "currentGlyphChanged")
        super(InterpolateStepView, self).windowCloseCallback(sender)

    def decomposeGlyph(self, glyph):
    	if glyph.components != None:
    		for c in glyph.components:
    			c.decompose()
    	return glyph

    def stemWidth(self, glyph):
    	try:
           val = int(self.w.stemWidthBeamX.get())
    	except ValueError:
           self.w.infoOutput.set("Pls enter a Number.") 
           return 
        BeamerPosition = int(self.w.stemWidthBeamX.get())
        result = IntersectGlyphWithLine(glyph, ((-10, BeamerPosition), (glyph.width+10, BeamerPosition)), canHaveComponent=True, addSideBearings=False)
        xValuesFromIntersection = [x[0] for x in result]
        xValuesSorted = sorted(xValuesFromIntersection)
        try:
            stemWidth = xValuesSorted[1] - xValuesSorted[0] 
            self.listOfValues.append(int(stemWidth))
        except IndexError:
            return



    def glyphChanged(self, info):
                font = CurrentFont()
                allfonts = AllFonts()
                if font is None:
                    self.w.infoOutput.set("Open 2 Fonts.")
                if len(allfonts) != 2:
                    self.w.infoOutput.set("You need 2 Fonts.")                    
                else:   
                    glyph = CurrentGlyph()

                    if glyph is None:
                        glyphs = []
                        self.w.infoOutput.set("Select a glyph.")
                    else:
                        self.w.infoOutput.set("")
                        glyphs = []
                        font1 = allfonts[0]
                        font2 = allfonts[1]
                        dummyInterpolFont1 = font1.copy()
                        dummyInterpolFont2 = font2.copy()
                        glyphName = glyph.name
                        if font1.has_key(glyphName):
                            InterpolGlyph1 = dummyInterpolFont1[glyphName]
                            self.decomposeGlyph(InterpolGlyph1)
                        else:
                            self.w.infoOutput.set("Exists only in 1 Master.")
                            return  
                        
                        if font2.has_key(glyphName):            
                            InterpolGlyph2 = dummyInterpolFont2[glyphName]
                            self.decomposeGlyph(InterpolGlyph2)
                
                            source1 = dummyInterpolFont1[glyphName]
                            source2 = dummyInterpolFont2[glyphName]
                
                            if not source1.isCompatible(source2, False):
                                self.w.infoOutput.set("Incompatible Glyphs")
                            else:  
                                try:
                                   val = int(self.d.interpolStepper.get())
                                   val = int(self.d.extrapolStepper.get())
                                except ValueError:
                                   self.w.infoOutput.set("Pls enter a Number.") 
                                   return 
                                interpolationSteps = int(self.d.interpolStepper.get())+1
                                extrapolateSteps = int(self.d.extrapolStepper.get())
                            
                                if interpolationSteps >= 0:    
                                    nameSteps = 0
                                    for i in range(-extrapolateSteps, interpolationSteps+extrapolateSteps + 1, 1):
                                        name = "interpolation.%03i" % nameSteps
                                        nameSteps += 1
                                        dest = dummyInterpolFont1.newGlyph(name)
                                        factor = i / float(interpolationSteps)                
                                        dest.interpolate(factor, source1, source2)
                                        self.stemWidth(dest)
                                        glyphs.append(dest)
                                    newList = []
                                    for key, item in enumerate(self.listOfValues): 
                                        count = key+1
                                        newList.append("%s:%s" % (str(count), str(item))) 
                                    self.w.stemWidthOutput.set(str(newList).strip('[\']').replace('\', \'','        '))
                                    self.listOfValues = []
                                else:
                                    self.w.infoOutput.set("Min. 1 Interpol. Step.")
                                    glyphs = []
                                    self.w.glyphLineView.set(glyphs)
                        else:
                            self.w.infoOutput.set("Exists only in 1 Master.")
                            
                    self.w.glyphLineView.set(glyphs)


    def ChangePointSizePlus(self, sender):
        self.w.glyphLineView.setPointSize(self.value+10)
        self.value = self.value +10
        
    def ChangePointSizeMinus(self, sender):
        if self.value < 10:
            self.value = 10
            self.w.glyphLineView.setPointSize(self.value-10)
            self.value = self.value -10
        else:
            self.w.glyphLineView.setPointSize(self.value-10)
            self.value = self.value -10

    def ChangeLineheightMinus(self, sender):
            lineheight = self.w.glyphLineView.getLineHeight()
            self.w.glyphLineView.setLineHeight(lineheight-30)
            
    def ChangeLineheightPlus(self, sender):
            lineheight = self.w.glyphLineView.getLineHeight()
            self.w.glyphLineView.setLineHeight(lineheight+30)
    
    def Inverse(self, sender):
        if self.d.checkBoxInverse.get() == 0:
            self.w.glyphLineView.setDisplayStates({'Inverse': False})
        else:
            self.w.glyphLineView.setDisplayStates({'Inverse': True})            

    def Metrics(self, sender):
        if self.d.checkBoxMetrics.get() == 0:
            self.w.glyphLineView.setDisplayStates({'Show Metrics': False})
        else:
            self.w.glyphLineView.setDisplayStates({'Show Metrics': True})

    def R2L(self, sender):
        if self.d.checkBoxR2L.get() == 0:
            self.w.glyphLineView.setDisplayStates({'Right to Left': False})
        else:
            self.w.glyphLineView.setDisplayStates({'Right to Left': True})

    def Stroke(self, sender):
        if self.d.checkBoxStroke.get() == 0:
            self.w.glyphLineView.setDisplayStates({'Stroke': False, 'Fill': True})
        else:
            self.w.glyphLineView.setDisplayStates({'Stroke': True, 'Fill': False})

   
InterpolateStepView()

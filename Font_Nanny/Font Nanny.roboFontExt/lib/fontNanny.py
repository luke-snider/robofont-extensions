"""
Font Nanny V.0.1 
Most of the Code is taken from Glyph Nanny Robofont Extension by Type Supply.
tweaked by Lukas Schneider, 2014 - 08 - 07
http://www.snider-inc.de

"""


from vanilla import FloatingWindow, TextBox, Button, HorizontalLine, SquareButton
from AppKit import NSColor
from vanilla import ColorWell
from robofab.interface.all.dialogs import ProgressBar
from fontTools.agl import AGL2UV
from robofab.pens.digestPen import DigestPointPen
import math


class FontNanny(object): 

    def __init__(self, font): 
        
        self.w = FloatingWindow((185, 370), "Font Nanny")
        y = 5
        self.w.info = TextBox((10, y, 180, 14), text="Glyph Checks (all Glyphs):", sizeStyle="small") 
        y += 20        
        self.w.check1 = SquareButton((10, y, 145, 20), "Unicode values", callback=self.perform, sizeStyle="small")
        self.w.color1 = ColorWell((155, y, 20, 20), color=NSColor.colorWithCalibratedRed_green_blue_alpha_(0,0,1,0.3))
        self.w.color1.enable(0)  
        y += 20
        self.w.check2 = SquareButton((10, y, 145, 20), "Contour Count", callback=self.perform, sizeStyle="small")
        self.w.color2 = ColorWell((155, y, 20, 20), color=NSColor.colorWithCalibratedRed_green_blue_alpha_(5,0,0,0.4))
        self.w.color2.enable(0)  
        y += 25
        self.w.info2 = TextBox((10, y, 180, 14), text="Outline Checks (all Glyphs):", sizeStyle="small")  
        y += 20        
        self.w.check3 = SquareButton((10, y, 145, 20), "Stray Points", callback=self.perform, sizeStyle="small")
        self.w.color3 = ColorWell((155, y, 20, 20), color=NSColor.colorWithCalibratedRed_green_blue_alpha_(.7,.0,.7, .9))
        self.w.color3.enable(0) 
        y += 20  
        self.w.check4 = SquareButton((10, y, 145, 20), "Small Contours", callback=self.perform, sizeStyle="small")
        self.w.color4 = ColorWell((155, y, 20, 20), color=NSColor.colorWithCalibratedRed_green_blue_alpha_(0,.8,0, 0.9))
        self.w.color4.enable(0) 
        y += 20  
        self.w.check5 = SquareButton((10, y, 145, 20), "Open Contours", callback=self.perform, sizeStyle="small")
        self.w.color5 = ColorWell((155, y, 20, 20), color=NSColor.colorWithCalibratedRed_green_blue_alpha_(.4, .4, .4, 0.8))
        self.w.color5.enable(0) 
        y += 20  
        self.w.check6 = SquareButton((10, y, 145, 20), "Duplicate Contours", callback=self.perform, sizeStyle="small")
        self.w.color6 = ColorWell((155, y, 20, 20), color=NSColor.colorWithCalibratedRed_green_blue_alpha_(1,0,0, 0.6))
        self.w.color6.enable(0)                      
        y += 20
        self.w.check7 = SquareButton((10, y, 145, 20), "Extreme points", callback=self.perform, sizeStyle="small")
        self.w.color7 = ColorWell((155, y, 20, 20), color=NSColor.colorWithCalibratedRed_green_blue_alpha_(0,.9,0, 0.6))
        self.w.color7.enable(0)
        y += 20  
        self.w.check8 = SquareButton((10, y, 145, 20), "Unnecessary Points", callback=self.perform, sizeStyle="small")
        self.w.color8 = ColorWell((155, y, 20, 20), color=NSColor.colorWithCalibratedRed_green_blue_alpha_(1, .0, 1, 0.8))
        self.w.color8.enable(0) 
        y += 20  
        self.w.check9 = SquareButton((10, y, 145, 20), "Unnecessary Handles", callback=self.perform, sizeStyle="small")
        self.w.color9 = ColorWell((155, y, 20, 20), color=NSColor.colorWithCalibratedRed_green_blue_alpha_(.4, .0, .0, .3))
        self.w.color9.enable(0) 
        y += 20  
        self.w.check10 = SquareButton((10, y, 145, 20), "Overlapping Points", callback=self.perform, sizeStyle="small")
        self.w.color10 = ColorWell((155, y, 20, 20), color=NSColor.colorWithCalibratedRed_green_blue_alpha_(.0, .0, .6, .3))
        self.w.color10.enable(0) 
        y += 20  
        self.w.check11 = SquareButton((10, y, 145, 20), "Points near vert. Metrics", callback=self.perform, sizeStyle="small")
        self.w.color11 = ColorWell((155, y, 20, 20), color=NSColor.colorWithCalibratedRed_green_blue_alpha_(1, 1, .0, .2))
        self.w.color11.enable(0)
        y += 20  
        self.w.check12 = SquareButton((10, y, 145, 20), "Complex Curves", callback=self.perform, sizeStyle="small")
        self.w.color12 = ColorWell((155, y, 20, 20), color=NSColor.colorWithCalibratedRed_green_blue_alpha_(1, 1, 0, 1))
        self.w.color12.enable(0) 
        y += 20
        self.w.check13 = SquareButton((10, y, 145, 20), "Crossed handles", callback=self.perform, sizeStyle="small")
        self.w.color13 = ColorWell((155, y, 20, 20), color=NSColor.colorWithCalibratedRed_green_blue_alpha_(1,0,.4,.2))
        self.w.color13.enable(0)
        y += 20  
        self.w.check14 = SquareButton((10, y, 145, 20), "Straight Lines", callback=self.perform, sizeStyle="small")
        self.w.color14 = ColorWell((155, y, 20, 20), color=NSColor.colorWithCalibratedRed_green_blue_alpha_(.0, .6, .0, .3))
        self.w.color14.enable(0)                                     
        y += 30        
        self.w.horizontalLine = HorizontalLine((10, y-5, 165, 1)) 
        self.w.clearGlyphMarksButton = SquareButton((10, y, 90, 20), "Clear all marks", callback=self.clearGlyphMarks, sizeStyle = "small")
        self.w.colorClearGlyphMarks = ColorWell((100, y, 20, 20), color=NSColor.colorWithCalibratedRed_green_blue_alpha_(1, 1, 1, 1))
        self.w.colorClearGlyphMarks.enable(0)  
        self.w.closeWin = SquareButton((120, y, -10, 20), "x) close", callback=self.CloseWindow, sizeStyle="small")
        self.w.open()
        
        
    def CloseWindow(self, sender):
        self.w.close() 

    def clearGlyphMarks(self, sender):
        font = CurrentFont()
        for g in font:
            if g.mark == (0,0,1,0.3) or (5,0,0,0.4) or (.7,.0,.7, .9) or (0,.8,0, 0.9) or (.4, .4, .4, 0.8) or (1,0,0, 0.6) or (0,.9,0, 0.6) or (1, .0, 1, 0.8) or (.4, .0, .0, .3) or (.0, .0, .6, .3) or (1, 1, .0, .2) or (1, 1, 0, 1) or (1,0,.4,.2) or (.0, .6, .0, .3):
                g.mark = None

    def perform(self, sender):
        senderInput = sender.getTitle()
        f = CurrentFont()
        tickCount = len(CurrentFont())
        progressBar = ProgressBar(title=senderInput, ticks=tickCount, label="checking all the glyphs...")
        tick = 0 
        
        if senderInput == "Open Contours":
            for glyph in f:
                self.testForOpenContours(glyph)
                tick = tick+1
                progressBar.tick(tick)
            progressBar.close()
        if senderInput == "Extreme points":
            for glyph in f:
                self.testForExtremePoints(glyph)
                tick = tick+1
                progressBar.tick(tick)
            progressBar.close()
        if senderInput == "Straight Lines":
            for glyph in f:
                self.testForStraightLines(glyph)
                tick = tick+1
                progressBar.tick(tick)
            progressBar.close()
        if senderInput == "Crossed handles":
            for glyph in f:
                self.testForCrossedHandles(glyph)
                tick = tick+1
                progressBar.tick(tick)
            progressBar.close()
        if senderInput == "Unicode values":
            for glyph in f:
                self.testUnicodeValue(glyph)
                tick = tick+1
                progressBar.tick(tick)
            progressBar.close()
        if senderInput == "Contour Count":
            for glyph in f:
                self.testContourCount(glyph)
                tick = tick+1
                progressBar.tick(tick)
            progressBar.close()
        if senderInput == "Duplicate Contours":
            for glyph in f:
                self.testDuplicateContours(glyph)
                tick = tick+1
                progressBar.tick(tick)
            progressBar.close()            
        if senderInput == "Small Contours":
            for glyph in f:
                self.testForSmallContours(glyph)
                tick = tick+1
                progressBar.tick(tick)
            progressBar.close()  
        if senderInput == "Complex Curves":
            for glyph in f:
                self.testForComplexCurves(glyph)
                tick = tick+1
                progressBar.tick(tick)
            progressBar.close() 
        if senderInput == "Unnecessary Points":
            for glyph in f:
                self.testForUnnecessaryPoints(glyph)
                tick = tick+1
                progressBar.tick(tick)
            progressBar.close()
        if senderInput == "Overlapping Points":
            for glyph in f:
                self.testForOverlappingPoints(glyph)
                tick = tick+1
                progressBar.tick(tick)
            progressBar.close()
        if senderInput == "Unnecessary Handles":
            for glyph in f:
                self.testForUnnecessaryHandles(glyph)
                tick = tick+1
                progressBar.tick(tick)
            progressBar.close()
        if senderInput == "Stray Points":
            for glyph in f:
                self.testForStrayPoints(glyph)
                tick = tick+1
                progressBar.tick(tick)
            progressBar.close()
        if senderInput == "Points near vert. Metrics":
            for glyph in f:
                self.testForPointsNearVerticalMetrics(glyph)
                tick = tick+1
                progressBar.tick(tick)
            progressBar.close()


    def testUnicodeValue(self, glyph):
        """
        A Unicode value should appear only once per font.
        """
        report = []
        font = glyph.getParent()
        uni = glyph.unicode
        name = glyph.name
        # test against AGL
        expectedUni = AGL2UV.get(name)
        if expectedUni != uni:
            report.append("Incorrect Unicode value?: %s." % name)
            glyph.mark = (0,0,1,0.3)
        # look for duplicates
        if uni is not None:
            duplicates = []
            for name in sorted(font.keys()):
                if name == glyph.name:
                    continue
                other = font[name]
                if other.unicode == uni:
                    duplicates.append(name)
                    glyph.mark = (0,0,1,0.3)
            report.append("The Unicode for this glyph is also used by: %s" % " ".join(duplicates))
            
    # Glyph Construction

    def testContourCount(self, glyph):
        """
        There shouldn't be too many overlapping contours.
        """
        report = []
        count = len(glyph)
        test = glyph.copy()
        test.removeOverlap()
        if count - len(test) > 2:
            report.append("This glyph has a unusally high number of overlapping contours.")
            glyph.mark = (5,0,0,0.4)
        return report

    def testDuplicateContours(self, glyph):
        """
        Contours shouldn't be duplicated on each other.
        """
        contours = {}
        for index, contour in enumerate(glyph):
            contour = contour.copy()
            contour.autoStartSegment()
            pen = DigestPointPen()
            contour.drawPoints(pen)
            digest = pen.getDigest()
            if digest not in contours:
                contours[digest] = []
            contours[digest].append(index)
        duplicateContours = []
        for digest, indexes in contours.items():
            if len(indexes) > 1:
                duplicateContours.append(indexes[0])
                glyph.mark = (1,0,0, 0.6)

    # Contours

    def testForSmallContours(self, glyph):
        """
        Contours should not have an area less than or equal to 4 units.
        """
        smallContours = {}
        for index, contour in enumerate(glyph):
            box = contour.box
            if not box:
                continue
            xMin, yMin, xMax, yMax = box
            w = xMax - xMin
            h = yMin - yMax
            area = abs(w * h)
            if area <= 4:
                smallContours[index] = contour.box
                glyph.mark = (0,.8,0, 0.9)

    def testForOpenContours(self, glyph):
        """
        Contours should be closed.
        """
        openContours = {}
        for index, contour in enumerate(glyph):
            if not contour.open:
                continue
            start = contour[0].onCurve
            start = (start.x, start.y)
            end = contour[-1].onCurve
            end = (end.x, end.y)
            if start != end:
                openContours[index] = (start, end)
            glyph.mark = (.4, .4, .4, 0.8)

    def testForExtremePoints(self, glyph):
        """
        Points should be at the extrema.
        """
        pointsAtExtrema = {}
        for index, contour in enumerate(glyph):
            dummy = glyph.copy()
            dummy.clear()
            dummy.appendContour(contour)
            dummy.extremePoints()
            testPoints = _getOnCurves(dummy[0])
            points = _getOnCurves(contour)
            if points != testPoints:
                pointsAtExtrema[index] = testPoints - points               
                glyph.mark = (0,.9,0, 0.6)

       
    def testForComplexCurves(self, glyph):
        """
        S curves are suspicious.
        """
        impliedS = {}
        for index, contour in enumerate(glyph):
            prev = _unwrapPoint(contour[-1].onCurve)
            for segment in contour:
                if segment.type == "curve":
                    pt0 = prev
                    pt1, pt2 = [_unwrapPoint(p) for p in segment.offCurve]
                    pt3 = _unwrapPoint(segment.onCurve)
                    line1 = (pt0, pt3)
                    line2 = (pt1, pt2)
                    if index not in impliedS:
                        impliedS[index] = []
                    if _intersectLines(line1, line2):
                        impliedS[index].append((prev, pt1, pt2, pt3))
                        glyph.mark = (1, 1, 0, 1)
                prev = _unwrapPoint(segment.onCurve)

    def testForCrossedHandles(self, glyph):
        """
        Handles shouldn't intersect.
        """
        crossedHandles = {}
        for index, contour in enumerate(glyph):
            pt0 = _unwrapPoint(contour[-1].onCurve)
            for segment in contour:
                pt3 = _unwrapPoint(segment.onCurve)
                if segment.type == "curve":
                    pt1, pt2 = [_unwrapPoint(p) for p in segment.offCurve]
                    # direct intersection
                    direct = _intersectLines((pt0, pt1), (pt2, pt3))
                    if direct:
                        if index not in crossedHandles:
                            crossedHandles[index] = []
                        crossedHandles[index].append(dict(points=(pt0, pt1, pt2, pt3), intersection=direct))               
                        glyph.mark = (1,0,.4,.2)
                    # indirect intersection
                    else:
                        while 1:
                            # bcp1 = ray, bcp2 = segment
                            angle = _calcAngle(pt0, pt1)
                            if angle in (0, 180.0):
                                t1 = (pt0[0] + 1000, pt0[1])
                                t2 = (pt0[0] - 1000, pt0[1])
                            else:
                                yOffset = _getAngleOffset(angle, 1000)
                                t1 = (pt0[0] + 1000, pt0[1] + yOffset)
                                t2 = (pt0[0] - 1000, pt0[1] - yOffset)
                            indirect = _intersectLines((t1, t2), (pt2, pt3))
                            if indirect:
                                if index not in crossedHandles:
                                    crossedHandles[index] = []
                                crossedHandles[index].append(dict(points=(pt0, indirect, pt2, pt3), intersection=indirect))
                                break
                            # bcp1 = segment, bcp2 = ray
                            angle = _calcAngle(pt3, pt2)
                            if angle in (90.0, 270.0):
                                t1 = (pt3[0], pt3[1] + 1000)
                                t2 = (pt3[0], pt3[1] - 1000)
                            else:
                                yOffset = _getAngleOffset(angle, 1000)
                                t1 = (pt3[0] + 1000, pt3[1] + yOffset)
                                t2 = (pt3[0] - 1000, pt3[1] - yOffset)
                            indirect = _intersectLines((t1, t2), (pt0, pt1))
                            if indirect:
                                if index not in crossedHandles:
                                    crossedHandles[index] = []
                                crossedHandles[index].append(dict(points=(pt0, pt1, indirect, pt3), intersection=indirect))            
                                glyph.mark = (1,0,.4,.2)
                                break
                            break
                pt0 = pt3

    def testForUnnecessaryPoints(self, glyph):
        """
        Consecutive segments shouldn't have the same angle.
        """
        unnecessaryPoints = {}
        for index, contour in enumerate(glyph):
            for segmentIndex, segment in enumerate(contour):
                if segment.type == "line":
                    prevSegment = contour[segmentIndex - 1]
                    nextSegment = contour[(segmentIndex + 1) % len(contour)]
                    if nextSegment.type == "line":
                        thisAngle = _calcAngle(prevSegment.onCurve, segment.onCurve)
                        nextAngle = _calcAngle(segment.onCurve, nextSegment.onCurve)
                        if thisAngle == nextAngle:
                            if index not in unnecessaryPoints:
                                unnecessaryPoints[index] = []
                            unnecessaryPoints[index].append(_unwrapPoint(segment.onCurve))
                            glyph.mark = (1, .0, 1, 0.8)

    def testForOverlappingPoints(self, glyph):
        """
        Consequtive points should not overlap.
        """
        overlappingPoints = {}
        for index, contour in enumerate(glyph):
            if len(contour) == 1:
                continue
            prev = _unwrapPoint(contour[-1].onCurve)
            for segment in contour:
                point = _unwrapPoint(segment.onCurve)
                if point == prev:
                    if index not in overlappingPoints:
                        overlappingPoints[index] = set()
                    overlappingPoints[index].add(point)
                    glyph.mark = (.0, .0, .6, .3)
                prev = point

    # Segments

    def testForUnnecessaryHandles(self, glyph):
        """
        Handles shouldn't be used if they aren't doing anything.
        """
        unnecessaryHandles = {}
        for index, contour in enumerate(glyph):
            prevPoint = contour[-1].onCurve
            for segment in contour:
                if segment.type == "curve":
                    pt0 = prevPoint
                    pt1, pt2 = segment.offCurve
                    pt3 = segment.onCurve
                    lineAngle = _calcAngle(pt0, pt3, 0)
                    bcpAngle1 = bcpAngle2 = None
                    if (pt0.x, pt0.y) != (pt1.x, pt1.y):
                        bcpAngle1 = _calcAngle(pt0, pt1, 0)
                    if (pt2.x, pt2.y) != (pt3.x, pt3.y):
                        bcpAngle2 = _calcAngle(pt2, pt3, 0)
                    if bcpAngle1 == lineAngle and bcpAngle2 == lineAngle:
                        if index not in unnecessaryHandles:
                            unnecessaryHandles[index] = []
                        unnecessaryHandles[index].append((_unwrapPoint(pt1), _unwrapPoint(pt2)))
                        glyph.mark = (.4, .0, .0, .3)
                prevPoint = segment.onCurve

    def testForStraightLines(self, glyph):
        """
        Lines shouldn't be just shy of vertical or horizontal.
        """
        straightLines = {}
        for index, contour in enumerate(glyph):
            prev = _unwrapPoint(contour[-1].onCurve)
            for segment in contour:
                point = _unwrapPoint(segment.onCurve)
                if segment.type == "line":
                    x = abs(prev[0] - point[0])
                    y = abs(prev[1] - point[1])
                    if x > 0 and x <= 5:
                        if index not in straightLines:
                            straightLines[index] = set()
                        straightLines[index].add((prev, point))
                        glyph.mark = (.0, .6, .0, .3)
                    if y > 0 and y <= 5:
                        if index not in straightLines:
                            straightLines[index] = set()
                        straightLines[index].add((prev, point))
                        glyph.mark = (.0, .6, .0, .3)
                prev = point

    # Points

    def testForStrayPoints(self, glyph):
        """
        There should be no stray points.
        """
        strayPoints = {}
        for index, contour in enumerate(glyph):
            if len(contour) == 1:
                pt = contour[0].onCurve
                pt = (pt.x, pt.y)
                strayPoints[index] = pt
                glyph.mark = (.7,.0,.7, .9)

    def testForPointsNearVerticalMetrics(self, glyph):
        """
        Points shouldn't be just off a vertical metric.
        """
        font = glyph.getParent()
        verticalMetrics = {
            0 : set()
        }
        for attr in "descender xHeight capHeight ascender".split(" "):
            value = getattr(font.info, attr)
            verticalMetrics[value] = set()
        for contour in glyph:
            for segment in contour:
                pt = _unwrapPoint(segment.onCurve)
                y = pt[1]
                for v in verticalMetrics:
                    d = abs(v - y)
                    if d != 0 and d <= 5:
                        verticalMetrics[v].add(pt)
                        glyph.mark = (1, 1, .0, .2)
        for verticalMetric, points in verticalMetrics.items():
            if not points:
                del verticalMetrics[verticalMetric]


# Utilities

### _getOnCurves is for missing extrema test
def _getOnCurves(contour):
    points = set()
    for segement in contour:
        pt = segement.onCurve
        points.add((pt.x, pt.y))
    return points

###
def _unwrapPoint(pt):
    return pt.x, pt.y

def _intersectLines((a1, a2), (b1, b2)):
    # adapted from: http://www.kevlindev.com/gui/math/intersection/Intersection.js
    ua_t = (b2[0] - b1[0]) * (a1[1] - b1[1]) - (b2[1] - b1[1]) * (a1[0] - b1[0]);
    ub_t = (a2[0] - a1[0]) * (a1[1] - b1[1]) - (a2[1] - a1[1]) * (a1[0] - b1[0]);
    u_b  = (b2[1] - b1[1]) * (a2[0] - a1[0]) - (b2[0] - b1[0]) * (a2[1] - a1[1]);
    if u_b != 0:
        ua = ua_t / u_b;
        ub = ub_t / u_b;
        if 0 <= ua and ua <= 1 and 0 <= ub and ub <= 1:
            return a1[0] + ua * (a2[0] - a1[0]), a1[1] + ua * (a2[1] - a1[1])
        else:
            return None
    else:
        return None

def _calcAngle(point1, point2, r=None):
    if not isinstance(point1, tuple):
        point1 = _unwrapPoint(point1)
    if not isinstance(point2, tuple):
        point2 = _unwrapPoint(point2)
    width = point2[0] - point1[0]
    height = point2[1] - point1[1]
    angle = round(math.atan2(height, width) * 180 / math.pi, 3)
    if r is not None:
        angle = round(angle, r)
    return angle

def _getAngleOffset(angle, distance):
    A = 90
    B = angle
    C = 180 - (A + B)
    if C == 0:
        return 0
    c = distance
    A = math.radians(A)
    B = math.radians(B)
    C = math.radians(C)
    b = (c * math.sin(B)) / math.sin(C)
    return b
    
FontNanny(CurrentFont())
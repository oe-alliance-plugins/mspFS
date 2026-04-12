# -*- coding: utf-8 -*-
###############################################################################
# schichtFS von shadowrider
###############################################################################
from . import _
from Screens.Screen import Screen
from Screens.ChoiceBox import ChoiceBox
from Screens.HelpMenu import HelpableScreen
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Screens.InputBox import InputBox
from Screens.MessageBox import MessageBox

from Components.ActionMap import ActionMap
from Components.ActionMap import HelpableActionMap
from Components.Input import Input
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.Sources.StaticText import StaticText
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Components.MenuList import MenuList
from Components.ConfigList import ConfigListScreen
from Components.config import config, ConfigSelection, ConfigText, ConfigDateTime, ConfigYesNo, getConfigListEntry, NoSave, ConfigNothing

from enigma import eListboxPythonMultiContent, RT_HALIGN_LEFT, RT_HALIGN_RIGHT, RT_HALIGN_CENTER, RT_VALIGN_CENTER, gFont, eListbox, getDesktop
from skin import parseColor, parseFont
from configparser import ConfigParser
from Tools.Directories import fileExists
import datetime
import os
from time import strftime, mktime, strptime
from .VKB_mod import VKB_mod  # as VirtualKeyBoard


monatsnamen = (_("January"), _("February"), _("March"), _("April"), _("May"), _("June"), _("July"), _("August"), _("September"), _("October"), _("November"), _("December"))

color_list = ("#006400", "#BDB76B", "#556B2F", "#CAFF70", "#BCEE68", "#A2CD5A", "#6E8B3D", "#8FBC8F", "#C1FFC1",
"#B4EEB4", "#9BCD9B", "#698B69", "#228B22", "#ADFF2F", "#7CFC00", "#90EE90", "#20B2AA", "#32CD32", "#3CB371", "#00FA9A", "#F5FFFA", "#6B8E23", "#C0FF3E", "#B3EE3A", "#9ACD32",
"#698B22", "#98FB98", "#9AFF9A", "#7CCD7C", "#548B54", "#2E8B57", "#54FF9F", "#4EEE94", "#43CD80", "#00FF7F", "#00EE76", "#00CD66", "#008B45", "#7FFF00", "#76EE00", "#66CD00",
"#458B00", "#00FF00", "#00EE00", "#00CD00", "#008B00", "#F0E68C", "#FFF68F", "#EEE685", "#CDC673", "#8B864E", "#F0F8FF", "#8A2BE2", "#5F9EA0", "#98F5FF", "#8EE5EE", "#7AC5CD",
"#53868B", "#6495ED", "#00008B", "#008B8B", "#483D8B", "#00CED1", "#00BFFF", "#00B2EE", "#009ACD", "#00688B", "#1E90FF", "#1C86EE", "#1874CD", "#104E8B", "#ADD8E6", "#BFEFFF",
"#B2DFEE", "#9AC0CD", "#68838B", "#E0FFFF", "#D1EEEE", "#B4CDCD", "#7A8B8B", "#87CEFA", "#B0E2FF", "#A4D3EE", "#8DB6CD", "#607B8B", "#8470FF", "#B0C4DE", "#CAE1FF", "#BCD2EE",
"#A2B5CD", "#6E7B8B", "#66CDAA", "#0000CD", "#7B68EE", "#48D1CC", "#191970", "#000080", "#AFEEEE", "#BBFFFF", "#AEEEEE", "#96CDCD", "#668B8B", "#B0E0E6", "#4169E1", "#4876FF",
"#436EEE", "#3A5FCD", "#27408B", "#87CEEB", "#87CEFF", "#7EC0EE", "#6CA6CD", "#4A708B", "#6A5ACD", "#836FFF", "#7A67EE", "#6959CD", "#473C8B", "#4682B4", "#63B8FF", "#5CACEE",
"#4F94CD", "#36648B", "#7FFFD4", "#76EEC6", "#458B74", "#F0FFFF", "#E0EEEE", "#C1CDCD", "#838B8B", "#0000FF", "#0000EE", "#00FFFF", "#00EEEE", "#00CDCD", "#40E0D0", "#00F5FF",
"#00E5EE", "#00C5CD", "#00868B", "#8B008B", "#9932CC", "#BF3EFF", "#B23AEE", "#9A32CD", "#68228B", "#9400D3", "#FFF0F5", "#EEE0E5", "#CDC1C5", "#8B8386", "#BA55D3", "#E066FF",
"#D15FEE", "#B452CD", "#7A378B", "#9370DB", "#AB82FF", "#9F79EE", "#8968CD", "#5D478B", "#E6E6FA", "#FF00FF", "#EE00EE", "#CD00CD", "#B03060", "#FF34B3", "#EE30A7", "#CD2990",
"#8B1C62", "#DA70D6", "#FF83FA", "#EE7AE9", "#CD69C9", "#8B4789", "#DDA0DD", "#FFBBFF", "#EEAEEE", "#CD96CD", "#8B668B", "#A020F0", "#9B30FF", "#912CEE", "#7D26CD", "#551A8B",
"#D8BFD8", "#FFE1FF", "#EED2EE", "#CDB5CD", "#8B7B8B", "#EE82EE", "#8B0000", "#FF1493", "#EE1289", "#CD1076", "#8B0A50", "#FF69B4", "#FF6EB4", "#EE6AA7", "#CD6090", "#8B3A62",
"#CD5C5C", "#FF6A6A", "#EE6363", "#CD5555", "#8B3A3A", "#FFB6C1", "#FFAEB9", "#EEA2AD", "#CD8C95", "#8B5F65", "#C71585", "#FFE4E1", "#EED5D2", "#CDB7B5", "#8B7D7B", "#FF4500",
"#EE4000", "#CD3700", "#8B2500", "#DB7093", "#FF82AB", "#EE799F", "#CD6889", "#8B475D", "#D02090", "#FF3E96", "#EE3A8C", "#CD3278", "#8B2252", "#B22222", "#FF3030", "#EE2C2C",
"#CD2626", "#8B1A1A", "#FFC0CB", "#FFB5C5", "#EEA9B8", "#CD919E", "#8B636C", "#FF0000", "#EE0000", "#CD0000", "#FF6347", "#EE5C42", "#CD4F39", "#8B3626", "#FF8C00", "#FF7F00",
"#EE7600", "#CD6600", "#8B4500", "#E9967A", "#F08080", "#FFA07A", "#EE9572", "#CD8162", "#8B5742", "#FFDAB9", "#EECBAD", "#CDAF95", "#8B7765", "#FFE4C4", "#EED5B7", "#CDB79E",
"#8B7D6B", "#FF7F50", "#FF7256", "#EE6A50", "#CD5B45", "#8B3E2F", "#F0FFF0", "#E0EEE0", "#C1CDC1", "#838B83", "#FFA500", "#EE9A00", "#CD8500", "#8B5A00", "#FA8072", "#FF8C69",
"#EE8262", "#CD7054", "#8B4C39", "#A0522D", "#FF8247", "#EE7942", "#CD6839", "#8B4726", "#FFEBCD", "#D9D919", "#B8860B", "#FFB90F", "#EEAD0E", "#CD950C", "#8B6508", "#FFFACD", "#EEE9BF",
"#CDC9A5", "#8B8970", "#EEDD82", "#FFEC8B", "#EEDC82", "#CDBE70", "#8B814C", "#FAFAD2", "#FFFFE0", "#EEEED1", "#CDCDB4", "#8B8B7A", "#EEE8AA", "#FFEFD5", "#FFF8DC", "#EEE8CD",
"#CDC8B1", "#8B8878", "#FFD700", "#EEC900", "#CDAD00", "#8B7500", "#DAA520", "#FFC125", "#EEB422", "#CD9B1D", "#8B6914", "#FFE4B5", "#FFFF00", "#EEEE00", "#CDCD00", "#8B8B00",
"#BC8F8F", "#FFC1C1", "#EEB4B4", "#CD9B9B", "#8B6969", "#8B4513", "#F4A460", "#F5F5DC", "#A52A2A", "#FF4040", "#EE3B3B", "#CD3333", "#8B2323", "#DEB887", "#FFD39B", "#EEC591",
"#CDAA7D", "#8B7355", "#D2691E", "#FF7F24", "#EE7621", "#CD661D", "#CD853F", "#D2B48C", "#FFA54F", "#EE9A49", "#8B5A2B", "#2F4F4F", "#97FFFF", "#8DEEEE", "#79CDCD", "#528B8B",
"#696969", "#D3D3D3", "#778899", "#708090", "#C6E2FF", "#B9D3EE", "#9FB6CD", "#6C7B8B", "#BEBEBE", "#000000", "#030303", "#050505", "#080808", "#0A0A0A", "#0D0D0D", "#0F0F0F",
"#121212", "#141414", "#171717", "#1A1A1A", "#1C1C1C", "#1F1F1F", "#212121", "#242424", "#262626", "#292929", "#2B2B2B", "#2E2E2E", "#303030", "#333333", "#363636", "#383838",
"#3B3B3B", "#3D3D3D", "#404040", "#424242", "#454545", "#474747", "#4A4A4A", "#4D4D4D", "#4F4F4F", "#525252", "#545454", "#575757", "#595959", "#5C5C5C", "#5E5E5E", "#616161",
"#636363", "#666666", "#6B6B6B", "#6E6E6E", "#707070", "#737373", "#757575", "#787878", "#7A7A7A", "#7D7D7D", "#7F7F7F", "#828282", "#858585", "#878787", "#8A8A8A", "#8C8C8C",
"#8F8F8F", "#919191", "#949494", "#969696", "#999999", "#9C9C9C", "#9E9E9E", "#A1A1A1", "#A3A3A3", "#A6A6A6", "#A8A8A8", "#ABABAB", "#ADADAD", "#B0B0B0", "#B3B3B3", "#B5B5B5",
"#B8B8B8", "#BABABA", "#BDBDBD", "#BFBFBF", "#C2C2C2", "#C4C4C4", "#C7C7C7", "#C9C9C9", "#CCCCCC", "#CFCFCF", "#D1D1D1", "#D4D4D4", "#D6D6D6", "#D9D9D9", "#DBDBDB", "#DEDEDE",
"#E0E0E0", "#E3E3E3", "#E5E5E5", "#E8E8E8", "#EBEBEB", "#EDEDED", "#F0F0F0", "#F2F2F2", "#F5F5F5", "#F7F7F7", "#FAFAFA", "#FCFCFC", "#FFFFFF", "#FAEBD7", "#FFEFDB", "#EEDFCC",
"#CDC0B0", "#8B8378", "#FFFAF0", "#F8F8FF", "#FFDEAD", "#EECFA1", "#CDB38B", "#8B795E", "#FDF5E6", "#DCDCDC", "#FFFFF0", "#EEEEE0", "#CDCDC1", "#8B8B83", "#FAF0E6", "#FFF5EE",
"#EEE5DE", "#CDC5BF", "#8B8682", "#FFFAFA", "#EEE9E9", "#CDC9C9", "#8B8989", "#F5DEB3", "#FFE7BA", "#EED8AE", "#CDBA96", "#8B7E66", "#20343c4f", "#C6E0F3", "#5C3317", "#B5A642",
"#8C7853", "#D98719", "#B87333", "#DC143C", "#5C4033", "#A9A9A9", "#4A766E", "#871F78", "#8FBC8B", "#97694F", "#855E42", "#856363", "#F5CCCC", "#D19275", "#527F76", "#215E21",
"#4B0082", "#E9C2A6", "#E47833", "#EAEAAE", "#9370D8", "#A68064", "#23238E", "#4E4EFF", "#FF6EC7", "#00009C", "#EBC79E", "#CFB53B", "#D87093", "#D9D9F3", "#5959AB", "#8C1717",
"#6B4226", "#FF1CAE", "#38B0DE", "#CDCDCD",)


turnus = ()
heute = datetime.date.today()

selected = heute
keystop = 0
selected_schicht = None

global L4l
try:
    from Plugins.Extensions.LCD4linux.module import L4Lelement
    L4l = True
except:
    L4l = None


configparser = ConfigParser()
configparser.read("/etc/ConfFS/mspFS.conf")

if configparser.has_section("settings"):
    if configparser.has_option("settings", "schicht_col"):
         schicht_colors = eval(configparser.get("settings", "schicht_col"))
    else:
        schicht_colors = {"F": "#008B45", "S": "#FFD700", "N": "#3A5FCD", "fr": "#858585"}

    if configparser.has_option("settings", "prog_colors"):
         prog_colors = eval(configparser.get("settings", "prog_colors"))
    else:
        prog_colors = ("000000", "B0C4DE", "C1FFC1", "FFA54F", "EE4000", "000000")
    if configparser.has_option("settings", "turnus"):
         turnus = configparser.get("settings", "turnus").split(",")
         #del turnus[-1]
         #turnus= [x.strip() for x in turnus.split(',')]
    else:
        turnus = ("N", "fr", "fr", "fr", "F", "F", "S", "S", "N", "N", "N")
    if configparser.has_option("settings", "l4l_sets"):
         l4l_sets = configparser.get("settings", "l4l_sets").split(":")

    else:
        l4l_sets = ("On", "1", "1", "0", "80", "500", "100", "10", "On,Idle", "0")
    if configparser.has_option("settings", "start_date"):
         dx = configparser.get("settings", "start_date").split("-")
         start_date = datetime.date(int(dx[0]), int(dx[1]), int(dx[2]))
    else:
        start_date = datetime.date.today().replace(month=1, day=1)
    if configparser.has_option("settings", "sonders"):
         sonders = eval(configparser.get("settings", "sonders"))
    else:
        sonders = {}
    if configparser.has_option("settings", "autodel"):
         autodel = configparser.get("settings", "autodel")
    else:
        autodel = "0"
else:
    schicht_colors = {"F": "#008B45", "S": "#FFD700", "N": "#3A5FCD", "fr": "#858585"}
    prog_colors = ("000000", "B0C4DE", "C1FFC1", "FFA54F", "EE4000", "000000")
    turnus = ("N", "N", "N", "fr", "F", "F", "S", "S", "S", "fr", "fr")
    l4l_sets = ("Off", "1", "1", "0", "80", "500", "100", "10", "On,Idle")
    start_date = datetime.date.today().replace(month=1, day=1)
    sonders = {}
    autodel = "0"


class Farben():
        def farb_re(session, farb):
                if farb:
                   new_farb = int(str(farb).strip().lstrip('#'), 16)
                   if new_farb == 0:
                       new_farb = 0x000001
                   return (new_farb)


class start_list(MenuList):
    def __init__(self, list, enableWrapAround=False):
        MenuList.__init__(self, list, enableWrapAround, eListboxPythonMultiContent)
        DWide = getDesktop(0).size().width()
#       if DWide == 720:
#            self.l.setFont(0, gFont("Regular", fontsize_list-2))
#            self.l.setFont(1, gFont("Regular", fontsize_list))
#       else:
#            self.l.setFont(0, gFont("Regular", fontsize_list))
#            self.l.setFont(1, gFont("Regular", fontsize_list+2))
        self.l.setFont(1, gFont("Regular", 22))
        self.l.setFont(2, gFont("Regular", 26))

    def postWidgetCreate(self, instance):
        MenuList.postWidgetCreate(self, instance)
        instance.setItemHeight(40)


class start_list(MenuList):
    def __init__(self, list, enableWrapAround=False):
        MenuList.__init__(self, list, enableWrapAround, eListboxPythonMultiContent)
        DWide = getDesktop(0).size().width()
        self.l.setFont(1, gFont("Regular", 22))
        self.l.setFont(2, gFont("Regular", 26))

    def postWidgetCreate(self, instance):
        MenuList.postWidgetCreate(self, instance)
        instance.setItemHeight(40)

    def buildList(self, listnew, d1):
        global keystop
        keystop = 1
        list = []
        #prog_colors(datum-text,datum-farbe,heute-farbe,kopf-farbe,so-farbe,kal-bgr
        pos_vorn = 5
        wochentage = ("Mo", "Di", "Mi", "Do", "Fr", "Sa")
        res = [""]
        bgcolor = int(prog_colors[5], 16)  # int("525252", 16)
        color = int(prog_colors[3], 16)
        res.append((eListboxPythonMultiContent.TYPE_TEXT, pos_vorn, 3, 30, 25, 1, RT_HALIGN_CENTER, " ", color, color, int("000000", 16)))
        pos_vorn += 70
        for x in wochentage:
          res.append((eListboxPythonMultiContent.TYPE_TEXT, pos_vorn, 3, 78, 25, 2, RT_HALIGN_CENTER | RT_VALIGN_CENTER, str(x), color, color, bgcolor))
          pos_vorn += 80
        res.append((eListboxPythonMultiContent.TYPE_TEXT, pos_vorn, 3, 78, 25, 2, RT_HALIGN_CENTER | RT_VALIGN_CENTER, "So", int(prog_colors[4], 16), int(prog_colors[4], 16), bgcolor))
        list.append(res)
        color = int("000000", 16)
        sel_col = int("FF0000", 16)
        #f=open("/tmp/dattest","a")
        #f.write(str(heute)+"\n\n")
        for x in listnew:

             res = [x[1]]
             res2 = [x[1]]
             pos_vorn = 5
             res.append((eListboxPythonMultiContent.TYPE_TEXT, pos_vorn, 3, 40, 38, 2, RT_HALIGN_RIGHT | RT_VALIGN_CENTER, x[1], int(prog_colors[3], 16), int(prog_colors[3], 16), int(prog_colors[5], 16)))
             res2.append((eListboxPythonMultiContent.TYPE_TEXT, pos_vorn, 3, 40, 26, 1, RT_HALIGN_LEFT, " ", color, color, int(prog_colors[5], 16)))
             pos_vorn += 70
             for xa in x[0]:
                size_minus = 0
                if xa[2] == selected:
                    global selected_schicht
                    selected_schicht = xa[1]
                    size_minus = 3
                    res.append((eListboxPythonMultiContent.TYPE_TEXT, pos_vorn, 0, 78, 40, 2, RT_HALIGN_CENTER, "", sel_col, sel_col, sel_col))
                    res2.append((eListboxPythonMultiContent.TYPE_TEXT, pos_vorn, 0, 78, 3, 1, RT_HALIGN_CENTER, "", sel_col, sel_col, sel_col))
                    #res2.append((eListboxPythonMultiContent.TYPE_TEXT,pos_vorn+size_minus, 0, 72, 3, 1, RT_HALIGN_CENTER, "", sel_col, int(prog_colors[5], 16), int(prog_colors[5], 16)))
                text = str(xa[1])
                s_col = xa[1]
                sbgcolor = int("858585", 16)
                if xa[3] in sonders:
                   text = sonders[xa[3]]
                   s_col = sonders[xa[3]]
                try:
                    sbgcolor = Farben().farb_re(schicht_colors[s_col])  # int(schicht_colors[s_col].lstrip('#'), 16)
                except KeyError:
                   schicht_colors[xa[1]] = "858585"
                   sbgcolor = int("858585", 16)
                #f.write(str(heute)+"\n\n")
                bgcolor = Farben().farb_re(prog_colors[1])  # int(prog_colors[1].lstrip('#'), 16)
                color = Farben().farb_re(prog_colors[0])  # int(prog_colors[0].lstrip('#'), 16)
                if xa == x[0][-1]:
                    Farben().farb_re(prog_colors[4])  # color=int(prog_colors[4].lstrip('#'), 16)
                if xa[2] == heute:
                     bgcolor = Farben().farb_re(prog_colors[2])  # int(prog_colors[2].lstrip('#'), 16) #int(color_list[10].lstrip('#'), 16)
                res.append((eListboxPythonMultiContent.TYPE_TEXT, pos_vorn + size_minus, 3, 78 - size_minus * 2, 38, 2, RT_HALIGN_CENTER | RT_VALIGN_CENTER, str(xa[0]), color, color, bgcolor))

                color = Farben().farb_re(prog_colors[0])  # int(prog_colors[0].lstrip('#'), 16) #int("000000", 16)
                if xa[2] >= start_date:
                 #try:
                 #  sbgcolor= int(schicht_colors[xa[1]].lstrip('#'), 16)
                 #except KeyError:
                 #  schicht_colors[xa[1]]="858585"
                 #  sbgcolor= int("858585", 16)
                 res2.append((eListboxPythonMultiContent.TYPE_TEXT, pos_vorn, 3, 78, 20, 1, RT_HALIGN_CENTER | RT_VALIGN_CENTER, text, color, color, sbgcolor))
                pos_vorn += 80
             list.append(res)
             list.append(res2)
        self.l.setList(list)
        keystop = 0


class mspFS_anzeige(Screen):
    skin = """<screen name="mspFS" title="mspFS - mein Schichtplan " position="center,center" size="710,470">
        <widget name="titel" font="Regular;24" zPosition="3" halign="center" size="710,25" foregroundColor="#FFFFFF" transparent="1"  />
        <widget name="listlabel" position="20,40" size="690,430" zPosition="3" foregroundColor="#FFFFFF" backgroundColor="#000000" scrollbarMode="showNever" selectionDisabled="1"/>
    </screen>"""

    def __init__(self, session, version):
        if turnus and len(turnus):
            Screen.__init__(self, session)
            self.title = "mspFS - mein Schichtplan" + " " * 10 + "Vers. " + version
            self.listlabel = start_list([])
            self["listlabel"] = self.listlabel
            self["titel"] = Label()
            self.mo_dat = None
            self["actions"] = ActionMap(["OkCancelActions", "DirectionActions", "MenuActions", "ChannelUpDownActions"],
                {
                        "ok": self.day_set,
                        "cancel": self.cancel,
                        "left": self.back,
                        "right": self.next,
                        "up": self.up,
                        "down": self.down,
                        "menu": self.settings,
                        "channelUp": self.next_mon,
                        "channelDown": self.back_mon,
                }, -1)
            global heute
            heute = datetime.date.today()
            self.dat_error = 0
            if heute.year == 1970:
               self.dat_error = 1
            self.onLayoutFinish.append(self.make_list)
#                               "up": self.keyUp,
#                               "down": self.keyDown,

    def day_set(self):
             self.session.openWithCallback(self.make_list, day_conf)

    def settings(self):
             self.session.openWithCallback(self.make_list, msp_conf)

    def make_list(self, datum=None):
            global selected
            sch_list = []
            sch1_list = []
            for x in turnus:
                if x.strip() not in sch1_list:
                     sch1_list.append(x.strip())

            start = heute
            if datum:
                start = datum
            self.start = start
            self.monat = start.month
            self.jahr = start.year
            if self.dat_error:
               self["titel"].setText("Systemdate is failed! / Systemdatum ist falsch!")
            else:
                self["titel"].setText(monatsnamen[start.month - 1] + " " + str(self.jahr))

            erstdatum = start_date  # datetime.date(2015,1,1)

            tage = start - erstdatum
            sch_tag = tage.days
            wt = start.isoweekday()
            if wt > 0:
                start = start - datetime.timedelta(wt - 1)
                sch_tag = sch_tag - wt + 1
            self.start = start
            if sch_tag > len(turnus):
                sch_tag = sch_tag % len(turnus)
            dat = start
            d1 = 0
            for i in range(5):
                w_list = []
                wo = None
                self.mo_dat = dat
                for x in range(7):
                    if i == 4 and x == 6:
                        self.end = dat
                    if sch_tag + 1 > len(turnus):
                        sch_tag = sch_tag % len(turnus)
                    if not wo:
                        wo = dat.isocalendar()[1]
                    if dat == heute:
                        d1 = dat.day

                        #f.write("heute: ")
                    #if dat.day==8:
                    #     self["titel"].setText(str(dat.month))
                    #f.write(str(dat.weekday())+" -- "+str(dat.day)+" -- "+str(schichten[sch_tag])+"\n")
                    stamp = str(dat).replace("-", "")
                    if sch_tag >= 0:
                        w_list.append((str(dat.day), str(turnus[sch_tag]).strip(), dat, stamp))
                    else:
                        w_list.append((str(dat.day), "", dat, stamp))
                    dat = dat + datetime.timedelta(1)
                    sch_tag += 1
                sch_list.append((w_list, '%0.2d' % (wo)))
            #f.write("\n############################################\n")
            #f.close()
            if selected > self.end or selected < self.start:
               selected = self.start
            self["listlabel"].buildList(sch_list, d1)

    def down(self):
        global keystop, selected
        if keystop == 0:
           keystop = 1
           self.keystop = 1
           dat = self.start
           selected = selected + datetime.timedelta(7)
           if selected > self.end:
                    dat = self.start + datetime.timedelta(7)
           self.make_list(dat)

    def up(self):
        global keystop, selected
        if keystop == 0:
           keystop = 1
           dat = self.start
           selected = selected - datetime.timedelta(7)
           if selected < self.start:
                    dat = self.start - datetime.timedelta(7)
           self.make_list(dat)

    def next(self):
        global keystop, selected
        if keystop == 0:
           keystop = 1
           dat = self.start
           selected = selected + datetime.timedelta(1)
           if selected > self.end:
                    dat = self.start + datetime.timedelta(7)
           self.make_list(dat)
           #self.dunb()

    def back(self):
        global keystop, selected
        if keystop == 0:
           keystop = 1
           dat = self.start
           selected = selected - datetime.timedelta(1)
           if selected < self.start:
                    dat = self.start - datetime.timedelta(7)
           self.make_list(dat)

    def back_mon(self):
        global keystop
        if keystop == 0:
           keystop = 1
           monat = self.monat - 1
           jahr = self.jahr
           if monat < 1:
              monat = 12
              jahr = self.jahr - 1
           #if datetime.date(jahr,monat,1)>= start_date:
           self.make_list(datetime.date(jahr, monat, 1))

    def next_mon(self):
        global keystop
        if keystop == 0:
           keystop = 1
           monat = self.monat + 1
           jahr = self.jahr
           if monat > 12:
              monat = 1
              jahr = self.jahr + 1
           self.make_list(datetime.date(jahr, monat, 1))

    def cancel(self):
           self.close()


class cate_liste(MenuList):
    def __init__(self, list, enableWrapAround=False):
        MenuList.__init__(self, list, enableWrapAround, eListboxPythonMultiContent)
        self.l.setFont(0, gFont("Regular", 24))
        self.l.setFont(1, gFont("Regular", 50))

    def postWidgetCreate(self, instance):
        MenuList.postWidgetCreate(self, instance)
        instance.setItemHeight(44)

    def buildList(self, listnew, idx=0):
        list = []
        for x in listnew:
            res = [x]
            if x[2] == "comment":
                 res.append((eListboxPythonMultiContent.TYPE_TEXT, 0, 5, 450, 30, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, x[0], int(prog_colors[3], 16), int(prog_colors[3], 16)))
            else:
                txtcol = Farben().farb_re(prog_colors[0])  # int(prog_colors[0], 16)
                if x[1]:
                    bgcol = Farben().farb_re(x[1])  # int(x[1].lstrip('#'), 16)

                if x[0] in ("Text Datum"):          #,_("calendar event")
                     bgcol = Farben().farb_re(prog_colors[1])  # int(prog_colors[1], 16)
                elif x[0] == "Sonntag":          #,_("calendar event")
                     txtcol = Farben().farb_re(x[1])  # int(x[1].lstrip('#'), 16)
                     bgcol = Farben().farb_re(prog_colors[1])  # int(prog_colors[1], 16)
                elif x[0] == "Kopfzeilen":
                     txtcol = Farben().farb_re(x[1])  # int(x[1].lstrip('#'), 16)
                     bgcol = Farben().farb_re(prog_colors[5])  # int(prog_colors[5], 16)
                #elif x[2] == "sch_col":
                #     bgcol=int(x[1].lstrip('#'), 16)
                #     txtcol=int(prog_colors[0], 16)
                res.append((eListboxPythonMultiContent.TYPE_TEXT, 5, 5, 500, 30, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, x[0]))
                if not x[1]:
                    res.append((eListboxPythonMultiContent.TYPE_TEXT, 400, 5, 150, 30, 0, RT_HALIGN_RIGHT | RT_VALIGN_CENTER, x[2]))
                else:
                    res.append((eListboxPythonMultiContent.TYPE_TEXT, 450, 5, 130, 30, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, " ", txtcol, txtcol, bgcol, bgcol))
                    res.append((eListboxPythonMultiContent.TYPE_TEXT, 450, 5, 120, 30, 0, RT_HALIGN_CENTER | RT_VALIGN_CENTER, "text", txtcol, txtcol))

            list.append(res)
        self.l.setList(list)
        self.moveToIndex(idx)


class msp_conf(Screen, HelpableScreen):

        DWide = getDesktop(0).size().width()

        skin = """
                <screen position="center,center" size="600,480" title="Select Color" >
                        <widget name="menu" position="10,5" size="580,430" scrollbarMode="showOnDemand" />
                <ePixmap pixmap="skin_default/buttons/red.png" position="10,440" size="140,40" alphatest="on" />
                <ePixmap pixmap="skin_default/buttons/green.png" position="155,440" size="140,40"  alphatest="on" />
                <widget name="pic_yellow" pixmap="skin_default/buttons/yellow.png" position="300,440" size="140,40"  alphatest="on" />
                <widget name="pic_blue" pixmap="skin_default/buttons/blue.png" position="450,440" size="140,40"  alphatest="on" />

                <widget name="key_red" position="10,443" zPosition="1" size="140,35" valign="center" halign="center" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" noWrap="1" shadowOffset="-1,-1" />
                <widget name="key_green" position="155,443" zPosition="1" size="140,35" valign="center" halign="center" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" noWrap="1" shadowOffset="-1,-1" />
                <widget name="key_yellow" position="300,443" zPosition="1" size="140,35" valign="center" halign="center" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" noWrap="1" shadowOffset="-1,-1" />
                <widget name="key_blue" position="450,443" zPosition="1" size="140,35" valign="center" halign="center" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" noWrap="1" shadowOffset="-1,-1" />

                </screen>"""

        def __init__(self, session):

                self.color_list = list(prog_colors)

                Screen.__init__(self, session)
                HelpableScreen.__init__(self)
                self.setTitle(_("Schichtplaner-Einstellungen"))
                self.idx = 0
                self.lcl_sets2 = list(l4l_sets)
                if len(self.lcl_sets2) == 9:
                    self.lcl_sets2.append("0")
                self.list = []
                self.anzeigeliste = cate_liste([])
                self["menu"] = self.anzeigeliste
                self["menu"].onSelectionChanged.append(self.selectionChanged)
                self.autodel_list = ("nie", "voriges Jahr")
                self.load_list()

                self["key_green"] = Label(_("Save"))
                self["key_red"] = Label(_("Cancel"))
                self["key_yellow"] = Label(_("delete"))
                self["pic_yellow"] = Pixmap()
                self["key_blue"] = Label(_("New"))
                self["pic_blue"] = Pixmap()
                self["pic_yellow"].hide()
                self["key_yellow"].hide()
                self["pic_blue"].hide()
                self["key_blue"].hide()
#               self["key_blue"] = Label(_("Color"))
                #self["help"] = Label(_("Press 'ok' for standard-list or write"))

                self["OkCancelActions"] = HelpableActionMap(self, "OkCancelActions",
                {
                        "cancel": (self.cancel, _("Cancel")),
                        "ok": (self.text, _("Edit selected option")),
                })

                self["ColorActions"] = HelpableActionMap(self, "ColorActions",
                {
                        "green": (self.save, _("Save and exit")),
                        "red": (self.cancel, _("Cancel")),
                        "yellow": (self.del_entry, _("delete shift entry")),
                        "blue": (self.new_entry, _("Make new entry")),
                })

                self.onLayoutFinish.append(self.load_list)
#
#                       "blue": (self.colors,_("Open color list")),

        def selectionChanged(self):
            if self["menu"].l.getCurrentSelection()[0][0] in schicht_colors:
                self["key_yellow"].show()
                self["pic_yellow"].show()
                self["key_blue"].show()
                self["pic_blue"].show()
            else:
                self["key_yellow"].hide()
                self["pic_yellow"].hide()
                self["pic_blue"].hide()
                self["key_blue"].hide()

        def load_list(self):
                liste = []
                liste.append((_("Programm-Daten"), None, "comment"))
                liste.append((_("Datum erster Turnus-Eintrag"), None, strftime("%d.%m.%Y", start_date.timetuple())))
                turnus_text = ','.join(turnus)  # .replace(","," ")
                liste.append((_("Schicht-Turnus"), None, turnus_text))
                liste.append((_("entferne Sonderdaten autom."), None, self.autodel_list[int(autodel)]))
                self.farb_start = 2
                liste.append((_("Programm-Farben"), None, "comment"))
                #prog_colors(datum-text,datum-farbe,heute-farbe,kopf-farbe,so-farbe,kal-bgr
                einstell_list = ("Text Datum", "Hintergrund Datum", "Hintergrund heute", "Kopfzeilen", "Sonntag", "Plan Hintergrund")
                # an/aus,lcd,screen,pos,size,breit,hoch,abstand,onidle
                for x in range(0, len(einstell_list)):
                      liste.append((einstell_list[x], self.color_list[x], "prog_col", x))
                liste.append((" ", None, "comment"))
                liste.append((_("Schicht-Farben"), None, "comment"))
                for key in schicht_colors:
                      liste.append((key, schicht_colors[key], "sch_col", None))

                if L4l:
                    # an/aus,lcd,screen,pos,size,breit,hoch,abstand,onidle
                    liste.append((" ", None, "comment"))
                    liste.append((_("l4l-Grafik"), None, "comment"))
                    liste.append((_("Show in LCD"), None, self.lcl_sets2[0], 0))
                    liste.append((_("LCD"), None, self.lcl_sets2[1], 1))
                    liste.append((_("Screen"), None, self.lcl_sets2[2], 2))
                    liste.append((_("Mode"), None, self.lcl_sets2[8], 8))
                    liste.append((_("Widht total"), None, self.lcl_sets2[5], 5))
                    liste.append((_("High total"), None, self.lcl_sets2[6], 6))
                    liste.append((_("Distance from top (pixel)"), None, self.lcl_sets2[3], 3))
                    liste.append((_("Distance from left (%)"), None, self.lcl_sets2[9], 9))
                    liste.append((_("Size for a single"), None, self.lcl_sets2[4], 4))
                    liste.append((_("distance between"), None, self.lcl_sets2[7], 7))
                self["menu"].buildList(liste, self.idx)
                #self["menu"].instance.moveSelectionTo(self.idx)
                #color_days,color_holiday,cal_background,color_event,extern_color,color_inactiv))

        def colors(self):
                self.session.openWithCallback(self.color_set, color_select)

        def color_set(self, answer=None):
                 if answer:
                     if self["menu"].l.getCurrentSelection()[0][2] == "prog_col":
                         self.color_list[self["menu"].l.getCurrentSelection()[0][3]] = answer.lstrip('#')
                         global prog_colors
                         prog_colors = self.color_list
                     self.load_list()

        def sch_col_set(self, answer=None):
                 if answer:
                     if self["menu"].l.getCurrentSelection()[0][2] == "sch_col":
                         global schicht_colors
                         schicht_colors[self["menu"].l.getCurrentSelection()[0][0]] = answer.lstrip('#')
                     self.load_list()

        def text(self):
           self.idx = self["menu"].l.getCurrentSelectionIndex()
           if self["menu"].l.getCurrentSelection()[0][2] != "comment":

             if self["menu"].l.getCurrentSelection()[0][0] == _("Datum erster Turnus-Eintrag"):
                text1 = self["menu"].l.getCurrentSelection()[0][2]
                self.session.openWithCallback(self.text_set, VirtualKeyBoard, title=_("Startdatum"), text=text1)

             elif self["menu"].l.getCurrentSelection()[0][0] == _("Schicht-Turnus"):
                text1 = self["menu"].l.getCurrentSelection()[0][2]
                self.session.openWithCallback(
                                        self.text_set,
                                        VKB_mod,
                                        title=_("Schicht-Turnus"),
                                        text=text1
                        )
             elif self["menu"].l.getCurrentSelection()[0][2] == "prog_col":
                self.session.openWithCallback(self.color_set, color_select, str(self["menu"].l.getCurrentSelection()[0][1]))
             elif self["menu"].l.getCurrentSelection()[0][2] == "sch_col":
                self.session.openWithCallback(self.sch_col_set, color_select, str(self["menu"].l.getCurrentSelection()[0][1]))

             elif self["menu"].l.getCurrentSelection()[0][0] == _("Show in LCD"):
                    self.session.openWithCallback(self.choice_back, ChoiceBox, title=_("Show on LCD"), list=((_("activate"), "On"), (_("deactivate"), "Off")))
             elif self["menu"].l.getCurrentSelection()[0][0] == _("entferne Sonderdaten autom."):
                    self.session.openWithCallback(self.choice_back, ChoiceBox, title=_("Auswahl Sonderdaten autom. entfernen"), list=(("nie", 0), ("voriges Jahr", 1)))
             elif self["menu"].l.getCurrentSelection()[0][0] == _("LCD"):
                    self.session.openWithCallback(self.choice_back, ChoiceBox, title=_("Select the LCD"), list=(("1", "LCD 1"), ("LCD 2", "2"), ("LCD 3", "3")))
             elif self["menu"].l.getCurrentSelection()[0][0] == _("Screen"):
                    self.session.openWithCallback(self.texteingabeFinished, InputBox, title=(_("Set number for screen")), text=self.lcl_sets2[2], maxSize=False, type=Input.NUMBER)
             elif self["menu"].l.getCurrentSelection()[0][0] == _("Mode"):
                    self.session.openWithCallback(self.choice_back, ChoiceBox, title=_("Select the Mode(s)"), list=(("On", "On"), ("Idle", "Idle"), ("Media", "Media"), ("On,Media", "On,Media"), ("Idle,Media", "Idle,Media"), ("On,Idle", "On,Idle"), ("On,Idle,Media", "On,Idle,Media")))
             elif self["menu"].l.getCurrentSelection()[0][0] == _("Widht total"):
                    self.session.openWithCallback(self.texteingabeFinished, InputBox, title=(_("Set Widht total")), text=self.lcl_sets2[5], maxSize=False, type=Input.NUMBER)
             elif self["menu"].l.getCurrentSelection()[0][0] == _("High total"):
                    self.session.openWithCallback(self.texteingabeFinished, InputBox, title=(_("Set High total")), text=self.lcl_sets2[4], maxSize=False, type=Input.NUMBER)
             elif self["menu"].l.getCurrentSelection()[0][0] == _("Distance from left (%)"):
                    self.session.openWithCallback(self.texteingabeFinished, InputBox, title=(_("Set Distance from left (%)")), text=self.lcl_sets2[9], maxSize=False, type=Input.NUMBER)
             elif self["menu"].l.getCurrentSelection()[0][0] == _("Distance from top (pixel)"):
                    self.session.openWithCallback(self.texteingabeFinished, InputBox, title=(_("Set Distance from top in pixel")), text=self.lcl_sets2[3], maxSize=False, type=Input.NUMBER)
             elif self["menu"].l.getCurrentSelection()[0][0] == _("Size for a single"):
                    self.session.openWithCallback(self.texteingabeFinished, InputBox, title=(_("Set Size for a single")), text=self.lcl_sets2[4], maxSize=False, type=Input.NUMBER)
             elif self["menu"].l.getCurrentSelection()[0][0] == _("distance between"):
                    self.session.openWithCallback(self.texteingabeFinished, InputBox, title=(_("Set distance between")), text=self.lcl_sets2[7], maxSize=False, type=Input.NUMBER)

        def choice_back(self, answer=None):
                if answer:
                       if self["menu"].l.getCurrentSelection()[0][0] == _("entferne Sonderdaten autom."):
                             global autodel
                             autodel = answer[1]
                       else:
                            self.lcl_sets2[self["menu"].l.getCurrentSelection()[0][3]] = answer[1]
                       self.load_list()

        def texteingabeFinished(self, answer=None):
                if answer:
                              self.lcl_sets2[self["menu"].l.getCurrentSelection()[0][3]] = answer
                              self.load_list()

        def text_set(self, answer=None):
                 if answer:
                     if self["menu"].l.getCurrentSelection()[0][0] == _("Datum erster Turnus-Eintrag"):
                         dats = answer.split(".")
                         try:
                              d2 = datetime.date(int(dats[2]), int(dats[1]), int(dats[0]))
                              global start_date
                              start_date = d2
                         except:
                             pass

                     elif self["menu"].l.getCurrentSelection()[0][0] == _("Schicht-Turnus"):
                         del_list = []
                         #answer=answer.strip()
                         global turnus
                         if answer.endswith(","):
                                answer = answer[:-1]
                         turnus = answer.split(",")
                         for x in turnus:
                            if not x in schicht_colors:
                                 schicht_colors[x] = "858585"

                     self.load_list()

        def del_entry(self):

                x = self["menu"].l.getCurrentSelection()[0][0]
                if not len(x.strip()):
                    if not " " in turnus and " " in schicht_colors:
                        del schicht_colors[" "]
                        self.load_list()
                elif not x.strip() in [x.strip() for x in turnus]:
                    del schicht_colors[x]
                    self.load_list()
                else:
                    self.session.open(MessageBox, "can not delete, entry in rota", type=MessageBox.TYPE_ERROR)

        def new_entry(self):
                self.session.openWithCallback(self.new_entry2, VKB_mod, title=_("New entry"), text="")

        def new_entry2(self, answer):
               if answer:
                   if not answer in schicht_colors:
                       schicht_colors[answer] = "858585"
                       self.load_list()
                   else:
                       self.session.open(MessageBox, "entry already exists", type=MessageBox.TYPE_ERROR)

        def save(self):
                #turnus.append(",")
                if L4l:
                    global l4l_sets
                    l4l_sets = self.lcl_sets2
                configparser2 = ConfigParser()
                if not fileExists('/etc/ConfFS/mspFS.conf'):
                    f = open("/etc/ConfFS/mspFS.conf", "w")
                    f.close()
                configparser2.read("/etc/ConfFS/mspFS.conf")
                if not configparser2.has_section("settings"):
                    configparser2.add_section("settings")
                configparser2.set("settings", "schicht_col", str(schicht_colors))
                configparser2.set("settings", "autodel", autodel)
                configparser2.set("settings", "prog_col", str(prog_colors))
                configparser2.set("settings", "turnus", ','.join(map(str, turnus)))  #str(turnus))
                configparser2.set("settings", "start_date", str(start_date))
                if L4l:
                    configparser2.set("settings", "l4l_sets", ':'.join(map(str, self.lcl_sets2)))
                fp = open("/etc/ConfFS/mspFS.conf", "w")
                configparser2.write(fp)
                if L4l:
                    from .paint import mspFS_paint
                    mspFS_paint(l4l_sets)
                self.close()

        def cancel(self):
                self.close()


class color_liste(MenuList):
    def __init__(self, list, enableWrapAround=False):
        MenuList.__init__(self, list, enableWrapAround, eListboxPythonMultiContent)
        self.l.setFont(0, gFont("Regular", 24))

    def postWidgetCreate(self, instance):
        MenuList.postWidgetCreate(self, instance)
        instance.setItemHeight(40)

    def buildList(self, listnew, s_color):
        list = []
        if s_color:
            s_color = int(s_color.lstrip('#'), 16)
        i = 0
        sel_index = 0
        for x in listnew:
            res = [x]
            color = int(x.lstrip('#'), 16)
            color2 = int("FFFFFF", 16)
            if s_color != None and s_color == color:
                sel_index = i
                res.append((eListboxPythonMultiContent.TYPE_TEXT, 0, 5, 140, 30, 0, RT_HALIGN_LEFT, "selected:", color, color))
                res.append((eListboxPythonMultiContent.TYPE_TEXT, 120, 5, 350, 30, 0, RT_HALIGN_LEFT, " ", color, color, color, color, 0, color))   #, color, color
            else:
                res.append((eListboxPythonMultiContent.TYPE_TEXT, 50, 5, 450, 30, 0, RT_HALIGN_LEFT, " ", color, color, color, color, 0, color))
                res.append((eListboxPythonMultiContent.TYPE_TEXT, 0, 5, 50, 30, 0, RT_HALIGN_LEFT, ">> ", color, color))
            res.append((eListboxPythonMultiContent.TYPE_TEXT, 510, 5, 50, 30, 0, RT_HALIGN_LEFT, " << ", color, color))
            list.append(res)
            i += 1
        self.l.setList(list)
        self.moveToIndex(sel_index)


class color_select(Screen):
        skin = """
                <screen position="center,center" size="600,380" title="Select Color" >
                        <widget name="menu" position="10,20" size="580,350" scrollbarMode="showOnDemand" />
                </screen>"""

        def __init__(self, session, color=None, args=None):
                Screen.__init__(self, session)
                self.session = session
                self.color = color
                self["menu"] = color_liste([])
                self["menu"].buildList(color_list, color)
                self.onLayoutFinish.append(self.move)

                self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
                {
                        "ok": self.keyOK,
                        "cancel": self.cancel,
                }, -1)

        def move(self):
               self["menu"].buildList(color_list, self.color)
               #self["menu"].moveToIndex(20)

        def keyOK(self):
                current = self["menu"].getCurrent()
                if current:
                        currentEntry = current[0]
                        self.close(currentEntry)

        def cancel(self):
                self.close(None)


class day_conf(Screen, ConfigListScreen, HelpableScreen):

        DWide = getDesktop(0).size().width()

        skin = """
                <screen position="center,center" size="600,480" title="Select Color" >
                        <widget name="config" position="10,5"  size="580,430" scrollbarMode="showOnDemand" />
                <ePixmap pixmap="skin_default/buttons/red.png" position="10,440" size="140,40" alphatest="on" />
                <ePixmap pixmap="skin_default/buttons/green.png" position="155,440" size="140,40"  alphatest="on" />

                <widget name="key_red" position="10,443" zPosition="1" size="140,35" valign="center" halign="center" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" noWrap="1" shadowOffset="-1,-1" />
                <widget name="key_green" position="155,443" zPosition="1" size="140,35" valign="center" halign="center" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" noWrap="1" shadowOffset="-1,-1" />

                </screen>"""

        def __init__(self, session):

                self.color_list = list(prog_colors)

                Screen.__init__(self, session)
                HelpableScreen.__init__(self)
                self.setTitle(_("Extra-Setting for dat"))
                self.sch_list = [(_("Set Standard"), _("Set Standard"))]
                for k in schicht_colors:
                    self.sch_list.append((k, k))
                self.sch_list.append((_("New entry"), _("New entry")))

                self.schichten = NoSave(ConfigSelection(choices=self.sch_list, default=_("Set Standard")))
                self.start = NoSave(ConfigDateTime(mktime(selected.timetuple()), _("%A, %d.%m %Y"), increment=86400))
                self.end = NoSave(ConfigDateTime(mktime(selected.timetuple()), _("%A, %d.%m %Y"), increment=86400))
                self.new_descr = NoSave(ConfigText(default=selected_schicht, visible_width=50, fixed_size=False))
                self.new_col = "858585"
                self.new_col_fake = NoSave(ConfigNothing())
                self.liste = []

                ConfigListScreen.__init__(self, self.liste, on_change=self.reloadList)   #858585

                self["key_green"] = Label(_("Save"))
                self["key_red"] = Label(_("Cancel"))

                self["actions"] = ActionMap(["SetupActions"],
                        {
                                "cancel": self.cancel,
                                "ok": self.text,
                        }, -2
                )

                self["ColorActions"] = HelpableActionMap(self, "ColorActions",
                {
                        "green": (self.save, _("Save and exit")),
                        "red": (self.cancel, _("Cancel")),
                })
                self.reloadList()

        def reloadList(self):
                  self.load_list()
                  self["config"].setList(self.liste)

        def load_list(self):
                liste = []
                liste.extend((
                    getConfigListEntry(_("Start-Date"), self.start),
                    getConfigListEntry(_("End-Date"), self.end),
                    getConfigListEntry(_("Entry"), self.schichten),
                    ))
                if self.schichten.value == _("New entry"):
                  liste.extend((
                    getConfigListEntry(_("New description"), self.new_descr),
                    getConfigListEntry(_("Color for new entry:") + self.new_col, self.new_col_fake),
                    ))
                self.liste = liste

        def colors(self):
                self.session.openWithCallback(self.color_set, color_select)

        def color_set(self, answer=None):
                 if answer:
                      global schicht_colors
                      schicht_colors[self.schichten.value] = answer.lstrip('#')
                      self.reloadList()
#

        def text(self):
            if self["config"].getCurrent() == self.new_col_fake:
                 self.session.openWithCallback(self.color_set, color_select)
            elif self["config"].getCurrent()[0] == _("Entry"):
                 self.session.openWithCallback(self.text_set, ChoiceBox, title=_("Select entry"), list=self.sch_list)
            elif self["config"].getCurrent()[0] == _("New description"):
                 self.session.openWithCallback(self.text_set, VirtualKeyBoard, title=_("New description"), text="")
            elif self["config"].getCurrent()[0] == _("Start-Date"):
                 dx = datetime.datetime.fromtimestamp(int(self.start.value)).strftime('%d.%m.%Y')
                 self.session.openWithCallback(self.text_set, VirtualKeyBoard, title=_("Set Start-Date"), text=dx)
            elif self["config"].getCurrent()[0] == _("End-Date"):
                 dx = datetime.datetime.fromtimestamp(int(self.end.value)).strftime('%d.%m.%Y')
                 self.session.openWithCallback(self.text_set, VirtualKeyBoard, title=_("Set End-Date"), text=dx)

        def text_set(self, answer=None):
                 if answer:
                     if self["config"].getCurrent()[0] == _("New description"):
                         if not answer in schicht_colors:
                                 self.new_descr.value = answer
                                 self.sch_list.append(answer)
                                 self.schichten.value = answer
                                 self.colors()
                         else:
                             pass
                     elif self["config"].getCurrent()[0] == _("Start-Date"):
                        self.dx = mktime(strptime(answer, "%d.%m.%Y"))
                        self.start.value = self.dx
                        if self.end.value < self.start.value:
                             self.end.value = self.start.value
                     elif self["config"].getCurrent()[0] == _("End-Date"):
                        self.dx2 = mktime(strptime(answer, "%d.%m.%Y"))
                        self.end.value = self.dx2
                     elif self["config"].getCurrent()[0] == _("Entry"):
                        self.schichten.value = answer[1]
                     self.reloadList()

        def save(self):
                starter = datetime.date.fromtimestamp(self.start.value)
                ender = datetime.date.fromtimestamp(self.end.value)
                diff = (ender - starter).days
                text = self.schichten.value
                for i in range(diff + 1):
                    write_date = str(starter).replace("-", "")
                    global sonders
                    if text == _("Set Standard"):
                        del sonders[write_date]
                    else:
                        sonders[write_date] = text
                    starter = starter + datetime.timedelta(1)
                configparser2 = ConfigParser()
                if not fileExists('/etc/ConfFS/mspFS.conf'):
                    f = open("/etc/ConfFS/mspFS.conf", "w")
                    f.close()
                configparser2.read("/etc/ConfFS/mspFS.conf")
                if not configparser2.has_section("settings"):
                    configparser2.add_section("settings")
                configparser2.set("settings", "sonders", str(sonders))
                configparser2.set("settings", "schicht_col", str(schicht_colors))
                fp = open("/etc/ConfFS/mspFS.conf", "w")
                configparser2.write(fp)
                fp.close()
                from .paint import mspFS_paint
                mspFS_paint()
                self.close()

        def cancel(self):
                self.close()

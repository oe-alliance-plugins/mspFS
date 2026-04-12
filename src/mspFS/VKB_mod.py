from . import _
# -*- coding: UTF-8 -*-
from enigma import eListboxPythonMultiContent, gFont, RT_HALIGN_CENTER, RT_VALIGN_CENTER, getPrevAsciiCode
#from Screen import Screen
from Screens.Screen import Screen
from Screens.HelpMenu import HelpableScreen
from Components.Language import language
from Components.ActionMap import ActionMap, HelpableActionMap
from Components.Sources.StaticText import StaticText
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Tools.Directories import resolveFilename, SCOPE_CURRENT_SKIN
from Tools.LoadPixmap import LoadPixmap

image_folder = "/usr/lib/enigma2/python/Plugins/Extensions/mspFS/vkb_mod_image/"


class VKB_modList(MenuList):
        def __init__(self, list, enableWrapAround=False):
                MenuList.__init__(self, list, enableWrapAround, eListboxPythonMultiContent)
                self.l.setFont(0, gFont("Regular", 28))
                self.l.setItemHeight(45)


def VKB_modEntryComponent(keys, selectedKey, shiftMode=False):
        vkb_backspace = LoadPixmap(cached=True, path=image_folder + "vkb_backspace.png")
        vkb_bg = LoadPixmap(cached=True, path=image_folder + "vkb_bg.png")
        vkb_clr = LoadPixmap(cached=True, path=image_folder + "vkb_clr.png")
        vkb_esc = LoadPixmap(cached=True, path=image_folder + "vkb_esc.png")
        vkb_ok = LoadPixmap(cached=True, path=image_folder + "vkb_ok.png")
        vkb_sel = LoadPixmap(cached=True, path=image_folder + "vkb_sel.png")
        vkb_shift = LoadPixmap(cached=True, path=image_folder + "vkb_shift.png")
        vkb_shift_sel = LoadPixmap(cached=True, path=image_folder + "vkb_shift_sel.png")
        vkb_space = LoadPixmap(cached=True, path=image_folder + "vkb_space.png")
        vkb_left = LoadPixmap(cached=True, path=image_folder + "vkb_left.png")
        vkb_right = LoadPixmap(cached=True, path=image_folder + "vkb_right.png")
        vkb_nix = LoadPixmap(cached=True, path=image_folder + "vkb_nix.png")
        res = [(keys)]

        x = 0
        count = 0
        if shiftMode:
                shiftkey_png = vkb_shift_sel
        else:
                shiftkey_png = vkb_shift
        for key in keys:
                width = None
                if key == "EXIT":
                        width = vkb_esc.size().width()
                        res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 45), png=vkb_esc))
                elif key == "BACKSPACE":
                        width = vkb_backspace.size().width()
                        res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 45), png=vkb_backspace))
                elif key == "CLEAR":
                        width = vkb_clr.size().width()
                        res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 45), png=vkb_clr))
                elif key == "SHIFT":
                        width = shiftkey_png.size().width()
                        res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 45), png=shiftkey_png))
                elif key == "SPACE":
                        width = vkb_space.size().width()
                        res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 45), png=vkb_space))
                elif key == "OK":
                        width = vkb_ok.size().width()
                        res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 45), png=vkb_ok))
                elif key == "REWIND":
                        width = vkb_left.size().width()
                        res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 45), png=vkb_left))
                elif key == "FORWARD":
                        width = vkb_right.size().width()
                        res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 45), png=vkb_right))
                elif key == "nix":
                        width = vkb_nix.size().width()
                        res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 45), png=vkb_nix))

                else:
                        width = vkb_bg.size().width()
                        res.extend((
                                MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 45), png=vkb_bg),
                                MultiContentEntryText(pos=(x, 0), size=(width, 45), font=0, text=key, flags=RT_HALIGN_CENTER | RT_VALIGN_CENTER)
                        ))

                if selectedKey == count:
                        width = vkb_sel.size().width()
                        res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 45), png=vkb_sel))

                if width is not None:
                        x += width
                else:
                        x += 45
                count += 1

        return res

#right    noWrap="0"


class VKB_mod(Screen, HelpableScreen):
        skin = """
                <screen name="VKB_mod" position="center,center" size="640,420" zPosition="99" backgroundColor="#000000" title="mspFS-VKB_mod">
                <widget name="text" position="12,10" size="620,110" font="Regular;30" transparent="0"  backgroundColor="#000000" halign="left" valign="top" />
                <widget name="list" position="10,130" size="630,305" selectionDisabled="1" backgroundColor="#000000" transparent="0" />
                <widget name="help" position="10,380" zPosition="2" size="620,40" font="Regular;20" foregroundColor="#FFFFFF" transparent="1" />

        </screen>"""

        def __init__(self, session, title="mspFS-VKB_mod", text=""):
                Screen.__init__(self, session)
                self["help"] = Label(_("trenne mit Komma - Beispiel: F,F,N,N,N,S,S,fr,fr"))
                self.keys_list = []
                self.shiftkeys_list = []
                self.lang = language.getLanguage()
                self.nextLang = None
                self.shiftMode = False
                self.text = text + "|"
                self.selectedKey = 0
                self.currPos = len(self.text) - 1     #neu
                self.setTitle(title)
                self["country"] = StaticText("")
                self["header"] = Label(title)
                self["text"] = Label(self.text)
                self["list"] = VKB_modList([])

                self["actions"] = ActionMap(["OkCancelActions", "WizardActions", "InputBoxActions", "InputAsciiActions"],
                        {
                                "gotAsciiCode": self.keyGotAscii,
                                "ok": self.okClicked,
                                "cancel": self.exit,
                                "left": self.left,
                                "right": self.right,
                                "up": self.up,
                                "down": self.down,
                                "back": self.exit,
                        }, -2)

                self["MediaPlayerSeekActions"] = HelpableActionMap(self, "MediaPlayerSeekActions",
                        {
                                "seekBack": (self.jumpLeft, _("Cursor jump left")),
                                "seekFwd": (self.jumpRight, _("Cursor jump right")),
                        }, -1)

                self["MediaPlayerActions"] = HelpableActionMap(self, "MediaPlayerActions",
                        {
                                "previous": (self.goLeft, _("Cursor left")),
                                "next": (self.goRight, _("Cursor right")),

                        }, -1)

                self["ColorActions"] = HelpableActionMap(self, "ColorActions",
                        {
                                "red": (self.backClicked, _("Delete left from cursor")),
                                "green": (self.ok, _("Save and exit")),
                                "yellow": (self.switchLang, _("Toggle Language")),
                                "blue": (self.shiftPressed, _("Shift")),
                        }, -1)

                self.setLang()
                HelpableScreen.__init__(self)
                #self.onExecBegin.append(self.setKeyboardModeAscii)
                self.onLayoutFinish.append(self.buildVKB_mod)

        def switchLang(self):
                self.lang = self.nextLang
                self.setLang()
                self.buildVKB_mod()

        def setLang(self):
                if self.lang == 'de_DE':
                        self.keys_list = [
                                [u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"0", u"ß", u"BACKSPACE", "nix", u"OK"],
                                [u"q", u"w", u"e", u"r", u"t", u"z", u"u", u"i", u"o", u"p", u"ü", u"+", "nix", "nix"],
                                [u"a", u"s", u"d", u"f", u"g", u"h", u"j", u"k", u"l", u"ö", u"ä", u"#", "nix", u"REWIND"],
                                [u"<", u"y", u"x", u"c", u"v", u"b", u"n", u"m", u",", ".", u"-", u"CLEAR", "nix", u"FORWARD"],
                                [u"SHIFT", u"SPACE", u"_", u"@", u"EXIT"]]
                        self.shiftkeys_list = [
                                [u"\\", u"!", u'"', u"§", u"$", u"%", u"&", u"/", u"(", u")", u"=", u"BACKSPACE", "nix", u"OK"],
                                [u"Q", u"W", u"E", u"R", u"T", u"Z", u"U", u"I", u"O", u"P", u"Ü", u"*", "nix", "nix"],
                                [u"A", u"S", u"D", u"F", u"G", u"H", u"J", u"K", u"L", u"Ö", u"Ä", u"'", "nix", u"REWIND"],
                                [u">", u"Y", u"X", u"C", u"V", u"B", u"N", u"M", u";", u":", u"_", u"CLEAR", "nix", u"FORWARD"],
                                [u"SHIFT", u"SPACE", u"?", u"EXIT"]]
                        self.nextLang = 'es_ES'
                elif self.lang == 'es_ES':
                        #still missing keys (u"ùÙ")
                        self.keys_list = [
                                [u"EXIT", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"0", u"BACKSPACE"],
                                [u"q", u"w", u"e", u"r", u"t", u"z", u"u", u"i", u"o", u"p", u"ú", u"+"],
                                [u"a", u"s", u"d", u"f", u"g", u"h", u"j", u"k", u"l", u"ó", u"á", u"#"],
                                [u"<", u"y", u"x", u"c", u"v", u"b", u"n", u"m", u",", ".", u"-", u"CLEAR"],
                                [u"SHIFT", u"SPACE", u"@", u"Ł", u"ŕ", u"é", u"č", u"í", u"ě", u"ń", u"ň", u"OK"],
                                [u"REWIND", u"FORWARD"]]
                        self.shiftkeys_list = [
                                [u"EXIT", u"!", u'"', u"§", u"$", u"%", u"&", u"/", u"(", u")", u"=", u"BACKSPACE"],
                                [u"Q", u"W", u"E", u"R", u"T", u"Z", u"U", u"I", u"O", u"P", u"Ú", u"*"],
                                [u"A", u"S", u"D", u"F", u"G", u"H", u"J", u"K", u"L", u"Ó", u"Á", u"'"],
                                [u">", u"Y", u"X", u"C", u"V", u"B", u"N", u"M", u";", u":", u"_", u"CLEAR"],
                                [u"SHIFT", u"SPACE", u"?", u"\\", u"Ŕ", u"É", u"Č", u"Í", u"Ě", u"Ń", u"Ň", u"OK"],
                                [u"REWIND", u"FORWARD"]]
                        self.nextLang = 'fi_FI'
                elif self.lang == 'fi_FI':
                        self.keys_list = [
                                [u"EXIT", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"0", u"BACKSPACE"],
                                [u"q", u"w", u"e", u"r", u"t", u"z", u"u", u"i", u"o", u"p", u"é", u"+"],
                                [u"a", u"s", u"d", u"f", u"g", u"h", u"j", u"k", u"l", u"ö", u"ä", u"#"],
                                [u"<", u"y", u"x", u"c", u"v", u"b", u"n", u"m", u",", ".", u"-", u"CLEAR"],
                                [u"SHIFT", u"SPACE", u"@", u"ß", u"ĺ", u"REWIND", u"FORWARD", u"OK"]]
                        self.shiftkeys_list = [
                                [u"EXIT", u"!", u'"', u"§", u"$", u"%", u"&", u"/", u"(", u")", u"=", u"BACKSPACE"],
                                [u"Q", u"W", u"E", u"R", u"T", u"Z", u"U", u"I", u"O", u"P", u"É", u"*"],
                                [u"A", u"S", u"D", u"F", u"G", u"H", u"J", u"K", u"L", u"Ö", u"Ä", u"'"],
                                [u">", u"Y", u"X", u"C", u"V", u"B", u"N", u"M", u";", u":", u"_", u"CLEAR"],
                                [u"SHIFT", u"SPACE", u"?", u"\\", u"Ĺ", u"REWIND", u"FORWARD", u"OK"]]
                        self.nextLang = 'sv_SE'
                elif self.lang == 'sv_SE':
                        self.keys_list = [
                                [u"EXIT", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"0", u"BACKSPACE"],
                                [u"q", u"w", u"e", u"r", u"t", u"z", u"u", u"i", u"o", u"p", u"é", u"+"],
                                [u"a", u"s", u"d", u"f", u"g", u"h", u"j", u"k", u"l", u"ö", u"ä", u"#"],
                                [u"<", u"y", u"x", u"c", u"v", u"b", u"n", u"m", u",", ".", u"-", u"CLEAR"],
                                [u"SHIFT", u"SPACE", u"@", u"ß", u"ĺ", u"REWIND", u"FORWARD", u"OK"]]
                        self.shiftkeys_list = [
                                [u"EXIT", u"!", u'"', u"§", u"$", u"%", u"&", u"/", u"(", u")", u"=", u"BACKSPACE"],
                                [u"Q", u"W", u"E", u"R", u"T", u"Z", u"U", u"I", u"O", u"P", u"É", u"*"],
                                [u"A", u"S", u"D", u"F", u"G", u"H", u"J", u"K", u"L", u"Ö", u"Ä", u"'"],
                                [u">", u"Y", u"X", u"C", u"V", u"B", u"N", u"M", u";", u":", u"_", u"CLEAR"],
                                [u"SHIFT", u"SPACE", u"?", u"\\", u"Ĺ", u"REWIND", u"FORWARD", u"OK"]]
                        self.nextLang = 'sk_SK'
                elif self.lang == 'sk_SK':
                        self.keys_list = [
                                [u"EXIT", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"0", u"BACKSPACE"],
                                [u"q", u"w", u"e", u"r", u"t", u"z", u"u", u"i", u"o", u"p", u"ú", u"+"],
                                [u"a", u"s", u"d", u"f", u"g", u"h", u"j", u"k", u"l", u"ľ", u"@", u"#"],
                                [u"<", u"y", u"x", u"c", u"v", u"b", u"n", u"m", u",", ".", u"-", u"CLEAR"],
                                [u"SHIFT", u"SPACE", u"š", u"č", u"ž", u"ý", u"á", u"í", u"é", u"REWIND", u"FORWARD", u"OK"]]
                        self.shiftkeys_list = [
                                [u"EXIT", u"!", u'"', u"§", u"$", u"%", u"&", u"/", u"(", u")", u"=", u"BACKSPACE"],
                                [u"Q", u"W", u"E", u"R", u"T", u"Z", u"U", u"I", u"O", u"P", u"ť", u"*"],
                                [u"A", u"S", u"D", u"F", u"G", u"H", u"J", u"K", u"L", u"ň", u"ď", u"'"],
                                [u"Á", u"É", u"Ď", u"Í", u"Ý", u"Ó", u"Ú", u"Ž", u"Š", u"Č", u"Ť", u"Ň"],
                                [u">", u"Y", u"X", u"C", u"V", u"B", u"N", u"M", u";", u":", u"_", u"CLEAR"],
                                [u"SHIFT", u"SPACE", u"?", u"\\", u"ä", u"ö", u"ü", u"ô", u"ŕ", u"ĺ", u"REWIND", u"FORWARD"],
                                [u"OK"]]
                        self.nextLang = 'cs_CZ'
                elif self.lang == 'cs_CZ':
                        self.keys_list = [
                                [u"EXIT", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"0", u"BACKSPACE"],
                                [u"q", u"w", u"e", u"r", u"t", u"z", u"u", u"i", u"o", u"p", u"ú", u"+"],
                                [u"a", u"s", u"d", u"f", u"g", u"h", u"j", u"k", u"l", u"ů", u"@", u"#"],
                                [u"<", u"y", u"x", u"c", u"v", u"b", u"n", u"m", u",", ".", u"-", u"CLEAR"],
                                [u"SHIFT", u"SPACE", u"ě", u"š", u"č", u"ř", u"ž", u"ý", u"á", u"í", u"REWIND", u"FORWARD"],
                                [u"OK"]]
                        self.shiftkeys_list = [
                                [u"EXIT", u"!", u'"', u"§", u"$", u"%", u"&", u"/", u"(", u")", u"=", u"BACKSPACE"],
                                [u"Q", u"W", u"E", u"R", u"T", u"Z", u"U", u"I", u"O", u"P", u"ť", u"*"],
                                [u"A", u"S", u"D", u"F", u"G", u"H", u"J", u"K", u"L", u"ň", u"ď", u"'"],
                                [u">", u"Y", u"X", u"C", u"V", u"B", u"N", u"M", u";", u":", u"_", u"CLEAR"],
                                [u"SHIFT", u"SPACE", u"?", u"\\", u"Č", u"Ř", u"Š", u"Ž", u"Ú", u"Á", u"É", u"REWIND", u"FORWARD"],
                                [u"OK"]]
                        self.nextLang = 'en_EN'
                else:
                        self.keys_list = [
                                [u"EXIT", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"0", u"BACKSPACE"],
                                [u"q", u"w", u"e", u"r", u"t", u"z", u"u", u"i", u"o", u"p", u"+", u"@"],
                                [u"a", u"s", u"d", u"f", u"g", u"h", u"j", u"k", u"l", u"#", u"\\", u"|"],
                                [u"<", u"y", u"x", u"c", u"v", u"b", u"n", u"m", u",", ".", u"-", u"CLEAR"],
                                [u"SHIFT", u"SPACE", u"REWIND", u"FORWARD", u"OK"]]
                        self.shiftkeys_list = [
                                [u"EXIT", u"!", u'"', u"§", u"$", u"%", u"&", u"/", u"(", u")", u"=", u"BACKSPACE"],
                                [u"Q", u"W", u"E", u"R", u"T", u"Z", u"U", u"I", u"O", u"P", u"*", u"["],
                                [u"A", u"S", u"D", u"F", u"G", u"H", u"J", u"K", u"L", u"'", u"?", u"]"],
                                [u">", u"Y", u"X", u"C", u"V", u"B", u"N", u"M", u";", u":", u"_", u"CLEAR"],
                                [u"SHIFT", u"SPACE", u"REWIND", u"FORWARD", u"OK"]]
                        self.lang = 'en_EN'
                        self.nextLang = 'de_DE'
                self["country"].setText(self.lang)
                k_len = len(self.keys_list)
                self.z_len = len(self.keys_list[0])
                self.max_key = ((k_len - 1) * self.z_len) + len(self.keys_list[k_len - 1]) - 1
                #self.max_key=61+len(self.keys_list[5])

        def buildVKB_mod(self, selectedKey=0):
                list = []

                if self.shiftMode:
                        self.k_list = self.shiftkeys_list
                        for keys in self.k_list:
                                keyslen = len(keys)
                                if selectedKey < keyslen and selectedKey > -1:
                                        list.append(VKB_modEntryComponent(keys, selectedKey, True))
                                else:
                                        list.append(VKB_modEntryComponent(keys, -1, True))
                                selectedKey -= keyslen
                else:
                        self.k_list = self.keys_list
                        for keys in self.k_list:
                                keyslen = len(keys)
                                if selectedKey < keyslen and selectedKey > -1:
                                        list.append(VKB_modEntryComponent(keys, selectedKey))
                                else:
                                        list.append(VKB_modEntryComponent(keys, -1))
                                selectedKey -= keyslen
                k_len = len(self.k_list)
                self.max_key = ((k_len - 1) * self.z_len) + len(self.k_list[k_len - 1]) - 1
                self["list"].setList(list)

        def shiftPressed(self):
                if self.shiftMode:
                        self.shiftMode = False
                else:
                        self.shiftMode = True
                self.buildVKB_mod(self.selectedKey)

#### funktion gehe links/rechts und text neu setzen ##########
        def goLeft(self):
                if self.currPos > 0:
                        self.text = self.text[0:self.currPos] + self.text[self.currPos + 1:]
                        self.currPos -= 1
                        self.text = self.text[0:self.currPos] + "|" + self.text[self.currPos:]
                        self["text"].setText(self.text)

        def goRight(self):
                if self.currPos < len(self.text) - 1:
                        self.text = self.text[0:self.currPos] + self.text[self.currPos + 1:]
                        self.currPos += 1
                        self.text = self.text[0:self.currPos] + "|" + self.text[self.currPos:]
                        self["text"].setText(self.text)

        def jumpLeft(self):
                if self.currPos > 0:
                        self.text = self.text[0:self.currPos] + self.text[self.currPos + 1:]
                        self.currPos = 0
                        self.text = "|" + self.text
                        self["text"].setText(self.text)

        def jumpRight(self):
                if self.currPos < len(self.text) - 1:
                        self.text = self.text[0:self.currPos] + self.text[self.currPos + 1:]
                        self.currPos = len(self.text)
                        self.text = self.text + "|"
                        self["text"].setText(self.text)

        def setTextNew(self, text=None, set=None):
                if text:
                        if self.currPos == len(self.text) - 1:
                                self.text = self.text[:-1] + text + "|"
                        elif self.currPos == 0:
                                self.text = text + self.text  # [2:]
                        else:
                                self.text = self.text[0:self.currPos] + text + self.text[self.currPos:]
                        self.currPos += 1

                elif set == "del":
                        if len(self.text):
                                if self.currPos == 0:
                                        pass
                                else:
                                        if self.currPos == len(self.text) - 1:
                                                self.text = self.text[:-2] + "|"
                                        else:
                                                self.text = self.text[0:self.currPos - 1] + self.text[self.currPos:]
                                self.currPos -= 1
                elif set == "del2":
                        if len(self.text):
                                if self.currPos == len(self.text) - 1:
                                        pass
                                else:
                                        if self.currPos == 0:
                                                self.text = "|" + self.text[2:]
                                        else:
                                                self.text = self.text[0:self.currPos + 1] + self.text[self.currPos + 2:]
                                        self.currPos -= 1
                self["text"].setText(self.text)
#### ende  funktion gehe links/rechts ############

        def backClicked(self):
                self.setTextNew(None, "del")

        def backSpace(self):
                self.setTextNew(None, "del2")

        def okClicked(self):
                if self.shiftMode:
                        list = self.shiftkeys_list
                else:
                        list = self.keys_list

                selectedKey = self.selectedKey

                text = None

                for x in list:
                        xlen = len(x)
                        if selectedKey < xlen:
                                if selectedKey < len(x):
                                        text = x[selectedKey]
                                break
                        else:
                                selectedKey -= xlen

                if text is None:
                        return

                text = text.encode("UTF-8")

                if text == "EXIT":
                        self.close(None)

                elif text == "BACKSPACE":
                        self.setTextNew(None, "del")
                elif text == "ADD":
                        self.backSpace()
                elif text == "CLEAR":
                        self.currPos == 0
                        self.text = "|"
                        self["text"].setText(self.text)
### tasten in tastenliste
                elif text == "REWIND":
                        self.goLeft()
                elif text == "FORWARD":
                        self.goRight()

                elif text == "SHIFT":
                        if self.shiftMode:
                                self.shiftMode = False
                        else:
                                self.shiftMode = True

                        self.buildVKB_mod(self.selectedKey)

                elif text == "SPACE":
                        self.setTextNew(" ", "add")

                elif text == "OK":
                        if self.currPos == 0:
                                self.text = self.text[1:]
                        else:
                                self.text = self.text[0:self.currPos] + self.text[self.currPos + 1:]
                        self.close(self.text)

                else:
                        self.setTextNew(text, "add")

        def ok(self):
                if "|" in self.text:
                        if self.currPos == 0:
                                self.text = self.text[1:]
                        else:
                                self.text = self.text[0:self.currPos] + self.text[self.currPos + 1:]
                        self.close(self.text)

        def exit(self):
                self.close(None)

        def left(self):
                self.selectedKey -= 1
                if self.selectedKey == -1:
                        self.selectedKey = self.z_len - 1
                elif (self.selectedKey + 1) % self.z_len == 0:
                        self.selectedKey = self.selectedKey + self.z_len
                if self.selectedKey > self.max_key:
                        self.selectedKey = self.max_key
                self.showActiveKey()

        def right(self):
                self.selectedKey += 1
                if (self.selectedKey) % self.z_len == 0:
                        self.selectedKey = self.selectedKey - self.z_len
                elif self.selectedKey > self.max_key:
                        self.selectedKey = self.selectedKey - (self.selectedKey) % self.z_len
                self.showActiveKey()

        def up(self):
                self.selectedKey -= self.z_len
                if self.selectedKey < 0:
                        self.selectedKey += (1 + int(self.max_key / self.z_len)) * self.z_len
                if self.selectedKey > self.max_key:
                        self.selectedKey -= self.z_len
                self.showActiveKey()

        def down(self):
                self.selectedKey += self.z_len
                if self.selectedKey > self.max_key:
                        self.selectedKey = self.selectedKey - (self.z_len * int(self.selectedKey / self.z_len))
                if self.selectedKey < 0:
                        self.selectedKey = 0
                self.showActiveKey()

        def showActiveKey(self):
                self.buildVKB_mod(self.selectedKey)

        def inShiftKeyList(self, key):
                for KeyList in self.shiftkeys_list:
                        for char in KeyList:
                                if char == key:
                                        return True
                return False

        def keyGotAscii(self):
                #char = str(unichr(getPrevAsciiCode()).encode('utf-8'))
                from Components.config import getCharValue
                char = getCharValue(getPrevAsciiCode())
                if self.inShiftKeyList(char):
                        self.shiftMode = True
                        list = self.shiftkeys_list
                else:
                        self.shiftMode = False
                        list = self.keys_list

                if char == " ":
                        char = "SPACE"

                selkey = 0
                for keylist in list:
                        for key in keylist:
                                if key == char:
                                        self.selectedKey = selkey
                                        self.okClicked()
                                        self.showActiveKey()
                                        return
                                else:
                                        selkey += 1

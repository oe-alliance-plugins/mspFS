# -*- coding: utf-8 -*-
###############################################################################
from configparser import ConfigParser
import datetime
from Tools.Directories import fileExists
import os
import shutil


picon_path = "/usr/lib/enigma2/python/Plugins/Extensions/mspFS/picons"


configparser = ConfigParser()

try:
    from Plugins.Extensions.LCD4linux.module import L4Lelement
    #configparser = ConfigParser()
    configparser.read("/etc/ConfFS/mspFS.conf")
    if configparser.has_option("settings", "l4l_sets"):
        l4l_sets = configparser.get("settings", "l4l_sets").split(":")
    else:
        l4l_sets = ("On", "1", "1", "0", "60", "100", "500", "10", "On", "0")
    L4Lmspfs = L4Lelement()
    l4l = True
except Exception:
    l4l = None

#heute=datetime.date.today()


class mspFS_paint:
  def __init__(self, sets=None):

    global l4l_sets

    try:

        configparser.read("/etc/ConfFS/mspFS.conf")

        self.schichten = configparser.get("settings", "turnus").split(",")
        self.schicht_colors = eval(configparser.get("settings", "schicht_col"))
        if configparser.has_option("settings", "sonders"):
            self.sonders = eval(configparser.get("settings", "sonders"))
        else:
            self.sonders = {}
        if configparser.has_option("settings", "start_date"):
            dx = configparser.get("settings", "start_date").split("-")
            self.start_date = datetime.date(int(dx[0]), int(dx[1]), int(dx[2]))
        else:
            self.start_date = datetime.date.today().replace(month=1, day=1)
    except Exception:
        self.schichten = None
    if l4l:
     if self.schichten and l4l_sets[0] == "On":
      count = 0
      if sets:
         l4l_sets = sets
      sch_len = len(self.schichten)  # -1
      try:
         os.remove("/tmp/mspFS1.png")
         os.remove("/tmp/mspFS2.png")
      except OSError:
         pass

      try:
          heute = datetime.date.today()
          s_dat = heute
          tage = heute - self.start_date
          tage = tage.days + 1  # +6
          mySchicht = []
          tg1 = tage
          for count in range(20):
              if tg1 > sch_len:
                tg1 = tg1 % sch_len

              if str(s_dat).replace("-", "") in self.sonders:
                  schicht = self.sonders[str(s_dat).replace("-", "")]
              else:
                  schicht = self.schichten[tg1 - 1].strip()
              if os.path.exists(picon_path):
                if count == 0:
                   if fileExists(os.path.join(picon_path, schicht + ".png")):
                        ret = shutil.copyfile(os.path.join(picon_path, schicht + ".png"), "/tmp/mspFS1.png")
                   else:
                        ret = shutil.copyfile(os.path.join(picon_path, 'err.png'), "/tmp/mspFS1.png")  # noqa F841

                elif count == 1:
                   if fileExists(os.path.join(picon_path, schicht + ".png")):
                       ret = shutil.copyfile(os.path.join(picon_path, schicht + ".png"), "/tmp/mspFS2.png")
                   else:
                       ret = shutil.copyfile(os.path.join(picon_path, 'err.png'), "/tmp/mspFS1.png")  # noqa F841
              mySchicht.append(schicht)
              tg1 += 1
              s_dat = s_dat + datetime.timedelta(1)
          if l4l and l4l_sets[0] == "On" and len(mySchicht):
                  self.paint_l4l(mySchicht)
      except Exception as e:
            f = open("/tmp/schichten", "a")
            f.write("error\n" + str(e) + "\n")
            f.close()


#############################################################################
#####################################################################################


  def paint_l4l(self, mySchicht):
     from PIL import Image
     from PIL import ImageFont
     from PIL import ImageDraw
     #("1","1","1","0","80","500","100","10","OnIdle")
     size = int(l4l_sets[4])  # 60
     breit = int(l4l_sets[5])  # 100  #from config
     hoch = int(l4l_sets[6])  # 600   #from config
     abstand = int(l4l_sets[7])  # 10  #from config
     top = str(l4l_sets[3])  # +"%"#10
     if len(l4l_sets) == 9:
         left = "0%"
     else:
        left = str(l4l_sets[9]) + "%"
     #pos="40"     #from config
     if breit > hoch:
         quer = 1
         anz = int(breit / (size + abstand))
         if anz > len(mySchicht) - 1:
             size = int(breit - (len(mySchicht) - 1) * abstand / (len(mySchicht) - 1))
         hoch = size + abstand * 2

     else:
         quer = 0
         anz = int(hoch / (size + abstand))
         if anz > len(mySchicht) - 1:
             size = int(hoch - (len(mySchicht) - 1) * abstand / (len(mySchicht) - 1))
         breit = size + abstand * 2

      # Init 80% Normalgr��e
     im = Image.new('RGBA', (breit, hoch), (0, 0, 0, 0))
     draw = ImageDraw.Draw(im)
     px = abstand
     py = abstand
     for i in range(anz):
        col = self.schicht_colors[mySchicht[i]].lstrip('#')
        lv = len(col)
        txt = mySchicht[i]
        TextSize = int(size * 0.8)
        font = ImageFont.truetype("/usr/share/fonts/nmsbd.ttf", TextSize, encoding='unic')
        w, h = draw.textsize(txt, font=font)
        while w > int(size * 0.95):  # max 90% solange verkleinern
                TextSize -= 1
                font = ImageFont.truetype("/usr/share/fonts/nmsbd.ttf", TextSize, encoding='unic')
                w, h = draw.textsize(txt, font=font)
        colx = tuple(int(col[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))  # col from hex
        col2 = (colx[0], colx[1], colx[2], 0)
        draw.ellipse((px, py, px + size, py + size), outline="black", fill=col2)
        draw.text((px + 1 + int((size - w) / 2), py + 1 + int((size - h) / 2)), txt, font=font, fill="black")
        if quer:
                px = px + size + abstand
        else:
              py = py + size + abstand
     im.save("/tmp/mspFS.png", "PNG")
     if l4l:
         L4Lmspfs.add("mspFS.png", {"Typ": "pic", "Align": left, "Pos": top, "File": "/tmp/mspFS.png", "Size": str(breit), "Screen": l4l_sets[2], "Lcd": l4l_sets[1], "Mode": l4l_sets[8].replace(",", ""), "Transp": "True"})
         L4Lmspfs.setRefresh()

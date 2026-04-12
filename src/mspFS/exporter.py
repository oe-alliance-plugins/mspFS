
from configparser import ConfigParser, DuplicateSectionError
import datetime


class exporter():
    def __init__(self, datum=()):
         if len(datum):
            start = datetime.date(datum[0], datum[1], 1)
            monat = datum[1]
            turnus = ()
            self.w_list = []
            #end=datetime.date(datum[0],datum[1]+1,1)
            configparser = ConfigParser()
            configparser.read("/etc/ConfFS/mspFS.conf")
            if configparser.has_section("settings"):
                if configparser.has_option("settings", "schicht_col"):
                     schicht_colors = eval(configparser.get("settings", "schicht_col"))
                else:
                     schicht_colors = {"F": "#008B45", "S": "#FFD700", "N": "#3A5FCD", "fr": "#858585"}
                if configparser.has_option("settings", "turnus"):
                     turnus = configparser.get("settings", "turnus").split(",")
                     #del turnus[-1]
                else:
                     turnus = ("N", "fr", "fr", "fr", "F", "F", "S", "S", "N", "N", "N")
                f = open("/tmp/turnus", "w")
                f.write(str(turnus))
                f.close()
                xr = 0
                #while len(turnus)<29:
                #    turnus.append(turnus(xr)
                #    xr+=1
                if configparser.has_option("settings", "start_date"):
                     dx = configparser.get("settings", "start_date").split("-")
                     erstdatum = datetime.date(int(dx[0]), int(dx[1]), int(dx[2]))
                else:
                     erstdatum = datetime.date.today().replace(month=1, day=1)
                if configparser.has_option("settings", "sonders"):
                    sonders = eval(configparser.get("settings", "sonders"))
                else:
                    sonders = {}
            if len(turnus):
              sch1_list = []
              for x in turnus:
                #if x == " " and x not in sch1_list:
                #    sch1_list.append(x)
                if x.strip() not in sch1_list:
                     sch1_list.append(x.strip())
                #if not len(x.strip()) and " " not in sch1_list:
                #     sch1_list.append(" ")
              f = open("/tmp/turnus", "a")
              f.write(str(sch1_list) + "\n")
              f.close()
              tage = start - erstdatum
              sch_tag = tage.days
              if sch_tag > len(turnus):
                sch_tag = sch_tag % len(turnus)
              dat = start
              ende = 0

              while ende == 0:
                    schicht = None
                    if sch_tag + 1 > len(turnus):
                            sch_tag = sch_tag % len(turnus)
                    if str(dat).replace("-", "") in sonders:
                        schicht = sonders[str(dat).replace("-", "")]
                        color = schicht_colors[schicht]
                    else:
                        if sch_tag >= 0:
                               try:
                               #if len(str(turnus[sch_tag]).strip()):
                                   schicht = str(turnus[sch_tag]).strip()
                                   color = schicht_colors[str(turnus[sch_tag]).strip()]
                               except:
                                   schicht = str(turnus[sch_tag]).strip()
                                   color = "858585"
                    if schicht or schicht == "":
                        self.w_list.append((str(dat.day), schicht, color))

                    dat = dat + datetime.timedelta(1)
                    sch_tag += 1
                    if monat != dat.month:
                        ende = 1
              f = open("/tmp/turnus", "a")
              f.write(str(self.w_list))
              f.close()

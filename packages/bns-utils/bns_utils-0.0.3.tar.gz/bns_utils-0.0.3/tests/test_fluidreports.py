import sys
sys.path.insert(1, '../src/')
import bns_utils.fluidreports as fr

def test_report_deserialization(path):
    report = fr.Report(path)
    report.rebuild("Central Concentrator MF2 Production Report REBUILD.frx")
    report.clean("Central Concentrator MF2 Production Report CLEANED.frx")

test_report_deserialization("Central Concentrator MF2 Production Report.frx")
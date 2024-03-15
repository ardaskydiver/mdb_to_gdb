# Kurulumlari yapiniz

# Python 2.7 ile calismaktadir!!

# pip install arcpy
# pip install os
import arcpy, os

# MDB ve GDB klasor yollari girilir

inws = r'D:\\'
outws = r'D:\\'

# Access Veritabanlarini Listeler
arcpy.env.workspace = inws
mdbs = arcpy.ListWorkspaces(workspace_type = "Access")

count = 1
for m in mdbs:
    # Cikti GDB adini tanimlar
    fgdb_name = os.path.basename(m).split(".")[0] + ".gdb"

    # Yeni bir GDB olusturur
    arcpy.CreateFileGDB_management(outws, fgdb_name)

    # MDB icerisinde bulunan tum verileri kopyalar
    arcpy.env.workspace = os.path.join(inws, m)
    fcs = arcpy.ListFeatureClasses()
    for fc in fcs:
        arcpy.CopyFeatures_management(fc, os.path.join(outws, fgdb_name, fc))

    # Islem durumu hakkinda rapor verir
    print ("%s of %s MDB dosyaniz GDB olarak donusturuldu." % (count, len(mdbs)))
    count += 1

    # Detay veri kumesini listeler
    arcpy.env.workspace = os.path.join(inws, m)
    fds = arcpy.ListDatasets()
    for f in fds:
        # Mekansal referans sistemini belirler
        desc = arcpy.Describe(f)
        sr = desc.spatialReference

        # MDB'nin ismini ve mekansal referans sistemini GDB'ye kopyalar
        arcpy.CreateFeatureDataset_management(os.path.join(outws, fgdb_name), f, spatial_reference = sr)

        # Detaylari yeni GDB'ye kopyalar ve islem sonucu ile ilgili bilgi verir
        arcpy.env.workspace = os.path.join(inws, m, f)
        fcs = arcpy.ListFeatureClasses()
        for fc in fcs:
            arcpy.CopyFeatures_management(fc, os.path.join(outws, fgdb_name, f, fc))
            print ("Kopyalama islemi tamamlanmistir.")
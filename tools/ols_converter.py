from tools.olsmap import OlsMap
from tools.olscollection import OlsCollection
import clr
from re import sub


clr.AddReference("tools/lib/EDCSuite.Parsers")
clr.AddReference("tools/lib/EDCSuiteBaseLibrary")
import EDCSuiteBaseLibrary
import EDCSuiteParsers


def tohex(i):
    return str(hex(i)).replace("0x", "$").upper()


def get_json_as_olscollection(filename: str) -> str:
    filetype = str(EDCSuiteBaseLibrary.Tools().DetermineFileType(filename, True))
    print(">> Identified {} as {}".format(filename, filetype))

    parser = getattr(EDCSuiteParsers, filetype + "FileParser")()
    result = parser.parseFile(filename, None, None)

    maps = []

    for x in result[0]:
        map = OlsMap()
        map.Name = sub("\s?\[codeblock \d\]", "", x.Varname)
        map.FolderName = "CodeBlock {} | {}".format(x.CodeBlock, x.Subcategory)
        map.Columns = str(x.Y_axis_length)
        map.Rows = str(x.X_axis_length)
        map.Comment = x.Description
        map.Map_Name = map.Name
        map.Map_Unit = sub("\((.*)\)", r"\1", map.Name)
        map.Map_Factor = str(x.Correction)
        map.Map_Offset = str(x.Offset)
        map.Map_StartAddr = tohex(x.Flash_start_address)

        map.X_Name = x.X_axis_descr
        map.X_Unit = x.XaxisUnits
        map.X_Factor = str(x.X_axis_correction)
        map.X_Offset = str(x.X_axis_offset)
        map.X_DataAddr = tohex(x.Y_axis_address)

        map.Y_Name = x.Y_axis_descr
        map.Y_Unit = x.YaxisUnits
        map.Y_Factor = str(x.Y_axis_correction)
        map.Y_Offset = str(x.Y_axis_offset)
        map.Y_DataAddr = tohex(x.X_axis_address)

        maps.append(map)

    print(">> Identified {} maps in total".format(len(maps)))

    mapcoll = OlsCollection()
    mapcoll.maps = maps

    return OlsCollection.to_json(mapcoll, indent=2)
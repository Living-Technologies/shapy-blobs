import re
import pathlib



def getAttributeFileList( base ):
    """
        grabs all of the attrubte_xxx.txt and sorts them by xxx. Where xxx represents the time
        frame.
    """
    files = []
    base = pathlib.Path(base)
    pat = re.compile("attributes-(\\d+).txt")
    for f in base.glob("attributes*txt"):
        x = pat.findall(f.name)
        if len( x ) == 1:
            files.append( (int(x[0]), f ) )
    files.sort()

    return files

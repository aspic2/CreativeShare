
class Helper:

    def return_LID_sets(wbdata):
        LIDSets = []
        for row in wbdata:
            try:
                oldval = int(row[0])
                newval = int(row[2])
                LIDSets.append((oldval, newval))
            except:
                continue
        return LIDSets

    def return_source_LIDs(sets):
        #oldLIDs as string for query
        sourceLIDs = []
        for group in sets:
                sourceLIDs.append(group[0])
        return sourceLIDs

    def format_for_query(alist):
        alist = tuple(alist)
        alist = str(alist)
        return alist

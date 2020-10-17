def checksqlstatement(statement:str):
    if "or ''=''" in statement.lower():
        raise Exception("statement returns everything from the selected table")
    elif "'" in statement or '"' in statement:
        raise Exception("unsupported characters in statement. statement may result in unknown breaches")
    else:
        return statement

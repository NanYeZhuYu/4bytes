#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
import os
import sqlite3
import shutil

def printProgressBar(
    iteration,
    total,
    prefix="Progress:",
    suffix="Complete",
    decimals=1,
    length=100,
    fill="█",
    printEnd="\r",
):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + "-" * (length - filledLength)
    print("\r%s |%s| %s%% %s" % (prefix, bar, percent, suffix), end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()

def create_selector_table(DB):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    try:
        sql_create_table = '''CREATE TABLE SELECTOR
                                            (ID INTEGER PRIMARY KEY  AUTOINCREMENT   NOT NULL,
                                            METHOD_SIGNATURE     TEXT  NOT NULL,
                                            METHOD_NAME          TEXT  NOT NULL);'''

        sql_create_signaure_index = "CREATE INDEX METHOD_SIGNATURE_INDEX ON SELECTOR(METHOD_SIGNATURE)"
        cursor.execute(sql_create_table)
        cursor.execute(sql_create_signaure_index)
    except:
        clean_table = "DELETE FROM SELECTOR"
        cursor.execute(clean_table)

    cursor.close()
    conn.commit()
    conn.close()


def getMethodName(path):
    with open(path, 'r') as file:
        methodName = file.readline()
    return methodName


def merge_selctors_to_sqlite(DB, dataRoot):
    if not os.path.exists(dataRoot):
        return None

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    fileList = os.listdir(dataRoot)

    if len(fileList):
        sum_of_file = len(fileList) - 1
        location = 0
        for eachFile in fileList:
            path = f"{dataRoot}/{eachFile}"
            try:
                name = getMethodName(path)
            except Exception as e:
                print(e)
                print("{eachFile} is error......".format(file=eachFile))
                continue

            sql_insert_info = 'insert into SELECTOR (METHOD_SIGNATURE, METHOD_NAME) values (?,?)'
            cursor.execute(sql_insert_info, (eachFile, name))
            location += 1
            printProgressBar(location, sum_of_file, prefix=f"processing: {eachFile}")

    cursor.close()
    conn.commit()
    conn.close()
 
 
if __name__ == "__main__":

    signatureDir = "signatures"
    dbSaveDir = "./outputs/selector/ethereum/"
    if not os.path.exists(dbSaveDir):
        os.makedirs(dbSaveDir)

    DB = dbSaveDir + "method_signatures.db"
    create_selector_table(DB)
    merge_selctors_to_sqlite(DB, dataRoot=signatureDir)

    shutil.make_archive('method_signatures', 'zip', root_dir='./outputs', base_dir='selector/ethereum')


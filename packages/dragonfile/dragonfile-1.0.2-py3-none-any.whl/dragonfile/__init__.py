import csv

class dragonfile:
    def __init__ (self, dFile, nColumn, dSep=",", coding="utf-8", dictD={}):
        self.dFile = dFile
        self.nColumn = nColumn
        self.dSep = dSep
        self.coding = coding
        self.dictD = dictD
    
    def readFile(self):
        columns = []

        with open(self.dFile, encoding=self.coding) as file:
            reader = csv.reader(file, delimiter=self.dSep)
            header = next(reader)
            nameColumn = header[self.nColumn]

            for i, row in enumerate(reader):
                columns.append(row[self.nColumn])

        dictDaux = {nameColumn: columns}
        self.dictD.update(dictDaux)
        print("Termino",self.nColumn)
        self.nColumn += 1

        return self.dictD, self.nColumn

    def readFileSetPeriod(self, varOp0="", varOp1="Valor1", varOp2="Valor2", varOp3="Valor3", varLog0="1", varLog1="6", varLog2="12", twoColumn=False):
        columns = []
        columnsTwo = []

        with open(self.dFile, encoding=self.coding) as file:
            reader = csv.reader(file, delimiter=self.dSep)
            header = next(reader)
            nameColumn = header[self.nColumn]
            extraColum = "New"+header[self.nColumn]
            
            for i, row in enumerate(reader):
                word = row[self.nColumn]

                if word != varOp0:
                    word = int(word[0]+word[1])
                else:
                    word = varOp0

                if word != varOp0:

                    if word > varLog0 and word <= varLog1:
                        word = varOp1

                    elif word > varLog1 and word < varLog2:
                        word = varOp2

                    else:
                        word = varOp3
                        
                else:
                    pass
                
                columns.append(word)
                columnsTwo.append(row[self.nColumn])

            if twoColumn == False:
                dictDaux = {extraColum: columns}
                self.dictD.update(dictDaux)
                print("Termino",self.nColumn)
                self.nColumn += 1
            else:
                dictDaux1 = {nameColumn: columnsTwo}
                dictDaux2 = {extraColum: columns}

                dictDaux1.update(dictDaux2)
                self.dictD.update(dictDaux1)

                print("Termino",self.nColumn)
                self.nColumn += 1
            
            return self.dictD, self.nColumn

    def readFileRename(self, nameRow=[], renameRow=[]):
        columns = []

        with open(self.dFile, encoding=self.coding) as file:
            reader = csv.reader(file, delimiter=self.dSep)
            header = next(reader)
            nameColumn = header[self.nColumn]

            for i, row in enumerate(reader):
                j = 0
                while j < len(nameRow):
                    if row[self.nColumn] == nameRow[j]:
                        columns.append(renameRow[j])
                        j += 1
                    else:
                        j += 1

                if j > len(nameRow):
                    find = False
                else:
                    find = True
                
                if find == False:
                    columns.append(row[self.nColumn])
                else:
                    pass

        dictDaux = {nameColumn: columns}
        self.dictD.update(dictDaux)
        print("Termino",self.nColumn)
        self.nColumn += 1

        return self.dictD, self.nColumn

    def fileToCsv(self):
        with open(self.dFile, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(self.dictD.keys())
            writer.writerows(zip(*self.dictD.values()))

    def lenColumns(self):
        with open(self.dFile, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=self.dSep)
            first_row = next(reader)
            return len(first_row)
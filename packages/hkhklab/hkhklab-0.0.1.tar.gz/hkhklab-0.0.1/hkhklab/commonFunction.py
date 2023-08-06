def calcSumListHk(inputList):

    """ define function: calculate sum of List
        parameter: (str) List 
        return: (int) sum of List
    """

    # inputList = ["1","2","3","4","5"]
    inputListLen = len(inputList)

    for i in range(0, len(inputList)):
        inputList[i]  = int( inputList[i] )

    outputValue = sum(inputList)
    return outputValue
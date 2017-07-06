import csv
import math
import json

#CLASS START
class prefConv:

    collections = []
    interests = []
    variables = []

    def __init__(self, collections, interests):
        self.collections = collections
        self.interests = self.loadJson(interests)

#STATIC METHODS

    @staticmethod
    def loadJson(obj):
        jsonStr = obj.decode("utf-8")
        return json.loads(jsonStr)

    #only here temporarily
    @staticmethod
    def transferData(filename, variables, datafile):
        with open(filename, 'r+') as file:
            for i in range(len(variables)):
                file.write(str(variables[i][1])+", ")

    #adds all of the variables within the given collection to the collectionVariables array
    def findCollectionVariables(self, collectionTitle):
        collectionVariables = []
        for variable in self.collections[collectionTitle]:
            for interest in self.interests["interests"]:
                if str(interest) == variable:
                    collectionVariables.append(variable)
        return collectionVariables

    """
    Following 5 methods are involved in the findExternalities process.
    The function collects all variables within the current collection
    that overlap with those of other collections, adding up the 
    weights of those specifically. This will amplify all final
    collection values to create more accurate results with matches
    """ 

    def findExternalities(self, collectionTitle):
        collectionVariables = self.findCollectionVariables(collectionTitle)
        return math.sqrt(self.createExternalities(collectionTitle, collectionVariables) * .15)

    def createExternalities(self, collectionTitle, collectionVariables):
        externality = 0
        for collection in self.collections:
            externality += self.checkCollectionTitle(collectionTitle, collection, collectionVariables)
        return externality

    def checkCollectionTitle(self, collectionTitle, collection, collectionVariables):
        if collection != collectionTitle:
            return self.addExternalities(collectionVariables, collection)
        elif collection == collectionTitle:
            return 0

    def addExternalities(self, collectionVariables, collection):
        temp = 0
        for variable in self.collections[collection]:
            for cVarIndex in range(len(collectionVariables)):
                temp += self.checkVarName(collectionVariables[cVarIndex], variable, collection)
        return temp

    def checkVarName(self, cVar, variable, collection):
        if cVar == variable:
            return self.collections[collection][variable]
        elif cVar != variable:
            return 0

    """
    Following 2 methods are part of the weightsToVals process.
    The function converts all interests of the user to a weight
    using the values found in the provided collections. Alongside
    these values, the findExternalities process is also utilized
    for the reasons provided above (the result of FindExternalities
    is included in the final variable values)
    """

    def weightsToVals(self):
        values = []
        for collection in self.collections:
            weight = 0
            for variable in self.collections[collection]:
                for interest in self.interests["interests"]:
                    weight += self.checkInterest(collection, variable, interest)
            values.append((collection, weight))
        return values

    def checkInterest(self, collection, variable, interest):
        if variable == str(interest):
            return self.collections[collection][variable] + self.findExternalities(collection)
        elif variable != str(interest):
            return 0


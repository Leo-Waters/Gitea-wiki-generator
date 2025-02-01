from pathlib import Path
from ScriptParser import ScriptParser
from DataModel import namespace_node,class_node,struct_node,variable_node

keyWords = {"namespace","class","struct","enum"}
modifiers = {"virtual","override","abstract","partial","sealed","static"}
access_modifiers = {"private","public","protected","internal"}

#base class for script parsers
class CSharp_Parser(ScriptParser):

    def __init__(self):
        super().__init__(language="cs")
    
    #takes content and current index and returns contents of current scope { } including the index of the end of scope
    def extract_scope(content,startIndex):

        open_count=0
        close_count=0
        extractedScope=""
        for index,char in enumerate(content,startIndex):
            if(char=="{"):
                open_count=open_count+1
            elif(char=="}"):
                close_count=close_count+1
            
            extractedScope=extractedScope+char
            
            if(close_count==open_count):
                return {extractedScope,index+1}



    def extract_namespaces(self,content):
        results = []

        # Iterate over each character in the file
        for i, char in enumerate(content):
            # Detect namespace start
            if content[i:i + 9] == "namespace" and (i == 0 or content[i - 1].isspace()):
                #get the index where the namespace scope starts
                cutoffIndex=content.find('{',i+9)
                #get the full namespace name substring
                namespace_name=content[i+9:i+cutoffIndex-1]

                namespace_content,end_of_scope=self.extract_scope(content,cutoffIndex)

                results.append({namespace_name,namespace_content})    
                i=end_of_scope
                continue            

        # Return all captured namespaces
        return results

    def parse_namespace(self,name,contents):
        namespace = namespace_node(name=name)

        for line in contents:
            for c in line:
                if c == ' ':#end of word
                    if currentWord in access_modifiers:
                        currentAccessModifer=currentWord
                    if currentWord in modifiers:
                        currentModifier=currentWord
                    if currentWord in keyWords:
                        currentKeyWord=currentWord
                    #clear the word buffer
                    currentWord=""

                elif c == ';':#end of statement
                    pass
                elif c == '{':#begining of scope
                    pass
                elif c == '}':#end of scope
                    pass
                else:
                    currentWord=currentWord+c
            
            #end of line

        return namespace

    def parse_file(self,filePath):

        #load the file into a string
        fileContents=ScriptParser._load_from_file(filePath)

        #get the namespaces names and contents
        namespaces_and_contents=self.extract_namespaces(fileContents)

        namespaces= []

        #parse all the name spaces        
        for name,contents in namespaces_and_contents:
            namespaces.append(self.parse_namespace(name=name,contents=contents))

        #return parsed data, these namespaces will most likely be duplicates and will need to have children be merged 
        return namespaces





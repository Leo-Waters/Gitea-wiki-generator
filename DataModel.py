#switch to database type model
import os
baseUrl= os.getenv('LINK_BASE_URL')


class code_node:
    def __init__(self,parent=None,name="blank node",desc="",generates_page=False,tag="n/a"):
        if(parent!=None):
            parent.addChild(self)
        self.parent=parent
        self.name=name
        self.desc=desc
        self.children=[]
        self.generates_page=generates_page

        if(generates_page):
            self.link=self.get_tree("-")
        else:
            self.link=None
        self.tag=tag
        

    def setParent(self,parent):
        if(parent!=None):
            parent.addChild(self)
        self.parent=parent
    #adds child called internaly by child when parent is set
    def addChild(self,child):
        self.children.append(child)

    #follows nodes till reaches the root
    def getRoot(self):
        node=self
        while(node.parent!=None):
            node=node.parent

    def findOrCreateNameSpaceParent(self,name):
        if('.' in name):
            
            scopes=name.split('.')
            totalscopes=len(scopes)

            parent=self
            i=0
            while i < totalscopes-1:
                scope=scopes[i]

                selectedChild=None
                for child in parent.children:
                    if(child.name==scope):
                        selectedChild=child
                
                if(selectedChild!=None):
                    parent=selectedChild
                else:
                    parent=namespace_node(parent,scope)

                i=i+1
            

            return parent,scopes[totalscopes-1]
        else:
            #the name of the discoverd namespace doest require any parent namespaces
            return self,name

    def debugChildren(self,depth=0):
        
        debugString=(" "*depth*4)+("-"*depth)
        debugString=debugString+" "

        for child in self.children:
            message=debugString+child.debug_info() 
            print(message)
            child.debugChildren(depth+1)

    def debug_info(self):
        return f'{self.name} ({self.tag}) "{self.desc.replace("\n", " *new-line* ")}"'
    
    #if the node has a page, this function will return its markup
    def get_page_markup(self):
        pass
    
    #returns what the parent page should see 
    def get_parent_page_markup(self):
        return self.get_tree()

    #gets a link if applicable or the name
    def get_link(self):
        if(self.generates_page):
            return f"[{self.name}](baseUrl)"
        else:
            return f"self.name"
        
    
    def get_tree(self,seperator=" -> "):
        node=self
        node_names=[]
        while node != None:
            node_names.append(node.get_link())
            node=node.parent
        
        node_names.reverse()

        tree=""
        for name in node_names:
            tree=f"{tree}{seperator}{name}"
        
        return tree

class namespace_node(code_node):
    def __init__(self,parent=None,name="blank namespace node",desc=""):
        super().__init__(parent=parent,name=name,desc=desc,generates_page=True,tag="namespace")
    
    def get_page_markup(self):
        markup= f"##namespace -> {self.name}\n\n{self.get_tree()}\n\n##\n{self.desc}\n\n##Varibles##\n\n"
        return markup

#proivdes the extra property access modifier for public private ect
class access_modifier_node(code_node):
    def __init__(self,parent,name,desc,access_modifiers = ["private"] ,generates_page=False,tag="n/a"):
        super().__init__(parent=parent,name=name,desc=desc,generates_page=generates_page,tag=tag)
        self.access_modifiers=access_modifiers
    
    def debug_info(self):
        modifiers=""
        for mod in self.access_modifiers:
            modifiers=f"{modifiers} {mod}"

        return f'{modifiers} {self.name} ({self.tag}) "{self.desc.replace("\n", " *new-line* ")}"'

class variable_node(access_modifier_node):
    def __init__(self,parent,name,desc,type,access_modifiers = ["private"]):
        super().__init__(parent=parent,name=name,access_modifiers=access_modifiers,desc=desc,tag="var")
        self.type=type

    def debug_info(self):
        modifiers=""
        for mod in self.access_modifiers:
            modifiers=f"{modifiers} {mod}"

        return f'{modifiers} {self.type} {self.name} ({self.tag}) "{self.desc.replace("\n", " *new-line* ")}"'

class struct_node(access_modifier_node):
    def __init__(self,parent,name,desc,access_modifiers = ["private"],tag="struct"):
        super().__init__(parent=parent,name=name,desc=desc,access_modifiers = access_modifiers,generates_page=True,tag=tag)

class class_node(struct_node):
    def __init__(self,parent,name,desc,access_modifiers = ["private"]):
        super().__init__(parent=parent,name=name,desc=desc,access_modifiers=access_modifiers,tag="class")



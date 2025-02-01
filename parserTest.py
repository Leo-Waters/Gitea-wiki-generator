import re

from DataModel import namespace_node,class_node,struct_node,variable_node

def extract_scope(content,startIndex):

    open_count=0
    close_count=0
    extractedScopeStartIndex=None

    for index,c in enumerate(content,startIndex):
        char=content[index]
        
        if(char=='{'):
            open_count=open_count+1

            if(extractedScopeStartIndex ==None):
                #this is the first open scope, this is the start of the sub string we want to capture
                extractedScopeStartIndex=index
            
        elif(char=='}'):
            close_count=close_count+1
        
        
        if(close_count==open_count):
            #all the opened scopes have been closed, this means we have caputured the contents
            return content[extractedScopeStartIndex:index],(index+1)

modifiers = {"virtual","override","abstract","partial","sealed","static","private","public","protected","internal"}

def is_modifier(index,content):
    for modifier in modifiers:
        if(content[index:index+len(modifier)]==modifier):
            
            return True,modifier,index+len(modifier)
    
    return False,None,index+1

def proccess_scope(parent_node,content):
        results = []

        i=0
        commentBuffer=""

        collected_modifiers=[]
        last_modifier_index=0
        collected_name=""
        linesSinceLastComment=0
        # Iterate over each character in the file
        while i < len(content):



            #clear comments after blank lines, ost likely not linked to next scope
            if(content[i:i+2]=="\n"):
                linesSinceLastComment=linesSinceLastComment+1
                if(linesSinceLastComment==3):
                    commentBuffer=""
            
            # detected single line comment
            if(content[i:i+2]=="//"):
                i=i+2
                if(content[i]=="/"):
                    i=i+1
                end_of_comment=content.find("\n",i)

                if(commentBuffer!=""):
                    commentBuffer=commentBuffer+"\n"
                commentBuffer=commentBuffer+content[i:end_of_comment]
                i=end_of_comment
                linesSinceLastComment=0
                continue

            #found multi line comment
            if(content[i:i+2]=="/*"):
                i=i+2
                end_of_comment=content.find("*/",i)

                commentBuffer=commentBuffer+content[i:end_of_comment-1]
                i=end_of_comment
                linesSinceLastComment=0
                continue

            #check and gather access modifier
            is_modifier_bool,modifier_rtn,modifier_skip=is_modifier(i,content)

            if(is_modifier_bool):
                collected_modifiers.append(modifier_rtn)
                print(f"skipping {modifier_skip-i} characters for {modifier_rtn}")
                i=modifier_skip
                last_modifier_index=modifier_skip
                continue



            # Detect namespace start
            if content[i:i + 9] == "namespace" and (i == 0 or content[i - 1].isspace()):

                #get the index where the namespace scope starts
                cutoffIndex=content.find('{',i+9)

                #get the full namespace name substring
                namespace_name=content[i+9:cutoffIndex].strip()

                #extract the scope and get end index
                namespace_content,end_of_scope=extract_scope(content,cutoffIndex)

                scoped_namespace_parent,scoped_namespace_name =parent_node.findOrCreateNameSpaceParent(namespace_name)

                namespace= namespace_node(parent=scoped_namespace_parent,name=scoped_namespace_name)

                #recursive call
                proccess_scope(namespace,namespace_content)

                #move the itteration forward until its past the namespaces scope
                i=end_of_scope
                continue      

            if content[i:i + 5] == "class" and (i == 0 or content[i - 1].isspace()):  
                
                #get the index where the class scope starts
                cutoffIndex=content.find('{',i+5)

                #get the full namespace name substring
                class_name=content[i+5:cutoffIndex].strip()

                description=commentBuffer
                commentBuffer=""

                #extract the scope and get end index
                class_content,end_of_scope=extract_scope(content,cutoffIndex)

                class_ =class_node(parent=parent_node,name=class_name,desc=description,access_modifiers=collected_modifiers)
                collected_modifiers= []
                proccess_scope(class_,class_content)

                #move the itteration forward until its past the namespaces scope
                i=end_of_scope
                continue      

            if content[i:i + 6] == "struct" and (i == 0 or content[i - 1].isspace()):  
                
                #get the index where the class scope starts
                cutoffIndex=content.find('{',i+5)

                #get the full namespace name substring
                class_name=content[i+6:cutoffIndex].strip()

                description=commentBuffer
                commentBuffer=""

                #extract the scope and get end index
                struct_content,end_of_scope=extract_scope(content,cutoffIndex)

                struct_ =struct_node(parent=parent_node,name=class_name,desc=description,access_modifiers=collected_modifiers)
                collected_modifiers= []
                proccess_scope(struct_,struct_content)

                #move the itteration forward until its past the namespaces scope
                i=end_of_scope
                continue     

            if content[i] == "(":
                functionParams  

            if content[i] == ";":  
                
                print(content[i-5:i])
                cutoffIndex=content.find(' ',last_modifier_index)

                var_type_name=content[last_modifier_index:cutoffIndex].strip()


                var_name=content[last_modifier_index:i].strip()

                description=commentBuffer
                commentBuffer=""

                variable_node(parent=parent_node,name=var_name,type=var_type_name,desc=description,access_modifiers=collected_modifiers)
                collected_modifiers= []

                #move the itteration forward until its past the namespaces scope
                i=i+1
                continue     

            i=i+1

# Example C# file content
cs_content = """
namespace leo {
    //this is a class A desc
    ///this is also a class a desc
    public class math {

        public int x=1;
        //this function adds int a and b and returns the result
        public int add(int a, int b) {}
    }

    //this class extends maths
    public class extended_maths : math
    {
        public int add_three(int a,int b,int c)
        {
            return add(add(a,b),c);
        }
    }
    namespace sub {
        //this is a class B desc
        
        public static class B {
            ///this is sub class desc
            protected class subClass{
                void MethodD(){}
            }
            void MethodB() {}
        }
    }
}

namespace leo.gui {

    /*
    This is a multi-line comment in C#.
    You can write as many lines as you need.
    Each line will be part of the comment until you close it with */
    class C {
        void MethodC() {}
    }

    public struct gui_state
    {
        int x,y;
        float z;
    }
}
"""

root_namespace = namespace_node(name="",desc="the root name space")

# Extract namespaces
proccess_scope(root_namespace,cs_content)


# Print results
root_namespace.debugChildren()

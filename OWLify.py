
import pickle, sys, string


class OWL:

    def __init__(self, namespace, outfile, propurl):
        self.namespace = str(namespace)
        self.outfile = outfile
        #self.outfile = 'output.owl'
        #self.propurl = 'http://staff.washington.edu/ngopal/prenatal.owl'
        self.propurl = propurl
        self.doc = ''
        self.start()

    def start(self):
#        stub='<?xml version="1.0" encoding="iso-8859-1"?> '+'\n'
        stub=''
        stub+='<rdf:RDF xmlns:dc="http://purl.org/dc/elements/1.1/"'+'\n'
        stub+='\txmlns:owl="http://www.w3.org/2002/07/owl#"'+'\n'
        stub+='\txmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"'+'\n'
        stub+='\txmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#" '+'\n'
        stub+='\txmlns:xsd="http://www.w3.org/2001/XMLSchema#"'+'\n'
        stub+='\txml:base="http://www.example.org/'+domain+'"'+'\n'
        stub+='\txmlns="http://www.example.org/'+domain+'#">''\n\n'
#
        stub+='<owl:Ontology rdf:about="">'+'\n'
        stub+='\t<rdfs:comment>Taxonomy for '+domain+'</rdfs:comment>'+'\n'
        stub+='</owl:Ontology>\n'
#        print stub
        self.doc += stub
        return 0

    def addClass(self, classname):
        classname=string.replace(classname,' ','_')
        classname=string.replace(classname,'-','_')
        stub = '\n<owl:Class rdf:ID="'+classname+'">\n'
        stub += '</owl:Class>\n'
        
#        print stub
        self.doc += stub
        return 0

    def addSubClass(self, classname, superclassname):
        classname=string.replace(classname,' ','_')
        classname=string.replace(classname,'-','_')
        superclassname=string.replace(superclassname,' ','_')
        superclassname=string.replace(superclassname,'-','_')
        stub = '\n<owl:Class rdf:ID="'+classname+'">\n'
        stub += '\t<rdfs:subClassOf rdf:resource="#'+superclassname+'"/>\n'
        stub += '</owl:Class>\n'
#        print stub
        self.doc += stub
        return 0
        
    def addInstance(self, classname, inst, val):
        classname=string.replace(classname,' ','_')
        inst=string.replace(inst,' ','_')
        stub='\n<'+classname+' rdf:about="#'+str(val)+'">\n'
        
        stub+='<title rdf:datatype="#string">'+str(inst)+'</title>\n'
        stub+='</'+classname+'>\n'
#        <owl:Class rdf:ID="reviewedarticle">
#            <rdfs:subClassOf rdf:resource="#publication"/>
#        </owl:Class>


    


    

    def end(self):
        fileh = open(self.outfile, 'w')
        self.doc += '</rdf:RDF>\n'
        fileh.write(self.doc)
        fileh.close()



def recAdd(o, parent, level):
    p=parent
    if parent=='Product':
        p=''
    try:
        labelMap=pickle.load(open('level'+str(level)+'/'+domain+'_'+p+'_LABEL_MAP.p'))
        labelDict=pickle.load(open('level'+str(level)+'/'+domain+'_'+p+'_LABEL_DICT.p'))
        par=string.replace(parent,'&','and')
        for l in labelMap:
            if labelDict[l]>limit:
                cat=string.replace(labelMap[l],'&','and')
                
                o.addSubClass(cat,par)  
                recAdd(o, labelMap[l], level+1)
    except:
        return
    


domain=sys.argv[1]
limit=int(sys.argv[2])
namespace=domain
outfile='Data/Tax_'+domain+'.owl'
propUrl='http://www.example.org'
o=OWL(namespace,outfile,propUrl)

labelMap=pickle.load(open('level0/'+domain+'__LABEL_MAP.p'))
labelDict=pickle.load(open('level0/'+domain+'__LABEL_DICT.p'))
cmap={}
isAdded={}

level=0
o.addClass('Product')
recAdd(o,'Product',level)

#for l in labelMap:
#    if labelDict[l]>limit:
#      o.addSubClass(labelMap[l],'Product')  
#      recAdd(o,labelMap[l],level+1)


o.end()       
        

    
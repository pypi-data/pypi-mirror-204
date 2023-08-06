#!/usr/bin/env python3
import sys
from ete3 import *
from .MMlib3 import *
from ncbi_db import ncbi_sequences
from ncbi_db import ncbi_taxonomy_tree
from ncbi_db import ncbi_taxonomy
from .tree_classes import *
import brewer2mpl ## nice colors
from math import log10
import random

class TextFace(faces.TextFace):
  def __init__(self,  *args, **kargs):
    if 'ftype' in kargs: pass
    else:                kargs['ftype']=opt['ft']
    return faces.TextFace.__init__(self,  *args, **kargs)

global help_msg
help_msg="""Program to show a tree of sequences using ete3. Accepts various id formats and provide options to customize the graphics.

Usage:    show_tree.py -f input_tree.newick [other_options] [feature_files] 

This program is thought for visualization of tree of sequences. It derives the species to which every node in the input tree belongs to, and their complete ncbi taxonomy. By default, node names can be gi codes from ncbi (like gi|12356715|whatever) which are interpreted as protein ids and fetched connecting to ncbi. Use option -nt to specify that the gi refers to a nucleotide entry. Node names can be selenoprofiles joined ids, like this: fam.1.label.species.target. Alternatively, other options are available to control species and taxonomy (see -h full).

## Tree attributes
-format forces ete3 to read the input tree in a certain newick specification. Def:0
-b      show branch support as values in the bottom of branch nodes
-s      do not show the column with the species name
-l      do not show the column with the taxonomy of the species. Taxonomy is still computed though: use -CL -1 to avoid fetching taxonomy from ncbi
-C      circular tree
-scale  defaults to 10, set higher to increase the size of the branches. when -C is active it gets *10
-ali    fasta alignment used to display the sequences directly in the nodes. The program tries also to derive the genomic coordinates of each result from the titles, to display intron positions. This will work only if titles are MMlib headers (e.g. selenoprofiles output). Otherwise, only the alignment structure is displayed and a warning is printed.

By default, the ETE interactive environment is opened to display the tree according to options. When it is closed, the program quits. 
Alternatively, one can:

-p      open interactive mode (prompt) after showing tree
-out    print file in output. Can be .png or .pdf ; if this option is active, the graphical environment will not be opened.
 -img_h  height in pixels of output file (only if -out is active)
 -img_w  width in pixels of output file  (only if -out is active)

To further customize visualization, see the advanced help page using  show_tree.py   -h full  """

advanced_help= """\n####### Advanced help page #######
-v            verbose mode. prints lots of stuff
-config       load options from this configuration file
-save_config  save options to this configuration file
-dry          do not produce any graphics (does not require X11)

## Setting outgroup; to call the duplications/losses events, the tree must be rooted. There are three ways to do this:
        by default, the outgroup is set using the ete3 Tree class method named get_midpoint_outgroup, which splits the tree according to branch length
-o      directly choose outgroup; the argument must be a node name. Otherwise, for ancestral nodes, you can define the outgroup node as last common ancestor of two or more nodes using the "&" symbol. E.g. "-o   'node_id1&node_id5'"
-age    species2age file (each line is species TAB age). if provided, the function get_age_balanced_outgroup is used to decide the outgroup. 

## Controlling size of elements added with option -ali
-ali_w      total width of face displayed (including gaps)
-ali_wpp    width per position (only if coordinates of the gene are recognized)
-ali_h      total height of face displayed (including gaps)
-ali_p      what is printed on this face; defaults to nothing. You can use comma separated arguments, e.g. chromosome,id

## Controlling style: node names, species and taxonomy displayed
-no_id  do not show face with node name
-nb     do not show colored balls next to nodes based on labels
-sf     species function. specify a python function based on "x" as the node name. Example:   -sf " x.split('.')[1] "; the result look like: "Drosophila melanogaster"; it can return 'ncbi', in which case it is taken as NCBI protein id
-st     species tab file (alternative to -sf). Each line must have this structure:    node_name TAB species name  (no space in between)
-um     unmask characters. Use with options -sf or -st if the species names are coded like: "Drosophila_melanogaster", "Xenopus_{ch40}Silurana{ch41}_tropicalis"
-umn    unmask ncbi ids before fetching. Use those ids with 'ncbi' assigned with -sf and -st are masked, e.g. XP{ch95}006124501{ch46}1
-cl     custom lineage summary. A tab separated file must be provided, with first field: species name (unmasked), and second field: custom lineage. The standard lineage fetched from the ncbi will be printed for species not found in the file
-CL     same as -cl, but it forces all names from the file provided. If no taxonomy is found for a species, it is left blank
-cs     common species translation; a tab separated file must be provided as argument
-tax    species and taxonomy information file. It is a tab separated file like: nodename TAB speciesname TAB taxonomyinfo. Actually one such .tax file is written at the end of computation, to derive all this information just once per tree.
-ids    show custom defined ids (instead of standard node names from input tree) next to each node. You must provide a tab separated file as argument
-g      tolerate errors in taxonomy determination (useful for big trees)
-mc     maximum number of characters in a species name
-ft     font type used in displayed text

## Duplications/speciations
-mfd    saturation number of species supporting a duplication. Even if an event has more support that this, it will not be displayed bigger

## Manipulating tree
-exec     execute some python commands given as string before calling t.show()
-remove   file with node names to be removed from the tree before displaying
-zoom     show only a portion of the tree, defined as the last common ancestor of two nodes. Argument= nodeName1&nodeName2
-log      transform branch lengths so that newDist=log10(1+dist)

## Controlling labels; these are categorical attributes of nodes which are color coded in the graphics'
-lab      label file, controlling each color and possibly an image to display next to each node. Format for each line: label -tab- color    OR   label -tab- color -tab- path_to_image
-lf       function to derive label from node name. specify a python function based on "x" as the node name. Example:   -sf " x.split('.')[2] "
-L        alternative to -lf to define label for each node. File format:  protein_id1 -tab- label
-lmap     if not -lab, then colors are automatically set; use this to define the options of the color settings with brewer2mpl.
          Format class:name  e.g. Qualitative:Set1

## Additional coloring:
-k      color scheme for species/lineage. Default ("1") is color by kingdom; "2" is color by eukaryotic lineage; "0" not to color
        do not color species and taxonomy according to kingdom.  default is Bacteria: red; Archaea: blue; Eukaryotes: green (non metazoa: darker green) 
        Another format for argument: lineage1:color1,lineage2:color2  etcetera
-y      file with style specifications, allowing to color backgrounds or text of certain nodes. 
 Format of each line:  which_nodes:what_style    where:
  which_nodes can be  i=NODEID or s=SPECIES or t=TAXONOMYTAG  or any comma-separated combination; ID1&ID2 can be used to call an ancestor
  what_style  can be  fgcolor=COLOR or bgcolor=COLOR (any attribute of Node.img_style in format WHAT=VALUE) or any comma-separated combination. c= is short for bgcolor=
  Examples of lines:  s=Homo_sapiens,s=Gorilla_gorilla:c=orange     t=Rodentia:fgcolor=red 
-Y      Like -y but provided on the command line instead; different 'lines' are here separated by ";" characters
-ac [n]   automatic color by duplication cluster. Experimental. Use -aco [ofile] to write file

## Features files; these are files to add custom columns for certain or all nodes. 
You can specify any feature files on the command line (see Usage above). These must have the following format; all delimiters shown from here below with more than one space are actually tab separators. Those shown as single spaces must be single spaces. Simplest example:

protein_id1    labelA
protein_id2    labelB
protein_idN    labelZ

Additional information can be included in the header of the feature file, to define the color with which the feature label will be printed. If undefined, black is used.
#FEATURE_TITLE cysteine #880000   selenocysteine #008800
Aan.C3    cysteine
Aan.U13   selenocysteine
Aan.U13a  selenocysteine

"""
def verbose(msg):
  global opt
  if opt['v']:   write(msg, 1)
  else:          service(msg)

def label_to_image(label):
  """This function is used when you define a particular feature file with option -L ; each node is drawed using a colored ball. The image for the ball is searched into image_folder, the file name depends on the label translated through label2image . If the label is not present among the keys, the image corresponding to the label "unknown" is used. """
  if label in label2image:    return label2image[label]
  else:                             return None

def label_to_color(label):
  if label in label2color:    return label2color[label]
  else:                             return label2color['unknown']
  
class BallImgFace(faces.ImgFace):
  def update_pixmap(self):
    self.pixmap = faces.QPixmap(self.img_file).scaled(15, 15, faces.Qt.KeepAspectRatio)

def get_duplication_size(node):
  """ function that assigns the size of a duplication node for displaying, in order to display nodes with higher reliability, given by the number of species supporting the duplication"""
  global opt
  if len(node.children)!=2 : return 4
  a, b = node.children
  set_a, set_b = set(), set()
  for n in a.traverse(): 
    if n.is_leaf(): set_a.add(protein2species[n.name])
  for n in b.traverse(): 
    if n.is_leaf():       set_b.add(protein2species[n.name])
  n_species= len(set_a.intersection(set_b))
  size= min(2+ n_species, 2+opt['mfd']) #more than 12 species will be displayed as 
  return size

def is_selenoprofiles_title(short_title): 
  short_title=short_title.split()[0]
  return short_title.count('.')==4 and is_number(  short_title.split('.')[1] )

lineage_color_specs=None
def get_color_for_lineage(t, s, option):
  t+='; '
  global lineage_color_specs
  if option==1:
    if   'Bacteria;'  in t: c="#990000"     
    elif 'Archaea;'   in t: c="#000099"     
    elif 'Eukaryota;' in t:  
      #drawing a slighly different color for non-metazoa
      if 'Metazoa; '  in t:          c="#009900"     
      else:                          c="#004400"     
    else:       c='#000000'
  elif option==2:
    if   not 'Metazoa; ' in t:    
      if   'Fungi; ' in t:          c='orchid'
      elif 'Chlorophyta; ' in t:    c='#222222'
      elif 'Archaea; ' in t:        c='#0A0A0A'
      elif 'Bacteria; ' in t:       c='#131313'
      else:                       c='#727073'
    elif not 'Bilateria; ' in t:  c='#ACAAAD'
    else: 
      if 'Deuterostomia; '   in t:
        if 'Vertebrata; '    in t:     
          if   'Mammalia; '    in t:       
            if   'Primates; ' in t:              c='#009900' #green            
            elif 'Rodentia; ' in t:              c='#00AA33' #green
            else:                                c='#187700' #green 
          elif 'Sauropsida; '  in t:       c='#004400' #darkergreen
          elif 'Amphibia; '    in t:       c='#178A71' #cyan
          elif 'Actinopterygii; '   in t:  c='#249BC9' #blue
          else:                            c='#153EB0'  #other vertebrates  #darkerblue
        else: c='#382AB8' #other deuteros    #darkpurple
      elif 'Protostomia; '    in t:
        if   'Insecta; '    in t:   c='#D10000'  #red
        elif 'Arthropoda; ' in t:   c='#690707'  #darker red    
        elif 'Nematoda; '    in t:  c='#E016A4'  #violet
        elif 'Mollusca; '    in t:  c='#D18C0A'  #orange
        else:                       c='#B0B518'  #yellow
      else:
          c='#000000'  #any bilaterian is not protos and not deuteros ?     
  elif option==0:  c="#004400"
  else:
    if lineage_color_specs is None:
      lineage_color_specs=[]
      for piece in option.split(','):
        lineage, color=piece.split(':')
        lineage_color_specs.append([lineage,color])
    c='#000000'
    for lineage, color in lineage_color_specs:
      if lineage+'; ' in t or s.startswith(lineage): c=color
  return c 

## Function to draw the tree. This is applied to every node
def mylayout(node):
  ## Phylogeny layout
  if hasattr(node,"evoltype"):
    if node.evoltype == 'D':
      node.img_style["fgcolor"] = "#1111FF"
      node.img_style["size"] = get_duplication_size(node)
    elif node.evoltype == 'S':
      node.img_style["fgcolor"] = "#FF1111"
      #node.img_style["line_color"] = "#FF0000"
      node.img_style["size"] = 4
  if not node.is_leaf():
    if node.name in style_dictionary['id']:     
      for attribute in style_dictionary['id'][node.name]:
        node.img_style[attribute] = style_dictionary['id'][node.name][attribute]
  else:
    node.img_style["size"] = 0
    node.img_style["fgcolor"] = "#000000"
    column_index=0
    label=id2label[node.name]
    label_color=label_to_color( label )
    image_path=label_to_image(  label  )
    if not image_path is None and not opt['nb']:
      ballFace=BallImgFace(image_path)
      faces.add_face_to_node(ballFace, node, column = column_index, aligned = False)
      column_index+=1
    elif image_path is None and not opt['nb']:         #not
      circleFace= faces.CircleFace( 4, label_color, style='sphere', label=None)
      faces.add_face_to_node(circleFace, node, column = column_index, aligned = False)
      column_index+=1
    else:
      column_index+=1

    # id writing
    if not opt['no_id']:
      fg_color="#000000"
      node_name_to_write=node.name
      if node_name_to_write.startswith('gi|'): node_name_to_write='gi|'+node_name_to_write.split('|')[1]
      elif is_selenoprofiles_title(node.name): node_name_to_write= node.name.split('.')[1]
      if node.name in names_to_show:           node_name_to_write= names_to_show[node.name]   ### if opt['ids'] is active
      nameFace=TextFace(node_name_to_write, fgcolor=fg_color)
      nameFace.margin_left=1; nameFace.margin_right=4
      faces.add_face_to_node(nameFace, node, column = column_index, aligned = False)
      column_index+=1

    for face in node.extra_faces:
      faces.add_face_to_node(face, node, column = column_index, aligned = True)
      column_index+=1

    if True: ###not (opt['s'] and not opt['k'] and opt['l']):
      #drawing species column
      species_name= protein2species[node.name]
      text_color="#000000"
      tax_string=''
      if opt['k'] or not opt['l']:
        #computing full lineage
        if opt['CL']:        tax_string=''
        else:                
          try:          tax_string=taxonomy_lineages[species_name]
          except KeyError: 
            if not opt['g']: raise
            printerr('WARNING no taxonomy for this species: {s}'.format(s=species_name), 1)
            tax_string=''
      if opt['k']:
        #setting color
        text_color=get_color_for_lineage(tax_string, species_name, opt['k'])

      if not opt['s']:    
        #adding species column
        verbose( "drawing "+ node.name +"\t\tspecies:"+ species_name)
        species_name_to_show= species_name
        if len(species_name_to_show)>opt['mc']: species_name_to_show=species_name_to_show[:opt['mc']]+'*'
        if species_name in species_common_names:          species_name_to_show=species_common_names[species_name]    ### for opt['cs']
        sp_face=TextFace(species_name_to_show+' ' , fgcolor=text_color) #######
        sp_face.margin_left=5;         sp_face.margin_right=5
        faces.add_face_to_node(sp_face, node, column = column_index, aligned = True)
        column_index+=1

      if not opt['l']:
        #drawing lineage column
        summ_lineage=lineage_string_to_abstract(tax_string)
        if species_name in custom_lineages:   
          summ_lineage= custom_lineages[species_name]
          write( (tax_string, summ_lineage, species_name), 1)

        lineage_face=TextFace(summ_lineage+' ' , fgcolor=text_color) 
        faces.add_face_to_node(lineage_face, node, column = column_index, aligned = True)
        column_index+=1

      pos_dict={}   ### all this block does nothing unless there's stuff in style_dictionary['tax']
      for taxtag in style_dictionary['tax']:
        f=tax_string.find ( '{}; '.format(taxtag) )
        if f!=-1: pos_dict[taxtag]=f
      for taxtag in sorted( list(pos_dict.keys()), key=lambda x:pos_dict[x] ):
        for attribute in style_dictionary['tax'][taxtag]:
          node.img_style[attribute] = style_dictionary['tax'][taxtag][attribute]         

      if species_name in style_dictionary['species']:
        for attribute in style_dictionary['species'][species_name]:
          node.img_style[attribute] = style_dictionary['species'][species_name][attribute]

      if node.name in style_dictionary['id']:     
        for attribute in style_dictionary['id'][node.name]:
          node.img_style[attribute] = style_dictionary['id'][node.name][attribute]
    
    """
    if opt['seq']:
      if hasattr(node, 'sequence') and node.sequence:
        seq_face= faces.SequenceFace( node.sequence, 'nt')
        faces.add_face_to_node(seq_face, node, column = column_index, aligned = True)
        column_index+=1"""

    for feature_index in range(len(features_dictionaries)):
      features_dict= features_dictionaries[feature_index]
      features_dict_label_to_color= features_dictionaries_label_to_color[feature_index]
      text='';       color='#000000'
      if node.name in features_dict: text= features_dict[node.name]
      if text in features_dict_label_to_color: color=features_dict_label_to_color[text]
      feature_face=TextFace(text, fgcolor=color)
      faces.add_face_to_node(feature_face, node, column = column_index, aligned = True)
      column_index+=1

#####################################################################
###########################  PROGRAM START ##########################
## ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *** ##
#####################################################################

protein2species={}              #filled with names during the execution of the program
taxonomy_lineages={}         #filed with key: species_name -> full lineage "; separated)
style_dictionary={'id':{}, 'species':{}, 'tax':{}}   ###### 

def main(args={}):
  command_line_synonyms={'t':'f', 'i':'f', 'style':'y', 'Style':'Y'}
  def_opt= {'f':'tree_inpufile.newick',  'o':'', 'C':'', 'S':0, 's':0, 'k':1, 'l':0, 'L':0,'*':[], 'p':0, 'out':'', 'ali':'', 'bsize':8, 'T':1, 'n':0, 'b':0, 'cs':0, 'ids':0, 'width':150, 'sf':None, 'st':None, 'um':0,  'tax':None, 'cl':0, 'CL':0, 'nt':0, 'ft':'Helvetica',
            'lab':0,
            'no_id':0, 'lf':0, 'scale':10, 'format':0, 'g':0, 'mc':35,  'mfd':12, 'nb':0, 'y':0, 'Y':0,
            'umn':0,
            'get_species':None, 'remove':0, 'age':0, 'img_h':None, 'img_w':None, 'v':0, 'temp':'/tmp/', 'exec':0, 
            'ali_w':150,  'ali_wpp':None, 'ali_h':10,    'ali_p':0, 
            'config':0, 'save_config':0, 'zoom':0, 'lmap':'Qualitative:Paired', 'log':0,   'ac':0, 'aco':0,
            'dry':0,
}

  config_filename=def_opt['config']
  for i in range(len(sys.argv)):
    if sys.argv[i] == "-config":     
      config_filename=sys.argv[i+1]
  if config_filename:
    def_opt.update( configuration_file(config_filename) )
    def_opt['*']=eval(def_opt['*'])
  global opt
  global all_seqs_alignment, profile_ali
  global label2image
  global label2color
  if not args: opt=command_line(def_opt, help_msg, '*', synonyms=command_line_synonyms, advanced={'full':advanced_help} )
  else:  opt=args
  set_MMlib_var('opt', opt)
  #########################################################
  ############ loading options
  if opt['save_config']:
    config_text='\n'.join([ '{} = {}'.format(k, opt[k]) for k in sorted(opt.keys()) if not (k.startswith('__') or k in set(['save_config', 'config'])   )] )
    write('Saving config --> {}'.format(opt['save_config']), 1)
    write_to_file(config_text, opt['save_config'])

  global temp_folder; temp_folder=Folder(random_folder(opt['temp'])); test_writeable_folder(temp_folder, 'temp_folder'); set_MMlib_var('temp_folder', temp_folder)
  inputfile=opt['f']; check_file_presence(inputfile, 'newick inputfile')

  ##### LOADING TREE !
  t = PhyloTree(inputfile, format=opt['format'])
  t.set_species_naming_function(  lambda x:protein2species[ x ] )
  for node in t: node.extra_faces=[]

  ############################### 
  ##### setting outgroup  
  if opt['o']:
    try:
      if "&" in opt['o']:
        outgroup= t.get_common_ancestor(   opt['o'].split('&') )   
      else:
        matches = t.search_nodes(name = opt['o'])
        outgroup=matches[0]
      write('OUTGROUP: setting with option -o -> '+opt['o'], 1)
      t.set_outgroup(outgroup);
    except:            raise Exception("ERROR setting outgroup with option -o, the node was not found: "+str(opt['o']))
  elif opt['age']:
    species2age={};       unmasked_species2age={}
    for line in open(opt['age']): 
      species2age[line.split('\t')[0]]= int( line.strip().split('\t')[1] )
      unmasked_species2age[     unmask_characters(  line.split('\t')[0].replace( '_', ' '))    ] = int( line.strip().split('\t')[1] )
    write('OUTGROUP: setting with get_age_balanced_outgroup method ... ', 1)
    try:                 outgroup=t.get_age_balanced_outgroup(species2age)
    except KeyError: 
      try:               outgroup=t.get_age_balanced_outgroup(unmasked_species2age)
      except KeyError:   
        printerr( "ERROR species not found in -age file "+opt['age'] +' ! ', 1)
        raise 
    t.set_outgroup(outgroup)
  else:
    write('OUTGROUP: setting with get_midpoint_outgroup method ... ', 1)      
    t.set_outgroup(t.get_midpoint_outgroup())
  t.ladderize()

  if opt['style'] or opt['Style']:
    unnamed_index=0
    write('Reading style specifications...', 1)
    style_text=opt['Style'] if not opt['style'] else ';'.join([line.strip() for line in open(opt['style'])])
    for piece in style_text.split(';'):      
      if not piece.strip(): continue
      which_nodes, what_style=piece.strip().split(':')
      stylespec={}
      for p in what_style.split(','):
        attribute,value=p.strip().split('=')
        if attribute=='c': attribute='bgcolor'
        value=option_value(value) #converting to int/float useful for certain attributes
        stylespec[attribute]=value
      for p in which_nodes.split(','):
        clas,value=p.strip().split('=')
        if   clas=='i': 
          if '&' in value: 
            id1,id2=value.split('&')
            anc=t.get_common_ancestor(id1, id2)
            if not anc.name: 
              anc.name='Node{}'.format(unnamed_index)
              unnamed_index+=1
            value=anc.name            
          style_dictionary['id'][value]=stylespec
        elif clas=='s': style_dictionary['species'][value]=stylespec
        elif clas=='t': style_dictionary['tax'][value]=stylespec
        else:     raise Exception("ERROR reading style failed {}  --> first bit of which_nodes part should be one of these: i s t  while it is: {}".format(style_text, clas))

  ### removing nodes if option is active
  if opt['remove']:
    write('Removing some leaf nodes from the tree... ', 1)
    ids_to_remove={}
    for line in open(opt['remove']):   ids_to_remove[line.strip()]=1
    nodes_to_keep=[]
    for node in t.traverse():
      if node.is_leaf():
        if node.name in ids_to_remove:  ids_to_remove[node.name]=0
        else: nodes_to_keep.append(node.name)
    if any( ids_to_remove.values() ):
      printerr('WARNING some nodes that were supposed to be removed were not found:\n'+join(  [an_id for an_id in ids_to_remove if  ids_to_remove[an_id] ] , '\n' ), 1   )
    t.prune(nodes_to_keep)

  #####################################################################
  #####################################################################
  #########  determining species for each node in the input protein tree
  ### checking if already computed or provided with option -tax
  if is_file(inputfile+'.tax') and not opt['tax']:  taxonomy_tab_file= inputfile+'.tax'
  else:                                             taxonomy_tab_file= opt['tax']
  if taxonomy_tab_file:
    try:
      for line in open(taxonomy_tab_file, 'r'):
        node_name, species_name, taxonomy_lineage = line[:-1].split('\t')
        protein2species[node_name]=species_name
        taxonomy_lineages[species_name]= taxonomy_lineage
    except:       printerr('ERROR parsing taxonomy file! \n{}'.format(line), 1);      raise
    for node in t:
      try: 
        if node.name not in protein2species:               
          raise Exception('ERROR species not found for node: '+node.name+' in -tax file: '+taxonomy_tab_file)
        if protein2species[node.name] not in taxonomy_lineages: raise Exception('ERROR taxonomy not found for species: '+protein2species[node.name]+' in -tax file: '+taxonomy_tab_file)
      except: 
        if not opt['g']: raise
        printerr('WARNING something missing in file {f} for node {s}'.format(f=taxonomy_tab_file, s=node.name))
        protein2species[node.name]=node.name
        taxonomy_lineages[  protein2species[node.name]  ] = 'unknown'

  else:
    ncbi_names_to_fetch={} # name_to_fetch -2-> node_name
    if not opt['sf'] is None:
      if opt['sf'].lower()=='ncbi':  species_function= lambda x:"ncbi"
      else:                         species_function=eval('lambda x:'+opt['sf'])
      for node in t:
        try:
          species= species_function(node.name)
          if opt['um']:   species= unmask_characters( species.replace( '_', ' ') )
          assert species
          if species.lower()=='ncbi':
            ncbi_names_to_fetch [node.name] = node.name
          else:
            protein2species[node.name] = species
        except: 
          printerr('ERROR species inferring function (-sf) not working on node: '+node.name, 1)
          raise
    elif not opt['st'] is None:
      for line in open(opt['st']):
        if line.startswith('#'): continue
        splt=line.strip().split('\t')
        protein_name=splt[0]; species=splt[1]
        if opt['um']:   species= unmask_characters( species.replace('_', ' ') )
        if species=='ncbi':
          ncbi_names_to_fetch [protein_name] = protein_name
        else:
          protein2species[protein_name] = species

        
      for node in t: 
        if node.name not in protein2species and node.name not in ncbi_names_to_fetch: 
          raise Exception('ERROR species not found for node: '+node.name+' in -st file: '+opt['st'])
    else:
      #### no species explicitly chosen. Trying to guess, if the title is a selenoprofiles title or a ncbi gi code
      for node in t:
        if is_selenoprofiles_title(node.name):
          masked_species= node.name.split('.')[3]
          species= unmask_characters( masked_species.replace(  '_', ' ') )
          protein2species[node.name] = species
        elif len(node.name)>3 and node.name[:3]=='gi|':    
          id_to_fetch='gi|'+node.name.split('|')[1]
          ncbi_names_to_fetch [id_to_fetch] = node.name
        else: 
          raise Exception("ERROR no species could be parsed from protein title:" +node.name)

    ## fetchin gi codes all at once
    if opt['umn']:
      ncbi_names_to_fetch={ unmask_characters(k):ncbi_names_to_fetch[k]    for k in ncbi_names_to_fetch}
    if ncbi_names_to_fetch and not opt['CL']:
        verbose('fetching species names for '+str(len(ncbi_names_to_fetch))+' proteins ... ')
        sequence_type_mode='P'
        if opt['nt']: sequence_type_mode='N'
        # write('fetching now', 1)
        # try:
        #write('\n'.join( sorted(ncbi_names_to_fetch.keys()) ) , 1)
        #print(ncbi_names_to_fetch.keys())
        fetch_output= fetch_ncbi_sequences.main({'I':   ','.join(list(ncbi_names_to_fetch.keys())), 'silent':1, 't':1, 'm':sequence_type_mode}) # #hash. 
        #   write('finished fetching', 1)
        #   write('\n'.join( [(a,b) for a,b in fetch_output.iteritems()]), 1)
        # except:
        #   raise
        
        for gi_code in list(ncbi_names_to_fetch.keys()):
          if not gi_code in fetch_output: raise Exception("ERROR could not obtain from ncbi the species from code: "+gi_code+' ; protein name: '+ncbi_names_to_fetch[gi_code])
          try: 
            species=   fetch_output[gi_code][1].split(' -> ')[-1]
            taxonomy=  fetch_output[gi_code][1].split(' -> ')[0]
          except:
            printerr('WARNING: could not fetch species / taxonomy for this entry: {}\n{}'.format(gi_code, fetch_output[gi_code][1]), 1)
            species, taxonomy='unknown', 'unknown'
                    
          protein2species[ncbi_names_to_fetch[gi_code]] = species
          if species not in taxonomy_lineages: taxonomy_lineages[species]=taxonomy

    if not opt['CL']:
      ### getting full taxonomy lineage for all species. First we try with ncbi_taxonomy_tree ; this is local and fasta but sometimes misses some entries, and we use ncbi_taxonomy (uses internet) for the rest
      species_to_fetch= sorted(list(set([ species for species in list(protein2species.values())         if species not in taxonomy_lineages ])))
      if species_to_fetch:
        write_to_file( '\n'.join(species_to_fetch), temp_folder+'species_to_fetch')
        #write(' debug: '+ temp_folder+'species_to_fetch', 1)
        verbose('getting taxonomy lineage for all species... ')
        try:
          args = ncbi_taxonomy_tree.parse_opts( '-n {0} -u --lineage --quiet -f -temp {1} '.format(temp_folder+'species_to_fetch', temp_folder) )
          lineage_annotated_tree =  ncbi_taxonomy_tree.main(args) #  TEMPORARY NO NCBI TAX TREE
          #print( lineage_annotated_tree )
        except:
          input('ERROR with ncbi_taxonomy_tree.py -n {0} -u --lineage --quiet -f -temp {1} '.format(temp_folder+'species_to_fetch', temp_folder)+ ' ... press enter to continue')
          raise 
        missing_species={}
        for species in species_to_fetch:
          try:
            unmasked_species= unmask_characters(species.replace('_', ' '))
            leaf = lineage_annotated_tree & unmasked_species
            taxonomy = '; '.join(leaf.lineage.split('||')[:-1])  #replacing || with "; " and taking off last field (species name)
            taxonomy_lineages[species]=taxonomy
          except: 
            missing_species[species]=1
        ## some were missed! fecthing online
        for species in missing_species:
          verbose('getting taxonomy lineage for missing species: '+species)
          tax_results = ncbi_taxonomy.main(  {'silent':1, 'S':species}  )
          if not len(tax_results): 
            if opt['g']: 
              printerr("WARNING can't find taxonomy entry for species: "+species, 1)  # Exception,  "ERROR can't find taxonomy entry for species: "+species              
              taxonomy_lineages[species]='unknown taxonomy'

            else: 
              #printerr("ERROR can't find taxonomy entry for species: "+species, 1)  # 
              raise Exception("ERROR can't find taxonomy entry for species: "+species)

          else:
            #print species, tax_results
            taxonomy=tax_results[list(tax_results.keys())[0]].split(': ')[1].split(' ->')[0]
            taxonomy_lineages[species]=taxonomy

      try:
          taxonomy_feature_file=inputfile+'.tax'
          taxonomy_feature_file_h=open(taxonomy_feature_file, 'w')
          for node in t:
            species_name=protein2species[node.name]
            print(node.name+'\t'+species_name+'\t'+taxonomy_lineages[species_name], file=taxonomy_feature_file_h)
          taxonomy_feature_file_h.close()
      except:      
        printerr('WARNING could not write taxonomy information file in '+taxonomy_feature_file+' ; the species and taxonomic lineages will be recomputed next time!', 1  )
        bash('rm '+taxonomy_feature_file)

  ##################### reading alignment file to be linked with the protein tree
  if opt['gff']:
    pass

  ########### labels file!
  label2image={}; label2color={}
  if opt['lab']:
    check_file_presence(opt['lab'], '-lab labels file')
    for line in open(opt['lab']):
      if not line[:-1]: continue
      splt=line.strip().split('\t')
      label2color[splt[0]]=splt[1]
      if len(splt)>2:
        label2image[splt[0]]=splt[2]    

  if not 'unknown' in  label2color:
    printerr('WARNING no default defined for "unknown" label! Please edit your -lab file', 1)
    label2color['unknown']='grey'
  ############ labels !  filling id2label
  global id2label; id2label={}
  if opt['L']:
    check_file_presence(opt['L'], 'labels feature file'); feature_file_h=open(opt['L'], 'r')
    line=feature_file_h.readline()
    while line and line[0]=='#':     line=feature_file_h.readline()
    while line:
      code, label=line[:-1].split('\t') #parsing feature file. code and label must be tab separated
      id2label[code]=label
      line=feature_file_h.readline()
    feature_file_h.close()
  else:
    if opt['lf']:
      try:      label_function=eval('lambda x:'+opt['lf'])
      except:   raise Exception("ERROR label function not valid: "+opt['lf'])
    else: 
      label_function=  lambda x:x.split()[0].split('.')[-3] ###trying selenoprofiles   lf
    for node in t:
      try:        
        label=label_function(  node.name ) or 'unknown'
        #print "LABELING", node.name, label
      except:     
        printerr("WARNING label function cannot determine label for node: "+node.name, 1)
        label='unknown'
      id2label[node.name]=label


  unassigned_labels=[label for label in sorted(set( id2label.values() ) )     if not label in label2color]
  map_type, map_name=opt['lmap'].split(':')
  colormap={}
  for strk in brewer2mpl.COLOR_MAPS[map_type][map_name]:
    colormap[int(strk)]=brewer2mpl.COLOR_MAPS[map_type][map_name][strk]
  
  if max(  colormap.keys()  )< len(unassigned_labels):
    printerr('WARNING too many labels with unassigned colors, skipping automatic label coloring', 1)
  else:    
    n_colors=len(unassigned_labels) if len(unassigned_labels) in colormap  else min( colormap.keys() )
    colormap=brewer2mpl.get_map(map_name, map_type, n_colors)
    for i, label in enumerate(unassigned_labels):
      label2color[label]=colormap.hex_colors[i]

  if opt['ali']:
    from PyQt5 import QtCore, QtGui
    #from selenoprofiles_tree_drawer import limited_p2ghit, reduce_font_if_necessary, GeneFace, set_selenoprofiles_tree_drawer_var    
    #set_selenoprofiles_tree_drawer_var('gene_brick_height', 15)
    #set_selenoprofiles_tree_drawer_var('gene_brick_width', opt['width'])    
    global_alignment=alignment(opt['ali'])
    #profile_ali=alignment()
    for title in global_alignment.titles():
      short_title=title.split()[0]
      aligned_seq=global_alignment.seq_of(title)
      try:        node=t&short_title  # --> searching the title in alignment in the tree
      except: 
        printerr( "-ali WARNING title: "+short_title+" not found in tree!", 1)
        continue
      label=id2label[short_title]
      label_color=label_to_color( label )
      color_bkg=label_color
      printed_hash= {'id':0, 'chromosome':0, 'boundaries':0, 'text':0}
      other_attributes={'height':opt['ali_h'], 'width':opt['ali_w'], 'width_per_position':opt['ali_wpp']}

      if opt['ali_p']:
        for field in opt['ali_p'].split(','):          printed_hash[field]=1


      try: # trying to infer gene structure from title        
        g=gene(); g.load_from_header(title)
        assert len(g.exons)
        if g.length() == (len(nogap(aligned_seq))+1)*3:  # sequence had the stop codon removed, trying to correct
            if   g.strand=='+':            g.exons[-1][1]-=3
            elif g.strand=='-':            g.exons[-1][0]+=3

        if g.length() != len(nogap(aligned_seq))*3:
          printerr('{} {} '.format(g.length(), len(nogap(aligned_seq))*3) , 1)
          printerr( "ERROR inferred gene length is not 3 times the length of sequence in the alignment! title: "+title+' ')

        exon_view_face=ExonViewFace(g, gaps=aligned_seq,     printed=printed_hash, colors={'bkg':color_bkg, 'outline':color_bkg}, **other_attributes)
        node.extra_faces.append(exon_view_face)
      except:
        for k in printed_hash: printed_hash[k]=0
        printerr( "-ali WARNING could not get gene coordinates from: "+title, 1)
        g=gene(chromosome='unknown', strand='+'); g.add_exon(1, len(nogap(aligned_seq)*3 ) )
        exon_view_face=ExonViewFace(g, gaps=aligned_seq,     printed=printed_hash, colors={'bkg':color_bkg, 'outline':color_bkg}, **other_attributes)
        node.extra_faces.append(exon_view_face)

    for node in t:
      if len(node.extra_faces) < 1:
        printerr( "-ali WARNING no alignment sequence found for tree node: "+node.name, 1)
        node.extra_faces.append( TextFace('') )



  """
  ### other sequences, these are dsplayed 
  if opt['seq']:
    seq_alignment=alignment(opt['seq'])
    t.link_to_alignment(alignment=seq_alignment.display(return_it=True), alg_format="fasta")
    for title in seq_alignment.titles():    
      try:
        n=t&title.split()[0]  # --> searching the title in alignment in the tree    
        n.sequence= seq_alignment.seq_of(title)
      except:        
        printerr('WARNING -seq : couldn\'t find title in alignment: '+title, 1)      """

  ####### loading custom ids
  global names_to_show; names_to_show={}
  if opt['ids']:
    for line in open(opt['ids']):      names_to_show[line.rstrip().split('\t')[0]] = line.rstrip().split('\t')[1]
  ####### loading custom species names
  global species_common_names; species_common_names={}
  if opt['cs']:
    for line in open(opt['cs']):      species_common_names[line.rstrip().split('\t')[0]] = line.rstrip().split('\t')[1]
  global custom_lineages;      custom_lineages={}
  if opt['cl'] or opt['CL']:    
    filename= opt['cl'] or opt['CL']
    if not opt['CL']==-1: 
      for line in open(filename):          custom_lineages[line.strip().split('\t')[0]]= line.strip().split('\t')[1]
    
  ################################## reading all features files
  global features_dictionaries;  features_dictionaries=[]
  global features_dictionaries_label_to_color; features_dictionaries_label_to_color=[]
  for feature_file in opt['*']:
    #parsing feature files
    check_file_presence(feature_file, 'feature_file'); feature_file_h=open(feature_file, 'r')
    code_to_label_diz={}; label_to_color_diz={}
    line=feature_file_h.readline()
    if line[0]=='#':
      #header; determining color for each label
      title=line.split('#')[1].split()[0]
      if title[0]==' ': title=feature_file
      for label_color in ' '.join(line.split(' ')[1:]).split('\t'): #parsing header of a feature file
        #print [label_color]
        label=label_color.split('#')[0][:-1] #parsing header of a feature file
        color='#'+label_color.split('#')[1]  #parsing header of a feature file
        label_to_color_diz[label]=color
      line=feature_file_h.readline() #jumping to first entry line, not commented.
    features_dictionaries_label_to_color.append(deepcopy(label_to_color_diz))
    #now parsing and adding one entry for each code found
    while line:
      code, label=line[:-1].split('\t') #parsing feature file. code and label must be tab separated
      code_to_label_diz[code]=label
      line=feature_file_h.readline()
    feature_file_h.close()
    features_dictionaries.append(deepcopy(code_to_label_diz))
    
  ########### executing commands
  if opt['exec']:
    try:
      exec(str(opt['exec']), globals(), locals())
    except Exception as e:
      write( "ERROR trying to evaluate: "+str(opt['exec'])+'; message:'+str(e), 1)
      raise

  if opt['log']:
    for n in t.traverse():            n.dist=log10(1+n.dist)

  ##########################
  ################### here we go! let's call evol events by species overlap
  ee=t.get_descendant_evol_events()
  #duplication_clusters(t)
  if opt['ac']:
    ## automatic clusters
    list_nodes2cluster, leaf2clustername=    make_clusters(t, species_fn=lambda x:protein2species[x.name], min_species_dup=opt['ac'], min_div_dist=2, min_species_div=sys.maxsize)
    if opt['aco']:
      ffw=open(opt['aco'], 'w')
      for leaf, cname in leaf2clustername.items(): print('{}\t{}'.format(leaf.name, cname), file=ffw)
      ffw.close()
    
    all_clusters=set(leaf2clustername.values())
    c1='#F0F0F0'; c2='#666666'    
    colors=[  color_scale( index/float(len(all_clusters)), c1, c2)   for index, cluster in enumerate(all_clusters)  ]
    random.shuffle(colors)
    cluster2color={ cluster: colors[index]  for index, cluster in enumerate(all_clusters)  }
    
    unnamed_index=-1
    
    for n,clust in list_nodes2cluster:
      if not n.name: 
        n.name='Node{}'.format(unnamed_index)
        unnamed_index-=1
      style_dictionary['id'][n.name]={'bgcolor':  cluster2color[clust] }

  
  tree_style=TreeStyle()
  tree_style.show_leaf_name=False
  tree_style.scale = opt['scale']
  if opt['b']: tree_style.show_branch_support=True  
  if opt['C']:
    tree_style.mode = "c" # draw tree in circular mode circular_style.scale = 20
    tree_style.allow_face_overlap = True
    tree_style.scale *= 10
    #tree_style.arc_start=270
  if opt['title']:
    tree_style.title.add_face(   TextFace(opt['title'], fgcolor='darkblue'), 0      )

  if opt['zoom']:   
    lca_nodes=opt['zoom'].split('&')
    t=t.get_common_ancestor(*lca_nodes)

  if opt['dry']:
    write('Dry run: not producing any graphics. Exiting... ', 1)
  else:
    if not opt['out']: t.show(mylayout, tree_style)
    else:              t.render(opt['out'], layout=mylayout, tree_style=tree_style, h=opt['img_h'], w=opt['img_w'])
  
  if opt['p']:     interactive_mode(message="The ete3.PhyloTree object is call t\nUse t.show(mylayout, tree_style) to display again the tree after your modifications")()

# ***** ***** ***** ***** ***** ***** ***** ***** *****
############################################################# PROGRAM END

def close_program():
  if 'temp_folder' in globals() and is_directory(temp_folder):
    bbash('rm -r '+temp_folder)
  try:
    if get_MMlib_var('printed_rchar'): 
      printerr('\r'+printed_rchar*' ' ) #flushing service msg space       
  except:
    pass

if __name__ == "__main__":
  try:
    main()
    close_program()  
  except Exception:
    close_program()
    raise 

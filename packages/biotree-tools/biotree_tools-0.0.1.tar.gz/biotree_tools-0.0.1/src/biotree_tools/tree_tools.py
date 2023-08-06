#! /usr/bin/env python3
from string import *
import sys
from subprocess import *
import ete3  #from ete3 import * 
from math import log10
from .MMlib3 import  *
#write, printerr, write_to_file

help_msg="""Generic script to manipulate trees. 

Usage: $ tree_tools.py  -i tree.nw  [-o output_tree.nw]  [options]  

### Format:
-if      newick format of input (numeric, see ete3 help)
-of      newick format of output; if not provided, same as input
-off     features exported in output, comma separated; use 'all' to use them all

### Name manipulations:
-names   change node names from this file, which must be like:  name_in_tree TAB new_name
-mask    mask characters in node names  (see MMlib.mask_characters)
-unmask  unmask characters in node names 

### Structure manipulations:
-exp     expand certain leaves by adding a sister leaf (or a cluster) at distance 0. File must have lines like: leaf_in_tree TAB leaf_add1 [leaf_addN]
-um      make ultrametric; tree length is 1.0 or the argument provided; use -1 to use max leaf distance
-log     transform branch lengths so that newDist=log10(1+dist)
-std     standardize: nodes with only one child are removed and multifurcations are automatically resolved
-prn     prune: remove leaf nodes which are not in this file list
-lca     zoom into an internal node, defined as the last common ancestor of a list (>1) of nodes. Arg: nodeName1:nodeName2
-lad     ladderize tree
-mp      set outgroup using midpoint method

### Actions:
-print   print the tree with ete
-show    show the tree with ete; if a file is provided, render to that file instead
-o       output newick to this file, using the format in -of (see above)
-on      output names of leaves to this file, one per line
-P       open IPython interactive environment at the end

### Options:
-print_opt      print currently active options
-h OR --help    print this help and exit"""

command_line_synonyms={'p':'print'}

def_opt= {'temp':'/tmp/', 
          'i':0,  'if':0, 'off':'',
          'names':0, 'exp':0, 'mask':0, 'unmask':0, 
          'um':0, 'std':0, 'lad':0, 'log':0, 'prn':0, 'lca':0,
          'print':0, 'show':0,  'C':0,
          'o':0, 'on':0, 'P':0,
          'mp':0,
          'v':0,
}


#########################################################
###### start main program function

def main(args={}):
#########################################################
############ loading options
  global opt
  if not args: opt=command_line(def_opt, help_msg, 'io', synonyms=command_line_synonyms )
  else:  opt=args
  set_MMlib_var('opt', opt)
  #global temp_folder; temp_folder=Folder(random_folder(opt['temp'])); test_writeable_folder(temp_folder, 'temp_folder'); set_MMlib_var('temp_folder', temp_folder)
  #global split_folder;    split_folder=Folder(opt['temp']);               test_writeable_folder(split_folder); set_MMlib_var('split_folder', split_folder) 
  #checking input
  input_file=opt['i'];   check_file_presence(input_file, 'input_file')
  intreeformat=opt['if'];    
  outtreeformat=intreeformat if opt['of'] is None else opt['of']
  tree=ete3.Tree(input_file, format=intreeformat)

  if opt['names']:
    dict_names={}; n_not_found_tree=0; 
    for line in open(opt['names']): 
      if not line[:-1]: continue
      splt=line.strip().split('\t')
      dict_names[splt[0]]=splt[1]
    for n in tree.traverse():
      if n.name and not n.name in dict_names: n_not_found_tree+=1
      elif n.name:   
        replacement=dict_names[n.name]
        dict_names[n.name]=None        
        n.name= replacement

    #print dict_names
    n_not_found_dict= len( [x for x in dict_names if not dict_names[x] is None ])
    if n_not_found_tree:  printerr('WARNING {n} titles in the tree were not found in {f}'.format(f=opt['names'], n=n_not_found_tree), 1)
    if n_not_found_dict:  printerr('WARNING {n} titles in {f} were not found in the tree'.format(f=opt['names'], n=n_not_found_dict), 1)
    write('-names : node names were modified from {f} '.format(f=opt['names']), 1)

  if opt['mask']:
    for n in tree.traverse():      n.name= mask_characters(n.name).replace(' ', '_')
    write('-mask : masked node names and replaced spaces with underscores', 1)

  if opt['unmask']:
    for n in tree.traverse():      n.name= unmask_characters(   n.name.replace('_', ' ') )
    write('-unmask : unmasked node names and replaced underscores with spaces', 1)

  if opt['exp']:
    repr2members={}
    for line in open(opt['exp']):
      if not line.strip(): continue
      splt=line.strip().split('\t')
      repr2members[splt[0]]=splt[1].split()

    for rep in repr2members:
      rep_node=tree&rep
      new_node=rep_node.up.add_child()
      rep_node.detach()
      new_node.add_child(rep_node)
      sisters_node=new_node.add_child()
      for sister in repr2members[rep]:
        sisters_node.add_child(name=sister)
    write('-exp : expanded nodes adding sisters from {f}'.format(f=opt['exp']), 1)

  if opt['log']:
    for n in tree.traverse():      
      n.dist=log10(1+n.dist)
    write('-log : transformed distances with log10 function', 1)

  if opt['prn']:
    names=[s.strip() for s in open(opt['prn']) if s.strip()]
    tree.prune(names, preserve_branch_length=False)
    write('-prn : pruned tree', 1)

  if opt['std']:
    tree.standardize()
    write('-std : standardized tree structure', 1)

  if opt['lad']:
    tree.ladderize()
    write('-lad : ladderized tree structure', 1)

  if opt['um']:
    tl=float(opt['um'])  # 1.0 if no argument is provided
    if tl == -1: tl=None
    tree.convert_to_ultrametric(tl)
    write('-um : converted to ultrametric, tree length= {tl}'.format(tl=tl), 1)


  if opt['mp']:
    write('-mp  : Set outgroup using midpoint method', 1)
    tree.set_outgroup(tree.get_midpoint_outgroup())

  if opt['lca']:
    lca_nodes=opt['lca'].split(':')
    tree=tree.get_common_ancestor(*lca_nodes)
    write('-lca : Zoom into the last common ancestor of {}'.format(' and '.join(lca_nodes)), 1)

#####

  if opt['print']:
    write('-print : find below the tree in ASCII format:', 1)
    print(tree)

  if opt['show']:
    tree_style=ete3.TreeStyle()
    node_style=ete3.NodeStyle()
    node_style['size']=0
    for n in tree.traverse(): n.set_style(node_style)
    if opt['C']: tree_style.mode='c'
    if opt['show']==1:  
      write('-show : Opening ete interactive environment ...', 1)
      tree.show(tree_style=tree_style)
    else:               
      write('-show : printing tree render to file {f} ... '.format(f=opt['show']), 1)
      tree.render(opt['show'], tree_style=tree_style)

  if opt['o']:
    features=None if not opt['off'] else (
        [] if opt['off']=='all' else opt['off'].split(','))      
    write_to_file(  tree.write(format=outtreeformat,
                               features=features),
                    opt['o'] )
    write('|', 1)
    write('--> Wrote output file {f} in newick format {fr}'.format(f=opt['o'], fr=outtreeformat), 1)

  if opt['on']:
    write_to_file( '\n'.join([n.name for n in tree]), opt['on'] )
    write('|', 1)
    write('--> Wrote output file {f} with leaf names'.format(f=opt['on']), 1)

  if opt['P']:
    import IPython
    IPython.embed(header='Interactive shell! Your tree is in variable -> tree ')
  
  

  

  ###############



#######################################################################################################################################

def close_program():
  if 'temp_folder' in globals() and is_directory(temp_folder):
    bbash('rm -r '+temp_folder)
  try:
    if get_MMlib_var('printed_rchar'): 
      printerr('\r'+printed_rchar*' ' ) #flushing service msg space       
  except:
    pass

  if 'log_file' in globals(): log_file.close()


if __name__ == "__main__":
  try:
    main()
    close_program()  
  except Exception:
    close_program()
    raise 

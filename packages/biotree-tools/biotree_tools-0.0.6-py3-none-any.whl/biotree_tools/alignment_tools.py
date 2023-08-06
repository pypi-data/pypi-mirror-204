#! /usr/bin/env python3
import sys
from .MMlib3 import *
import random

help_msg="""Generic script to manipulate alignments.

Usage: $ alignment_tools  -i input_ali.fa  -o output_ali.fa  [options]  

File format is normally inferred from extension. Alternatively you can use:
-if       format of input file.  Accepted: fasta,clustal,stockholm
-of       format of output file. Accepted: fasta,clustal,stockholm,phylip,codeml,slx

### Change titles / order:
-fill     fill titles from first word to complete lines using this other fasta file as dictionary
-chids    change titles, new titles are from this tabular file; format: title TAB new_title
 +use option -kids to keep the old ids (including description) after the new titles
-nids     change ids to seq1, seq2 etc. If arg is provided, it is an output tsv file of new vs old title
-pyids    change titles applying this python function to existing titles. Eg: 'x.split(".")[0]'
-com      sort by 'completeness'; top sequences will cover all the alignment 
-tree     sort titles by the order found in this tree (newick)
 +has options: [-mp | -outg | -age] & -tma & -tmt & [-mu | -md] & -nolad ;  see -help tree
-ord      sort titles from this file (one title per line). Can be also used to extract seqs
-get      same as -ord but with argument in command line. Multiple titles (first word) split by ,

### Subsets:
-repr     use trimal to get the N best representatives. you can use -clu (see below)
-maxid    use trimal to get representatives with this max identity. you can use -clu (see below)
-clu      only if -repr | -maxid; write this output file with cluster structure: title_repr TAB discarded1 discarded2 etc
-rnd      get a random sample of this many sequences 

### Change sequences:
-rem      remove empty columns (100% gaps) from the alignment
-trim     trim out the columns in the alignment with this many gaps or more (0.0 / 1.0)
-cat      concatenate with this other alignment with same titles. Use comma-separator for multiple files.
 +has option -tmcat (tolerate missing sequences from alignments) -cati (use index instead of title to match alis)
-cut      subseq the alignment in columns with this start (1-based)
 +has options: [-len | -end] & -rel ;  see -help cut
-ali      (re)-align with mafft
 +has options: -alip for processors  and  -alio for options [--auto]
-stn      standardize nucleotides; uppercase, and convert any character except AGTC- to N
-rev      reverse complement (for nucleotides)
-trn      translate (for nucleotides); the frame (1, 2 or 3) can be provided
-cons     output only consensus seq. Argument (0.0 / 1.0) defines max gaps per column to be included [def:1.0]
-ng       remove all gaps (as last step)

## other options:
-bl             block length for stockholm
-temp  +        temp folder. A folder with random name is created here, used and deleted at the end of the computation.
-P              open ipython prompt after operations, before output
-q              quiet; no messages printed on screen
-print_opt      print currently active options
-h OR --help    print this help and exit"""

cut_help="""###### -cut advanced options ######
-cut      subseq the alignment in columns. position start, 1-based
-len      length of subseq
-end      position end, overrides -len; accepts an expression using "L" as alignment length (seq length if -rel)
-rel      provide a title; subseq is relative to this sequence instead of global. -len is also relative, is provided"""
sort_tree_help="""###### -tree advanced options ######
-tree     sort titles by the order found in this tree, provided in newick format

Normally the tree is ladderized; otherwise:
-nolad     do not ladderize the tree structure

You can set an outgroup with:
-mp        set outgroup with get_midpoint_outgroup method
-outg +    set specified node as outgroup
-age +     set outgroup using get_age_balanced_outgroup method, and the provided species2age file

Normally if any alignment entries are not found in the tree or vice versa, the program prints an error; otherwise:
-tma       tolerate that there are sequences in the tree missing in the alignment; these will not be output
-tmt       tolerate that there are sequences in the alignment missing in the tree; these will not be output
-mu        put missing sequences as first in the tree (missing up) 
-md        put missing sequences as last in the tree  (missing down) """

command_line_synonyms={}

def_opt= {'temp':'/tmp/', 
'i':0, 'if':'auto', 'of':'auto',
 'chids':0, 'pyids':0, 'rem':0,  'fill':0, 'trim':0, 'mmred':0, 'com':0,
 'kids':0,  'nids':0,        
 'cat':0, 'tmcat':0, 'cati':0,
 'cut':0, 'len':0, 'end':0, 'rel':0, 
 'stn':0,
 'rev':0, 'trn':0,  'cons':None,        
 'ali':0, 'alip':0, 'alio':' --auto ',
 'tree':0, 'mp':0, 'outg':0, 'age':0, 'tma':0, 'tmt':0, 'mu':0, 'md':0, 'nolad':0,
'repr':0, 'maxid':0, 'clu':0, 'rnd':0,
          'ng':0,
          'bl':150,
          'ord':0, 'get':0,
'o':0,
'P':0, 'q':0, 
'v':0,
}


#########################################################
###### start main program function

def main(args={}):
#########################################################
############ loading options
  global opt
  if not args:
    opt=command_line(def_opt, help_msg, 'io', synonyms=command_line_synonyms, advanced={'cut':cut_help, 'tree':sort_tree_help}, strict=True )
  else:
    opt=options(def_opt)
    opt.update(args)
    
  set_MMlib_var('opt', opt)
  global temp_folder; temp_folder=Folder(random_folder(opt['temp'])); test_writeable_folder(temp_folder, 'temp_folder'); set_MMlib_var('temp_folder', temp_folder)
  #global split_folder;    split_folder=Folder(opt['temp']);               test_writeable_folder(split_folder); set_MMlib_var('split_folder', split_folder) 
  #checking input
  input_file=opt['i'];   check_file_presence(input_file, 'input_file')
  output_file=opt['o']; 

  if opt['tree']: from ete3 import Tree
  extension2format={'fa':'fasta', 'fasta':'fasta', 'ali':'fasta', 
                    'aln':'clustal', 'clustal':'clustal', 'clw':'clustal',
                    'stk':'stockholm', 'stockholm':'stockholm', 
                    'phy':'phylip', 'phylip':'phylip', 
                    'codeml':'codeml', 'cml':'codeml', 'slx':'slx'     }
  input_format=opt['if']
  if input_format=='auto':  
    suffix=input_file.split('.')[-1]
    if not suffix  in extension2format: raise Exception('ERROR automatic format detection failed with {inp}; use a different file extension or use option -if '.format(inp=input_file))
    input_format= extension2format[suffix]
  elif input_format in extension2format:   input_format=extension2format[input_format]
  
  if not input_format in list(extension2format.values()): raise Exception("ERROR format not recognized: {}".format(input_format))

  if output_file==0: #raise Exception, 'ERROR please provide an output file with -o  ; see -h'
    if not opt['q']: printerr('WARNING no output file specified!', 1)
    output_file='output.fa'

  out_format=opt['of']
  if out_format=='auto':  
    suffix=output_file.split('.')[-1]
    if not suffix in extension2format: raise Exception('ERROR automatic format detection failed with {inp}; use a different file extension or use option -of '.format(inp=output_file))
    out_format= extension2format[suffix]

  ali=alignment(); ali.load_file(input_file, format=input_format)
  if input_format=='stockholm':
    for t in ['#=GC', '#=GR']:
      if ali.has_title(t): ali.remove(t)

  if opt['q']: mute()
  write('{n} sequences loaded from file {i}'.format(n=ali.nseq(), i=input_file), 1)

  ##
  if opt['fill']:
    dict_ali=alignment(opt['fill'])
    for t in ali.titles():
      try:     new_title= dict_ali.fill_title(t)
      except:  raise Exception("ERROR this title was not found in the dictionary-like file ({f}) : {t}".format(f=opt['fill'],  t=t))
      ali.change_title(t, new_title)
    write('-fill : the titles in the alignment were filled from {f}'.format(f=opt['fill']), 1)

  ##
  if opt['chids'] or opt['nids']:
    dict_titles={}; n_not_found_dict=0; n_not_found_ali=0; 
    if opt['nids']:
      for i, t in enumerate(ali.titles()):
        st=t.split()[0]
        dict_titles[st]='seq{}'.format(i+1)
    elif opt['chids']:     
      for line in open(opt['chids']): 
        if not line[:-1]: continue
        splt=line.strip().split('\t')
        dict_titles[splt[0]]=splt[1] #join(splt[1:], '\t')
        if not ali.has_title(splt[0], even_partial=True): n_not_found_dict+=1
    for t in ali.titles():
      st=t.split()[0]
      if not st in dict_titles: n_not_found_ali+=1
      else:   
        ali.change_title(t,  '{}{}'.format(dict_titles[st], '' if not opt['kids'] else ' '+t) ) 
    if n_not_found_ali:  printerr('WARNING {n} titles in the alignment were not found in {f}'.format(f=opt['chids'], n=n_not_found_ali), 1)
    if n_not_found_dict:  printerr('WARNING {n} titles in {f} were not found in the alignment'.format(f=opt['chids'], n=n_not_found_dict), 1)
    if   opt['chids']:
      write('-chids : titles in alignment were modified from {f} {k}'.format(f=opt['chids'], k='(-kids: concatenating old titles)' if opt['kids'] else ''), 1)
    elif opt['nids']:
      if opt['nids']!=1:
        fhh=open(opt['nids'], 'w')
        for st in dict_titles:           print('{}\t{}'.format(dict_titles[st], st), file=fhh)
        fhh.close()        
      write('-nids :  titles in alignment were changed to seq1, seq2 etc   {}'.format('' if opt['nids']==1 else ' --> '+opt['nids']), 1)
    
  if opt['pyids']:
    fn=eval('lambda x:'+opt['pyids'])
    for title in ali.titles():
      newt=fn(title)
      ali.change_title(title, newt)
    write('-pyids : changed titles in alignment! Example of new title (last)={}'.format(newt, 1), 1)    

  if opt['com']:
    write('-com : sorting by completeness the sequences in the alignment', 1)
    ali.sort_by_completeness()

  ## tree sort
  if opt['tree']:
    tree_file=opt['tree'];   check_file_presence(tree_file, 'tree_file')
    t=Tree(tree_file)
    write('-tree : loaded tree from {tr} to sort titles'.format(tr=tree_file), 1)
    if opt['outg']:
      outgroup=opt['outg']
      matches = t.search_nodes(name = outgroup)
      if len(matches) > 0:
        write('OUTGROUP: setting with option -outg -> '+outgroup, 1)
        t.set_outgroup(matches[0]);
      else:            raise Exception("ERROR setting outgroup with option -outg, the node was not found: "+str(outgroup))
    elif opt['age']:
      species2age={};       unmasked_species2age={}
      for line in open(opt['age']):
        species2age[line.split('\t')[0]]= int( line.strip().split('\t')[1] )
        unmasked_species2age[     unmask_characters(  replace(  line.split('\t')[0] , '_', ' '))    ] = int( line.strip().split('\t')[1] )
        write('OUTGROUP: setting with get_age_balanced_outgroup method ... ', 1)
        try:                 outgroup=t.get_age_balanced_outgroup(species2age)
        except KeyError:
          try:               outgroup=t.get_age_balanced_outgroup(unmasked_species2age)
          except KeyError:
            printerr( "ERROR species not found in -age file "+opt['age'] +' ! ', 1)
            raise
        t.set_outgroup(outgroup)
    elif opt['mp']:
        write('OUTGROUP: setting with get_midpoint_outgroup method ... ', 1)
        t.set_outgroup(t.get_midpoint_outgroup())
    if not opt['nolad']: t.ladderize()
    input_titles={}
    for tit in ali.titles(): input_titles[tit]=0
    b=alignment()
    for n in t:
      title=ali.fill_title( n.name, silent= True ) # this will raise an exception if the node name is not found in the alignment
      if not title:
        if opt['tma']: 
          #printerr("WARNING tree node "+n.name+ " not found in alignment. skipping this... ", 1)
          continue
        else: raise Exception("ERROR tree node "+n.name+ " not found in alignment!")
      b.add(title, ali.seq_of(title))
      input_titles[title]=1
    if not  all( input_titles.values() ):
      unmatched_titles=[ tit.split()[0] for tit in input_titles if not input_titles[tit]   ]
      #if opt['tmt']:   printerr("WARNING "+str(len(unmatched_titles))+ " entries were not found in the tree and are not reported in output!", 1)
      if opt['mu']: 
        for title in ali.titles()[::-1]:
          if not input_titles[title]:          b.add(title, ali.seq_of(title), index=0)
      elif opt['md']:
        for title in ali.titles():
          if not input_titles[title]:          b.add(title, ali.seq_of(title))
      elif not opt['tmt']:          raise Exception("ERROR these alignment entries were not found in the tree: \n"+'\n'.join(unmatched_titles))
    copy_attrs(ali, b)
    ali=b  
  #### tree sort stop

  ##
  if opt['ord'] or opt['get']:
    if opt['ord']:
      write('-ord : sorting/fetching sequences based on titles on file {}'.format(opt['ord']), 1)
      sorted_titles=[line.strip() for line in open(opt['ord']) if line.strip()]      
    if opt['get']:
      write('-get : sorting/fetching sequences based on command line argument {}'.format(opt['get']), 1)
      sorted_titles=opt['get'].split(',')
    b=alignment()
    found_titles={ t:0 for t in ali.titles()}
    for st in sorted_titles:
      full_title=ali.fill_title(st)
      b.add(   full_title,   ali.seq_of(full_title)    )
      found_titles[full_title]=1
    if not b.nseq():                       raise Exception("ERROR empty alignment after -ord or -get filtering. None of {} seqs were found in {} ({} titles)".format(ali.nseq(), opt['ord'], len(sorted_titles)))
    if not all(found_titles.values()) and opt['ord']:     printerr('WARNING  {} titles were not found in {} and were dropped'.format(len([x for x in list(found_titles.values()) if not x]), opt['ord']), 1)
    copy_attrs(ali, b)
    ali=b
      
  ####
    ##
  if opt['clu'] and not (opt['repr'] or opt['maxid']): raise Exception('ERROR option -clu if available only if you used -repr or -maxid !')
  if opt['repr'] and opt['maxid']: raise Exception('ERROR you cannot specify both options -repr and -maxid !')
  if opt['repr'] and opt['repr'] >= ali.nseq(): printerr('WARNING -repr : the alignment contains fewer or the same number of sequences than requested. Leaving it as it is...', 1)
  elif opt['repr'] or opt['maxid']:
    #### using trimal; wrapping it
    #encode alignment
    id2title={}
    tfile=temp_folder+'temp_ali.fa'         
    fh=open(tfile, 'w'); 
    tfile_out=temp_folder+'temp_ali.post.fa'; 
    temp_identities=temp_folder+'identities' 
    for index, title in enumerate(ali.titles()): print('>seq{index}\n{s}'.format(index=index, s=ali.seq_of(title)), file=fh); id2title['seq'+str(index)]=title
    fh.close()
    nseq_before=ali.nseq()
    del ali #free memory
      
    if opt['repr']:
      if not type(opt['repr'])==int or opt['repr']==1: raise Exception("ERROR invalid value provided for option -repr !")
      write('-repr : selecting {r} (approx) best representative sequences with trimal'.format(r=opt['repr']), 1)
      
      trimal_cmnd='trimal -in {inp} -out {out} -clusters {n} -sident > {ident} '.format(inp=tfile, out=tfile_out, n=opt['repr'], ident=temp_identities)

    if opt['maxid']:
      if not type(opt['maxid'])==float or opt['maxid']==1: raise Exception("ERROR invalid value provided for option -maxid !")
      write('-maxid : selecting representative sequences to a resulting max identity of {s}'.format(s=opt['maxid']), 1)
      trimal_cmnd='trimal -in {inp} -out {out} -maxidentity {n} -sident > {ident} '.format(inp=tfile, out=tfile_out, n=opt['maxid'], ident=temp_identities)

    #raw_input(trimal_cmnd)
    bbash(trimal_cmnd)  
    ali=alignment(); found={}
    for tid, seq in parse_fasta(tfile_out):
      tit=id2title[tid]
      ali.add(tit , seq  )
      found[tit]=True
      
    if opt['clu']:
      if opt['clu']==1: raise Exception('ERROR option -clu requires an output file as argument!')

      matrix_started=False
      seqid_matrix={}
      for line in open(temp_identities):
        if matrix_started:
          if not line.strip(): break
          s=line.strip().split()
          #id1=s[0]
          tit1=id2title[  s[0]  ] #.split()[0]
          seqid_matrix[tit1]={}
          #seqid_matrix[id1]={}
          for i,v in enumerate(s[1:]):
            id2='seq{}'.format(i)
            tit2=id2title[  id2  ]  #.split()[0]
            seqid_matrix[tit1][tit2]=float(v)
            #seqid_matrix[id1][id2]=float(v)
        elif line.startswith('#') and 'Identity sequence' in line: matrix_started=True          

      kept2discarded={};          
      for id1 in id2title:
        tit1=id2title[id1] #.split()[0]
        if not tit1 in found:
          kept=None
          #try: 
          for tit2 in   sorted(   list(seqid_matrix[tit1].keys()), key= lambda x:seqid_matrix[tit1][x], reverse=True):
              if tit2 in found:
                kept=tit2 #id2title[id2].split()[0]
                break
          #except:
          #  print '\n'.join(  seqid_matrix.keys()  )
          #  raw_input(temp_identities)
          #  raise
          if not kept in kept2discarded:    kept2discarded[kept]=[]
          kept2discarded[kept].append(tit1)
        
      # kept2discarded={};  
      # most_similar_lines_started=False
      # for line in open(temp_identities):
      #   if most_similar_lines_started:
      #     if line[:-1]: 
      #       tit1, seqid, tit2 = line.strip().split()
      #       if not tit1 in found: 
      #         short_title=id2title[tit2].split()[0]
      #         if not short_title in kept2discarded: kept2discarded[short_title]=[]
      #         kept2discarded[short_title].append(id2title[tit1].split()[0])
      #   elif line=='## Identity for most similar pair-wise sequences matrix\n':  most_similar_lines_started=True
        


      fh=open(opt['clu'], 'w')
      for kept in  kept2discarded:         print(kept + '\t' + ' '.join(kept2discarded[kept]), file=fh)
      fh.close()
    write('         N of sequences {}  ->  {}'.format(nseq_before, ali.nseq()), 1)


  if opt['rnd']:
    write('-rnd  : sampling {} random sequences'.format(opt['rnd']), 1)
    nseqs=opt['rnd']
    if nseqs > ali.nseq():
      printerr('WARNING -rnd requested more sequences than those in the alignment; leaving alignment as is', 1)
      nseqs=ali.nseq()  #unnecessary
    newali=alignment()
    indices=[i for i in range(ali.nseq())]
    random.shuffle(indices)
    keep_these=set(  indices[:nseqs]  )
    for index, title in enumerate(ali.titles()):
      if index in keep_these:
        newali.add(title, ali.seq_of(title))
    ali=newali
    
  ### 
  if opt['rem']:
    n_removed=len(  ali.remove_empty_columns()     )
    write('-rem : {n} only gap columns were removed from the alignment'.format(n=n_removed), 1)

  ##
  if opt['trim']:
    out_trim= ali.trim_columns( 1.0 - opt['trim'] )
    if out_trim:       write('-trim : {n} columns were removed from the alignment'.format(n=len(out_trim)), 1)

  ##
  if opt['mmred']:
    nseq_before=ali.nseq()
    ali.remove_redundancy( opt['mmred'], inplace=True, silent=not opt['v'])
    nseq_removed= nseq_before - ali.nseq()    
    if nseq_removed:       write('-mmred : {n} sequences were removed from the alignment'.format(n=len(nseq_removed)), 1)

  ##
  if opt['cat']:
    for other_file in opt['cat'].split(','):
      second_ali=alignment(other_file)
      if opt['cati']:
        t1s=ali.titles();          t2s=second_ali.titles();  
        if len(t1s)!=len(t2s): raise Exception("ERROR -cati can be used only with alignments with the same number of sequences")
        for i, title1 in enumerate(t1s):
          second_ali.change_title(t2s[i], title1)
          
      else:
        s1=set(ali.titles());       s2=set(second_ali.titles())
        if s1!=s2 and opt['tmcat']:
          if s1.issubset(s2):   
            for t in s2.difference(s1): ali.add(t, '-'*ali.length())
          elif s2.issubset(s1):   
            for t in s1.difference(s2): second_ali.add(t, '-'*second_ali.length())
        #else:  --> exception will be raised next

      ali.concatenate_with(second_ali, inplace=True)
      cols_added=second_ali.length()
      if cols_added:       write('-cat : {n} columns were concatenated from the alignment {f}'.format(f=opt['cat'], n=cols_added), 1)

  ##
  if opt['cut']:
    start=opt['cut']
    if not opt['len'] and not opt['end']:       opt['end']='L'
    len_seq=  opt['len'] #if opt['len'] else 1
    if opt['end']: 
      opt['end']=str(opt['end'])
      L=ali.length()
      len_seq= eval(opt['end']) - start + 1 
    if opt['rel']:
      title=ali.fill_title(opt['rel'])
      start=ali.position_in_ali(title, start)
      if opt['end']: 
        L  =len(nogap(ali.seq_of(title)))
        len_seq= ali.position_in_ali(title, eval(opt['end']))  - start + 1
    ali.columns(position=start-1, length=len_seq, inplace=True, remove_empty_seqs=True)
    write('-cut : cut columns of alignment successful; ali start={s} len={l} '.format(s=start, l=len_seq), 1)

  ##
  if opt['ali']:
    mafft_options=opt['alio']
    if opt['alip']:    mafft_options+=' --thread {n} '.format(n=opt['alip'])
    if ali.nseq()>1:
      ali.realign(inplace=True, mafft_options=mafft_options)
      write('-ali : (re)alignment with mafft successful!', 1)     
    else: 
      write('WARNING skipping -ali : there are less than two sequences!', 1)     
      

  ##
  if opt['stn']:
    global count_changed
    count_changed=0
    def convert_seq(seq):      
      global count_changed
      out='';  accepted_chars=dict.fromkeys('ACGT-N')
      sseq=seq.upper().replace('U', 'T')
      for s in sseq:
        #s=upper(s)
        if not s in accepted_chars: s='N'; count_changed+=1
        out+=s
      return out
    ali.convert_sequences(convert_seq)
    write('-stn : Standardize nucleotide sequences, {n} characters changed to N'.format(n=count_changed), 1)     

  ##
  if opt['rev']:
    write('-rev : Reverse complement nucleotide sequences', 1)     
    ali.convert_sequences( reverse_complement )

  ##
  if opt['trn']:
    frame=opt['trn']-1
    if frame: ali.columns(frame, length=  ali.length()-frame, inplace=True)
    write('-trn : Translate nucleotide sequences; frame: {f}'.format(f=frame+1), 1)      
    ali=ali.translate()

  ##
  if not opt['cons'] is None:
    write('-cons : Compute consensus sequence with gap threshold {}'.format(opt['cons']), 1)
    consensus_seq=    ali.consensus_sequence(threshold=opt['cons']) #, sec_char='', exclude={})
    ali=alignment()
    ali.add('consensus', consensus_seq)
        
  ##  
  if opt['ng']:
    write('-ng  : un-aligning sequences (removing gaps)', 1)
    ali.convert_sequences( lambda x:x.replace('-', '') )
    

  if opt['P']:
    import IPython
    IPython.embed(header='Interactive shell! Your alignment is in variable -> ali ')

  if   out_format=='fasta':       ali.display(                         output_file )
  elif out_format=='clustal':     write_to_file( ali.clustal_format(), output_file )
  elif out_format=='stockholm':   write_to_file( ali.stockholm(opt['bl']),      output_file )    
  elif out_format=='phylip':      write_to_file( ali.phylip_format(),  output_file )      
  elif out_format=='codeml':      write_to_file( ali.codeml_format(),  output_file )    
  elif out_format=='slx':         write_to_file( slx_format(ali),      output_file )    
  write('|', 1)
  write('--> Wrote output file {f} in format {fr}'.format(f=output_file, fr=out_format), 1)
  
  ###############

def copy_attrs(ali, b):
  if hasattr(ali, 'ss'):  b.ss=ali.ss
  if hasattr(ali, 'rf'):  b.rf=ali.rf
  
def slx_format(ali):
  out=''
  nchars_st=max( [len(t.split()[0]) for t in ali.titles()] )
  for t in ali.titles():
    st=t.split()[0]
    seq=ali.seq_of(t).upper().replace('-', ' ')
    out+='{:<{n}}  {}\n'.format(st, seq, n=nchars_st)
  return out
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

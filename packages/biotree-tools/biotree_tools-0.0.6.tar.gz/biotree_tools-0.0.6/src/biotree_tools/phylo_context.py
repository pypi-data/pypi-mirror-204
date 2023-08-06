#! /usr/bin/env python3
#from string import *
import sys, os, shlex, subprocess
from easyterm import *
from Bio import SeqIO
from glob import glob
from . import alignment_tools


##### catching up from MMlib
def parse_fasta(filename):
  with open(filename) as fh:
    for title, seq in SeqIO.FastaIO.SimpleFastaParser(fh):
      yield (title, seq)

def fasta(seq):
  return '\n'.join(  [chunk for chunk in seq[::60] ] )

def bbash(cmnd, print_it=0,  out=None, err=None, tolerate=False, shell=False):
  if out is None and err is None:
    out=subprocess.PIPE
    err=subprocess.STDOUT
  elif out is None or err is None:
    raise Exception('bbash ERROR if you specify out then specify err too')
  p=subprocess.run( shlex.split(cmnd),
                  stdout=out, stderr=err,
                    check=False, shell=shell)
  o=p.stdout  
  if not tolerate and p.returncode!=0:
    if o:
      raise Exception("bbash ERROR command: {} error: {}".format(cmnd, o.decode(encoding = 'utf-8')))
    else: 
      raise Exception("bbash ERROR command: {} error --> check {}".format(cmnd, o.__file__))
  if o:
    return o.decode(encoding = 'utf-8')
  else:
    return o

help_msg=""" Program to build and draw a tree for a set of proteins together with their most similar annotated proteins identified by blast against a target DB.

Usage:  phylo_context  -i protein_sequences.fasta  -o output_prefix  -db protein_db.fa

* Compulsory I/O:

-i    path to input protein sequences in fasta format
-db   path to blast protein database, must be already formatted with makeblastdb
-o    this argument will be used as prefix for all output files

* You must also include one of these options:
-st    file defining species name for each sequence id; such as 'Homo sapiens'  or 'Homo_sapiens'
        format:  seqid -tab- species
-sf    python code to derive species from sequence id; example: x.split('.')[3]
Note that the species label 'ncbi' can be used to fetch species name online; it works for NCBI ids

* All these routines are executed sequentially:
B = Blastp+ of all proteins against a reference database (ncbi NR recommended)
 -mts  Maximum number of aligned sequences to keep  [6000]
 -rem  Run blastp remotely; please use -db nr (or another accepted db name) with this

P = Parse blastp output and fetch proteins from reference database
 -e    evalue filter of blast hits              [1e-5]
   
R = align "context" proteins (those matched in ref db) and Reduce them to a feasible number
 -m    maximum amount of context proteins       [300]

T = run ete3 build Tree phylogeny on the ali of input and context proteins
 -w    ete3 workflow                            [phylomedb4]
 -c    run with --clear (instead of --resume)

F = build tree figures, one with context protein descriptions and one without
 -nf   do not build figures (just show the command)

Force recomputing any given routine by using the corresponding option: 
 e.g. -B to recompute blastp (and everything after that).

This options allows to reutilize useful output from a previous run:
-load  prev_out_prefix
When using -load, you HAVE to provide the routine option corresponding to where to restart from 
 e.g. -R to not recompute blast, but do recompute context proteins, tree and figures

### other options:
-dr            do not run anything, but print commands    **** not supported !
-n              number of threads used for blastp and mafft   [20]
-print_opt      print currently active options
-h OR --help    print this help and exit"""

command_line_synonyms={}

def_opt= {'temp':'/tmp', 
          'i':'', 'o':'',
          'B':False, 'P':False, 'R':False, 'T':False, 'F':False,
          'db':'undefined_DB',   'e':1e-5,  'n':20, 
          'm':300,     'mts':6000,
          'rem':False,
          'w':'standard_trimmed_fasttree',    
          'dr':False,   'c':False, 'nf':False,
          'load':False,
          'st':'', 'sf':'',
}



#########################################################
###### start main program function
how_routine =''
how_found   ='' #green'
how_main    ='blue'
how_commands='magenta'
how_info=    'yellow'


def main(args={}):  
#########################################################
############ loading options
  if not args:
    opt=command_line_options(def_opt, help_msg, '', synonyms=command_line_synonyms )
  else:
    opt=args
  temp_folder=random_folder(opt['temp'])

  ############################################################
  #### to do:
  #     -check n sequences, warning or stop
  #     -options of ete  clearall or resume
  #     -show tree (and previous = style etc)

  def run(cmnd, *args, **kargs):
    write(cmnd, how=how_commands)
    if not opt['dr']:
      return bbash(cmnd, *args, **kargs)

  input_file=opt['i'];   check_file_presence(input_file, 'input_file')
  db_file=opt['db'];     #check_file_presence(db_file, 'db_file')
  #output_folder=Folder(opt['o'])
  evalue_threshold=opt['e']
  n_threads=opt['n']
  max_seqs=opt['m']
  ete3_workflow=opt['w']
  max_target_seqs=opt['mts']
  load_prefix=('/auisbdUnMatchathackjacble' if not opt['load'] else opt['load']  ).rstrip('.')+'.'

  if opt['o']:    output_prefix=opt['o']
  else:
    x='.'.join(os.path.basename(input_file).split('.')[:-1]) if os.path.basename(input_file).count('.') else os.path.basename(input_file)
    output_prefix='{}/{}.'.format( os.path.dirname(input_file) or  '.', x)
  if not output_prefix.endswith('.'): output_prefix+='.'

  #log_fileh=open('{}phylo_context.log'.format(output_prefix), 'w')
  log_file='{}phylo_context.log'.format(output_prefix)
  set_logfile(log_file)
  write('# ++++++++++++++++++ phylo_context  ++++++++++++++++++ #',  how=how_main)
  write('# start date: {}'.format(bbash('date'))) #, how=how_main)
  write(opt)

  ## checking for duplicates; also, keeping titles (first word) in stitles
  stitles={}
  some_dups=False
  txt_no_dups=''
  for t,seq in parse_fasta(input_file):
    splt=t.split()
    st=splt[0]
    if st in stitles:
      some_dups=True
      i=2
      nt='{}{}'.format(st, i)
      while nt in stitles:
        i+=1
        nt='{}{}'.format(st, i)
      stitles[nt]=st
      st=nt
    else:
      stitles[st]=None
    txt_no_dups+='>{}\n{}\n'.format( ' '.join( [st]+splt[1:] ),   fasta(seq) )
  if some_dups:
    no_dups_file='{}no_dups.fa'.format(output_prefix)
    dups_tsv='{}dups.tsv'.format(output_prefix)
    write('WARNING duplicate titles were detected! removing them. -->  {}    old/new titles  -->  {}'.format(no_dups_file, dups_tsv))
    with open(no_dups_file, 'w') as fh:
      fh.write(txt_no_dups)

    with open(dups_tsv, 'w') as fh:
      fh.write( '\n'.join(['{}\t{}'.format(st, stitles[st])   for st in stitles if not stitles[st] is None]) )

    input_file=no_dups_file    


  if opt['st']:
    seqid2species={s:None  for s in stitles}    
    for line in open(opt['st']):
      seqid, species=line.strip().split('\t')
      if not seqid in seqid2species:
        raise Exception(f"-st file ERROR id not found in sequence file: {seqid}")
      seqid2species[seqid]=species
    not_found=[seqid for seqid in seqid2species if seqid2species[seqid] is None]
    if len(not_found):
      raise Exception(f"-st file ERROR ids not covered:  {' '.join(not_found)}")    
  elif opt['sf']:
    species_function=eval('lambda x:'+opt['sf'])
    seqid2species={s:species_function(s)    for s in stitles}
  else:
    raise Exception("ERROR you must specify option -st or -sf")


  ## routine options
  sequential_routines='BPRTF';  forcing=False
  for r in sequential_routines:
    if opt[r]:    forcing=True
    elif forcing: opt[r]= True

  n_input_seqs=int(bbash('grep -c ">" {}'.format(input_file)))
  write('# input sequences: {}'.format(n_input_seqs), how=how_info)  

  ### add controls! n of seqs vs n of context

  write('#### routine: BLAST        ######', how=how_routine)
  blast_output='{}blastp'.format(output_prefix)
  temp_blast_output='{}blastp.temp'.format(output_prefix)
  load_blast_output='{}blastp'.format(load_prefix)
  if not os.path.isfile(blast_output) or opt['B']:
    if os.path.isfile(load_blast_output) and not opt['B']:
      load_rel_path=smartlink(load_blast_output, blast_output)
      write('# <- link: {} to {}'.format(load_rel_path, blast_output), how=how_found)
      os.symlink(load_rel_path, blast_output)
    else:
      check_file_presence(db_file, 'db_file')
      blast_cmd='blastp -max_target_seqs {maxs}  -db {d} -query {q} -out {to} -outfmt 6 {remote} -num_threads {nt}'.format(
        d=db_file, q=input_file, to=temp_blast_output, nt=n_threads, maxs=max_target_seqs,
        remote='-remote' if opt['rem'] else '')
      run(blast_cmd)
      run('mv {to} {o}'.format(to=temp_blast_output, o=blast_output) )
  else:
    write('# <- found: {}'.format(blast_output), how=how_found)


  write('#### routine: PARSE        ######', how=how_routine)
  blast_ids='{}hits.ids'.format(output_prefix)
  temp_blast_ids='{}hits.ids.temp'.format(output_prefix)
  blast_fasta='{}hits.fa'.format(output_prefix)
  temp_blast_fasta='{}hits.fa.temp'.format(output_prefix)
  load_blast_ids='{}hits.ids'.format(load_prefix)
  load_blast_fasta='{}hits.fa'.format(load_prefix)
  if not os.path.isfile(blast_fasta) or opt['P']:
    if os.path.isfile(load_blast_fasta) and not opt['P']:
      load_rel_path=smartlink(load_blast_fasta, blast_fasta)
      write('# <- link: {} to {}'.format(load_rel_path, blast_fasta), how=how_found)
      os.symlink(load_rel_path, blast_fasta)
      load_rel_path=smartlink(load_blast_ids, blast_ids)
      write('# <- link: {} to {}'.format(load_rel_path, blast_ids), how=how_found)
      os.symlink(load_rel_path, blast_ids)
    else:
      check_file_presence(db_file, 'db_file')
      parse_cmd='''gawk '$(NF-1)<{e} {{ print $2 }}' {i} '''.format(i=blast_output,  e=evalue_threshold )
      with open(temp_blast_ids, 'w') as fh:
          fh.write(   '\n'.join( [i  for i in    set( run(parse_cmd).split('\n') )    if i] )   +'\n')

      run('mv {to} {o}'.format(to=temp_blast_ids, o=blast_ids))
          
      fetch_cmd='blastdbcmd -db {d} -entry_batch {i} -out {to}'.format(i=blast_ids, d=db_file, to=temp_blast_fasta)
      run(fetch_cmd)
      run('mv {to} {o}'.format(to=temp_blast_fasta, o=blast_fasta))
  else:
    write('# <- found: {}'.format(blast_ids), how=how_found)
    write('# <- found: {}'.format(blast_fasta), how=how_found)
    
  n_context_seqs=int(bbash('wc -l {}'.format(blast_ids)).split()[0])
  write('# blast hits: {}'.format(n_context_seqs), how=how_info)  

  write('#### routine: REDUCE       ######', how=how_routine)
  context_sequences='{}context.fa'.format(output_prefix)
  ali_w_context='{}w_context.fa'.format(output_prefix)
  if n_context_seqs>max_seqs:
    mafft_out='{}hits.mft.fa'.format(output_prefix)
    mafft_temp='{}hits.mft.temp'.format(output_prefix)
    reduce_out='{}hits.mft.r{}.fa'.format(output_prefix, max_seqs)
    reduce_temp='{}hits.mft.r.temp.fa'.format(output_prefix)
    load_mafft_out='{}hits.mft.fa'.format(load_prefix)
    load_reduce_out='{}hits.mft.r{}.fa'.format(load_prefix, max_seqs)
    
    if not os.path.isfile(reduce_out) or opt['R']:
      if os.path.isfile(load_reduce_out) and not opt['R']:
        load_rel_path=smartlink(load_mafft_out, mafft_out)
        write('# <- link: {} to {}'.format(load_rel_path, mafft_out), how=how_found)
        os.symlink(load_rel_path, mafft_out)
        load_rel_path=smartlink(load_reduce_out, reduce_out)
        write('# <- link: {} to {}'.format(load_rel_path, reduce_out), how=how_found)
        os.symlink(load_rel_path, reduce_out)
        
      else:      

        #mafft_cmd='align_with_mafft.py {i} -temp {tmp}  -n {nt} > {to} && mv {to} {o}'.format( i=blast_fasta, nt=n_threads, to=mafft_temp, o=mafft_out, tmp=temp_folder)
        with open(mafft_temp, 'w') as fh:
          mafft_cmd='mafft --anysymbol --auto --thread {nt} {i}'.format( i=blast_fasta, nt=n_threads)        
          run(mafft_cmd, out=fh, err=subprocess.DEVNULL)
        run('mv {to} {o}'.format(to=mafft_temp, o=mafft_out))
        
        #reduce_cmd='alignment_tools -temp {tmp}  -i {i} -repr {m} -o {to}'.format(i=mafft_out, m=max_seqs, to=reduce_temp, tmp=temp_folder)
        #run(reduce_cmd)
        alignment_tools.main({'temp':temp_folder, 'i':mafft_out, 'repr':max_seqs, 'o':reduce_temp})
        
        run('mv {to} {o}'.format(to=reduce_temp, o=reduce_out))

        link_cmd='ln -fs {} {}'.format(os.path.basename(reduce_out), context_sequences)
        run(link_cmd)
        #cat_cmd='nogap.g {} {} > {}'.format(input_file, context_sequences, ali_w_context)
        with open(ali_w_context, 'w') as fh:
          for ffile in [input_file, context_sequences]:
            for t,seq in parse_fasta(ffile):
              fh.write(f">{t}\n" + fasta(seq.replace('-', '')) + "\n")
          #run('nogap.g {} {}'.format(), out=fh, err=fh)

    else:
      write('# <- found: {}'.format(mafft_out), how=how_found)
      write('# <- found: {}'.format(reduce_out), how=how_found)

  else:
    write('# reduce routine not necessary', how=how_info)
    if not os.path.isfile(ali_w_context) or opt['R']:
      link_cmd='ln -fs {} {}'.format(os.path.basename(blast_fasta), context_sequences)
      run(link_cmd)
      with open(ali_w_context, 'w') as fh:
        for ffile in [input_file, context_sequences]:
          for t,seq in parse_fasta(ffile):
            fh.write(f">{t}\n" + fasta(seq.replace('-', '')) + "\n")
        # run('nogap.g {} {}'.format(input_file, context_sequences), out=fh, err=fh)


  ete_option='--resume'  if not opt['c'] else '--clearall'
  
  write('#### routine: TREE        ######', how=how_routine)
  ete_out_folder='{}{}'.format(output_prefix, ete3_workflow)
  if not os.path.isdir(ete_out_folder):
    os.mkdir(ete_out_folder)
  
  ete_tree_link= '{}tree'.format(output_prefix)
  ete_log='{}/ete_build.log'.format(ete_out_folder)
  load_ete_tree_link='{}tree'.format(load_prefix)
  
  if not os.path.isfile(ete_tree_link) or opt['T']:
    if os.path.isfile(load_ete_tree_link) and not opt['T']:
      load_rel_path=smartlink(load_ete_tree_link, ete_tree_link)
      write('# <- link: {} to {}'.format(load_rel_path, ete_tree_link), how=how_found)
      os.symlink(load_rel_path, ete_tree_link)
    else:    
      build_cmd='ete3 build --noimg {x} -w {w} -a {a} -o {o} -v 1'.format(w=ete3_workflow, a=ali_w_context, o=ete_out_folder, x=ete_option)
      with open(ete_log, 'w') as fh:
        run(build_cmd, out=fh, err=fh, tolerate=True)

      last_lines_of_log=run('tail -n 30 {}'.format(ete_log))
      if not 'The following published software and/or methods were used.' in last_lines_of_log:
        raise Exception('ERROR ete3 failed, check: {}'.format(ete_log))
      
      dest_file=glob('{}/*/*.w_context.fa.final_tree.nw'.format(ete_out_folder))[0]
      link_cmd='ln -fs {} {}'.format(    smartlink(dest_file, ete_tree_link),     ete_tree_link)
      run(link_cmd)
  else:
    write('# <- found: {}'.format(ete_tree_link), how=how_found)

  write('#### routine: FIGURES      ######', how=how_routine)
  species_file=   '{}id2species'.format(output_prefix)
  desc_file=      '{}desc'.format(output_prefix)
  style_file=     '{}style'.format(output_prefix)
  figure_w_desc=  '{}tree.2.pdf'.format(output_prefix)
  figure_no_desc= '{}tree.pdf'.format(output_prefix)
  tax_file=       '{}tree.tax'.format(output_prefix)
  tax_temp=       '{}tree.tax.tmp'.format(output_prefix)
  
  with open(species_file, 'w') as fh:
    write(f'# writing -> {species_file}')
    fh.write('\n'.join( [s+'\t'+seqid2species[s]   for s in   seqid2species] ) +'\n' )
    fh.write('\n'.join( [title.split()[0]+'\tncbi' for title, seq in parse_fasta(context_sequences)]) +'\n')
  
  if not os.path.isfile(figure_w_desc) or opt['F']:
    desc_cmd='''gawk '/>/{{print substr($1, 2) "\\t" substr($0, length($1)+1, {n})}}' {i}'''.format(n=60, i=context_sequences)
    with open(desc_file, 'w') as fh:
      run(desc_cmd, out=fh, err=fh)
    style_cmd='''gawk '/>/{{print "i="substr($1, 2)":c={c}"}}' {i} '''.format(c='lightblue', i=input_file)
    with open(style_file, 'w') as fh:
      run(style_cmd, out=fh, err=fh)
    show_1_cmd='''show_tree.py -f {t} -y {s} -C -lf ' "a" ' -no_id -nb 1 -k {k} -st {st} -g -out {o}  '''.format(t=ete_tree_link, s=style_file, k=2, o=figure_no_desc, st=species_file)
    if not opt['nf']:

      try:    run(show_1_cmd)
      except: write('# ERROR show_tree.py did not work! Is a display available? -- attempting to continue')
      if not os.path.isfile(tax_file) and not opt['dr']:
        write("# weird error with getting tax. going one by one... ")
        tax_remedy_cmd='''for x in $(gawk '/>/{{print substr($1, 2)}}' {c} ); do fetch_ncbi_sequences.py -I $x -m P -t -M -L | gawk -F"\t" '{{$1=substr($1, 2); split($2, A, " -> "); $2=A[2]; $3=A[1]; OFS="\t"; print}}'  ; done > {to}; for x in $(gawk '/>/{{print substr($1, 2)}}' {i} ); do s=$(echo $x | gawk -F. '{{print $4}}'); echo ${{x}}%%%${{s}}%%%$(ncbi_taxonomy.py -S $s) | sed 's/%%%/\\t/g' >> {to}; done'''.format(c=context_sequences, i=input_file, to=tax_temp)        
        run(tax_remedy_cmd, shell=True)
        run('mv {to} {o}'.format(o=tax_file, to=tax_temp) )
        write("# repeating show tree command ...")
        run(show_1_cmd)
    else: write(show_1_cmd)       
        
    show_2_cmd='''show_tree.py -f {t} -y {s} -C -lf ' "a" ' -no_id -nb 1 -k {k} -st {st} -g -out {o} {d}'''.format(t=ete_tree_link, s=style_file, k=2, d=desc_file, o=figure_w_desc, st=species_file)
    if not opt['nf']:
      try:    run(show_2_cmd)
      except: write('# ERROR show_tree.py did not work! Is a display available? -- attempting to continue')
    else: write(show_2_cmd)

    





  write('#   end date: {}'.format(bbash('date'))) #, how=how_main)


  ###############




def smartlink(source, dest):
  """ Return the path that should be used to link source to dest accounting for relative paths """
  abs_source=os.path.abspath(source)
  abs_source_folder= '/'.join( abs_source.split('/')[:-1] )  # no trailing /
  if abs_source_folder.count('/'): abs_source_folder+='/'
  abs_dest=os.path.abspath(dest)
  abs_dest_folder=   '/'.join( abs_dest.split('/')[:-1]   )
  if abs_dest_folder.count('/'): abs_dest_folder+='/'

  chari=0  # to deal with limit case, no folder
  for chari, char in enumerate(abs_source_folder):
    if  chari+1>len(abs_dest_folder) or abs_dest_folder[chari]!=char: break
    chari+=1 # only to deal with case in which it exists without breaking
  #chari now marks the limit of first non-equal character
  common_path=abs_source_folder[:chari]
  rest_source=abs_source[chari:]
  rest_dest_folder=abs_dest_folder[chari:]
  n_back=rest_dest_folder.count('/')

  # print ( ('abs_source_folder', abs_source_folder) )
  # print ( ('abs_dest_folder', abs_dest_folder) )
  # print ( ('common', common_path) )
  # print ( ('rest_source', rest_source) )
  # print ( ('rest_dest_folder', rest_dest_folder) )

  dest_link_to='../'*n_back + rest_source  if common_path else  source

  # to deal with absolute inputs with nothing in common (algorithm would try to do relative paths until the very root; working but not pretty:
  if source in dest_link_to: dest_link_to=source  
  return (dest_link_to)


  

#######################################################################################################################################

def close_program():
  if 'temp_folder' in globals() and os.path.isdir(temp_folder):
    printerr(f'Program finished. Make sure you delete this: {temp_folder}')
    #shutil.rmtree(temp_folder)
    try:
      flush_service()
    except:
      pass


if __name__ == "__main__":
  try:
    main()
    close_program()  
  except Exception:
    close_program()
    raise 

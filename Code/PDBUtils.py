import os
import PyUtils
import subprocess
def DownloadPDBs(PDB_list_file):
    PDB_list = open(os.getcwd()+'/'+PDB_list_file,'r').readlines()
    for i in range(len(PDB_list)):
        PDBid = PDB_list[i].split()[0]
        PyUtils.create_folder(os.getcwd()+"/"+PDBid)
        os.chdir(PDBid)
        cmd = ["/work/londonlab/scripts/pdbUtil/getPdb.pl"+" -id "+PDBid]
        subprocess.call(cmd,shell=True)
        os.chdir("..")

def rec(PDB_list_file):
    PDB_list = open(os.getcwd()+'/'+PDB_list_file,'r').readlines()
    for i in range(len(PDB_list)):
        PDBid = PDB_list[i].split()[0]
        os.chdir(PDBid)
        subprocess.call(["/work/londonlab/scripts/pdbUtil/extract_chains_and_range.pl -p "+PDBid.lower()+".pdb -c "+PDB_list[i].split()[1]+" -o rec.pdb"],shell=True)
        os.chdir("..")

def lig(PDB_list_file):
    PDB_list = open(os.getcwd()+'/'+PDB_list_file,'r').readlines()
    for i in range(len(PDB_list)):
        sp_PDB = PDB_list[i].split()
        PDBid = sp_PDB[0]  
        os.chdir(PDBid)
        PDBf_name = PDBid.lower()+".pdb"
        PDBf = open(PDBf_name).readlines()
        lig_f = open(os.getcwd()+'/xtal-lig.pdb','w')
        for line in PDBf:
            if line.startswith('HETATM'):
                sp_line = line.split()
                if len(sp_line) == 12:
                    if sp_line[3] == sp_PDB[2] and sp_line[4] == sp_PDB[1] and sp_line[5] == sp_PDB[3]:
                        lig_f.write(line)
                if len(sp_line) == 11:
                    if sp_line[3] == sp_PDB[2] and sp_line[4][0:1] == sp_PDB[1] and sp_line[4][2:] == sp_PDB[3]:
                        lig_f.write(line)
        lig_f.flush()
        os.chdir("..")

def changeMolChain(pdb_file, new_chain):
    with open(pdb_file, 'r') as pfile:
        lines = pfile.readlines()
    with open(pdb_file, 'w') as pfile:
        for line in lines:
            if line[0] == 'H':
                pfile.write(line[:17] + new_chain + line[20:])

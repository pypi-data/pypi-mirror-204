#!/usr/bin/env python
#Korean description of PRato

def main():

    print(f"""
    
########################################################################################################

PRauto는 Bioinformatic & Chemoinformatics Automation tool로
1. Data retrieve
2. Data preprocessing
두가지 자동화 기능을 제공합니다.

prauto.retriever(Data retrieval)

$ python -m prauto.retriever

명령어를 커맨드라인 인터페이스에 입력함으로써 사용할 수 있습니다.

검색어를 통해 uniprot API에서 FASTA file을 retrieve하고
uniport accession을 통해 
1.PDB file과 
2.상호작용하는 ligand들의 sdf파일들도
각각 RCSB PDB API와 ChEMBL API에서 retrieve해줍니다.

결과물 : target 단백질 sequence들의 fasta파일, target 단백질 PDB파일들, target과 상호작용하는 리간드들의 sdf파일들


prauto.prepauto(Data preprocessing)

$ python -m prauto.prepauto

명령어를 커맨드라인 인터페이스에 입력함으로써 사용할 수 있습니다.

한 디렉토리에 담겨있는 PDB파일들을 
1. target에 해당되는 chain들만 분리해서 추출하고,기준이 되는 PDB에 맞춰 align해줍니다.
2. 주요 리간드와 결합에 관여하는 분자를 제외한 불필요한 분자들을 제거해줍니다.(세션 피일에서는 제거 대신 숨김)

결과물 : 전처리된 PDB파일들, PSE PyMOL 세션파일들
                                                  
#########################################################################################################
                                                                                            """)

if __name__ == "__main__":
    main()
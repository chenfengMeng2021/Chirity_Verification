# Amino acid Chirity problem
Is it possible that the left-handed amino acid and right-handed amino acid exist simultaneously?

This is a project to answer the question of why there is only left-handed protein exists in the world.

## Background: 
  when we are trying to synthesize some amino acid in the lab, the probability of appearing amino acid for left-
and right-handed is equal, and all of their physical and chemical properties are the same, thus we can't distinguish them from
each other. But in the real world, there is only left-handed amino acid, in the model, we want to verify the probability that
there is only one kind of amino acid can exist even if there are two chirality exist.

## method: 
  we make some simplifications for the simulation. we use computers to simulate two kinds of amino acids, and both of them form an organism, organism can only be left-handed amino acid and right-handed amino acid, and they are not compatible with each other. the
default limitation of the environment capacity is 10000(you can change it), and those two species will die when they reach their life expectancy. 
those species will replicate themselves and grows exponentially. if their total population passes the environmental capacity, the replication will stop.

## How to run it
```
git pull git@github.com:chenfengMeng2021/Chirity_Verification.git
conda create -n myenv python=3.9
conda activate myenv
pip install --upgrade pip
pip install -r requirements.txt
streamlit run main.py
```
  

## assumption: 
  left-handed amino acids and right-handed amino acids can't exist in the same animals.

## Result
  We demonstrate that two types of amino acid is not a stable system and there will only be one type of amino acid exist finally. 

  

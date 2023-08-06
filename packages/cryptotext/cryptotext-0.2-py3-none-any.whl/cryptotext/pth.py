import pandas as pd
from tabulate import tabulate

def generate_sequence(states,sequence_length):
    all_sequences = []
    nodes = []
    depth = sequence_length
    def gen_seq_recur(states,nodes,depth):
        if depth == 0:
            all_sequences.append(nodes)
        else:
            for state in states:
                temp_nodes = list(nodes)
                temp_nodes.append(state)
                gen_seq_recur(states,temp_nodes,depth-1)
    gen_seq_recur(states,[],depth)
    return all_sequences
def score_sequences(sequences,initial_probs,transition_probs,emission_probs,obs):
    best_score = -1
    best_sequence = None
    sequence_scores = []
    for seq in sequences:
        total_score = 1
        total_score_breakdown = []
        first = True
        for i in range(len(seq)):
            state_score = 1
            if first == True:
                state_score *= initial_probs[seq[i]]
                first = False
            else:
                state_score *= transition_probs[seq[i] + "|" + seq[i-1]]
                state_score *= emission_probs[obs[i] + "|" + seq[i]]
            total_score_breakdown.append(state_score)
            total_score *= state_score
        sequence_scores.append(total_score)
    return sequence_scores
def pretty_print_probs(distribs):
    rows = set()
    cols = set()
    for val in distribs.keys():
        temp = val.split("|")
        rows.add(temp[0])
        cols.add(temp[1])
    rows = list(rows)
    cols = list(cols)
    df = []
    for i in range(len(rows)):
        temp = []
        for j in range(len(cols)):
            temp.append(distribs[rows[i]+"|"+cols[j]])
        df.append(temp)
    I = pd.Index(rows, name="rows")
    C = pd.Index(cols, name="cols")
    df = pd.DataFrame(data=df,index=I, columns=C)
    print(tabulate(df, headers='keys', tablefmt='psql'))
def initializeSequences(_obs):
    seqLen = len(_obs)
    seqs = generate_sequence(states,seqLen)
    seq_scores = score_sequences(seqs,initial_probs,transition_probs,emission_probs,obs)
    return (seqLen,seqs,seq_scores)
states = ['Noun','Verb','Determiner']
initial_probs = {'Noun':0.9,'Verb':0.05,'Determiner':0.05}
transition_probs = {'Noun|Noun':0.1,'Noun|Verb':0.1,'Noun|Determiner':0.8,
                    'Verb|Noun':0.8,'Verb|Verb':0.1,'Verb|Determiner':0.1,
                    'Determiner|Noun':0.1,'Determiner|Verb':0.8,'Determiner|Determiner':0.1}
emission_probs = {'Bob|Noun':0.9,'ate|Noun':0.05,'the|Noun':0.05,'fruit|Noun':0.9,\
                  'Bob|Verb':0.05,'ate|Verb':0.9,'the|Verb':0.05,'fruit|Verb':0.05,\
                  'Bob|Determiner':0.05,'ate|Determiner':0.05,'the|Determiner':0.9,'fruit|Determiner':0.05}
print("Initial Distributions")
print(initial_probs)
print("\nTransition Probabilities")
pretty_print_probs(transition_probs)
print("\nEmission Probabilities")
pretty_print_probs(emission_probs)


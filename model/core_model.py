import numpy as np
from model.translation import translation_dynamics
from model.transcription import transcription_dynamics

# Converts a protein concentration to a regulatory signal
# Allows for a 'switch' effect
def activation(x, k=1.0, n=1):
    return x**n / (k**n + x**n + 1e-12)

def create_gene_model(genes, reg_map, promoter_history, delays, params):
    gene_index = {gene: i for i, gene in enumerate(genes)}

    # Defining the main part of the model
    # State function is built from initial conditions in simulation.py
    def model(state_function, t):
        n = len(genes)
        state = state_function(t)
        # Both mRNA and protein contained within the same state function - easier for coupled equations
        mRNA = state[:n]
        protein = state[n:]

        # Transcription delay → use past protein level for mRNA expression
        if t >= delays['transcription']:
            past_state = state_function(t - delays['transcription'])
            past_protein = past_state[n:]
        else:
            past_protein = np.zeros(n)

        # Translation delay → use past mRNA level for mRNA level for protein expression
        if t >= delays['translation']:
            mRNA_delayed = state_function(t - delays['translation'])[:n]
        else:
            mRNA_delayed = np.zeros(n)

        dstate_dt = np.zeros(2 * n)
        for gene in genes:
            i = gene_index[gene]
            reg_input = sum(w * activation(past_protein[gene_index[src]]) for src, w in reg_map.get(gene, []))
            promoter_state = promoter_history[gene](t)
            dstate_dt[i] = transcription_dynamics(promoter_state, reg_input, mRNA[i], params['transcription'])
            dstate_dt[i + n] = translation_dynamics(mRNA_delayed[i], protein[i], params['translation'])
        return dstate_dt

    return model

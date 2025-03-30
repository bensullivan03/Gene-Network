import numpy as np
from ddeint import ddeint
from parameters import genes, delays, dt, T, params
from model.core_model import create_gene_model
from visualisation import plot_results
import random

# Filled from GUI sliders
interaction_weights = {}
promoter_transition = {}

# How genes interact with each other
def build_regulatory_map():
    reg_map = {gene: [] for gene in genes}
    for (src, tgt), var in interaction_weights.items():
        w = var.get()
        # Don't include very small effects in the network
        if abs(w) > 1e-6:
            reg_map[tgt].append((src, w))
    return reg_map

# 2 step Markov function for changing promoter state
def generate_promoter_history(genes, promoter_probs, t_vals):
    step = dt
    # Initated state
    states = ['ON', 'OFF', 'INITIATED']
    current = {g: random.choice(states) for g in genes}
    histories = {g: [] for g in genes}
    for t in t_vals:
        for g in genes:
            # Transition from 'off' state
            if current[g] == 'OFF':
                if np.random.rand() < promoter_probs[g]['off_to_initiated'] * step:
                    current[g] = 'initiated'

            # Transitions from 'initiated' state
            elif current[g] == 'INITIATED':
                if np.random.rand() < promoter_probs[g]['initiated_to_off'] * step:
                    current[g] = 'off'
                elif np.random.rand() > (promoter_probs[g]['initiated_to_on']) * step:
                    current[g] = 'on'
                else:
                    current[g] = 'initiated'

            # Transition from 'on' state
            elif current[g] == 'ON':
                if np.random.rand() < promoter_probs[g]['on_to_off'] * step:
                    current[g] = 'OFF'
        
            histories[g].append(current[g])
    return {g: lambda t, hist=np.array(states): hist[min(int(t/step), len(hist)-1)]
            for g, states in histories.items()}

# Building the main simulation
def simulation():
    reg_map = build_regulatory_map()
    promoter_probs = {g: {'on': promoter_transition[g]['on'].get(),
                          'off': promoter_transition[g]['off'].get(),
                          'initiated': promoter_transition[g]['initiated'].get(),
                          }
                      for g in genes}

    steps = int(T / dt) + 1
    t_vals = np.linspace(0, T, steps)
    promoter_history = generate_promoter_history(genes, promoter_probs, t_vals)

    def history_func(t):
        return np.zeros(2 * len(genes))

    model = create_gene_model(genes, reg_map, promoter_history, delays, params)
    sol = ddeint(model, history_func, t_vals)
    mRNA_vals = sol[:, :len(genes)]
    protein_vals = sol[:, len(genes):]
    plot_results(t_vals, mRNA_vals, protein_vals, promoter_history, genes)

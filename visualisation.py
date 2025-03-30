import matplotlib.pyplot as plt
import numpy as np

# Generating the 3 plots
def plot_results(t_vals, mRNA_vals, protein_vals, promoter_history, genes):
    fig, axs = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

    # Plot promoter state over time
    
    for k, gene in enumerate(genes): 
        state_value = []
        for t in t_vals:
            current_state = promoter_history[gene](t)
            if current_state == 'ON':
                value = 1
            elif current_state == 'INITIATED':
                value = 0.2
            else:
                value = 0
            state_value.append(value)

        offset = k * 1.2
        axs[0].step(t_vals, np.array(state_value) + offset, where='post', label=gene)

    axs[0].set_yticks([i * 1.2 for i in range(len(genes))])
    axs[0].set_yticklabels(genes)
    axs[0].set_ylabel("Promoter State")
    axs[0].set_xlabel("Time")
    axs[0].grid(True)
    axs[0].legend(loc = 'upper left')
    
    # Levels of mRNA over time
    for idx, gene in enumerate(genes):
        axs[1].plot(t_vals, mRNA_vals[:, idx], label=gene)

    axs[1].set_ylabel("mRNA Levels")
    axs[1].grid(True)
    axs[1].legend(loc = 'upper left')

    # Levels of protein over time
    for j, gene in enumerate(genes):
        axs[2].plot(t_vals, protein_vals[:, j], label=gene)

    axs[2].set_ylabel("Protein Levels")
    axs[2].legend(loc = 'upper left')
    axs[2].grid(True)

    plt.tight_layout()
    plt.suptitle("Gene Expression Dynamics", y=1.1)
    plt.show()

# How protein levels change

def translation_dynamics(mRNA_delayed, protein, params):
    # Protein production is proportional to mRNA level at previous point in time
    production = params['translation_rate'] * mRNA_delayed

    # Degradation is proportional to protein concentration
    degradation = params['degradation_rate'] * protein
    return production - degradation

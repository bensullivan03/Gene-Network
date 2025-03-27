# How mRNA levels change

def transcription_dynamics(promoter_state, regulation_input, mRNA, params):
    # 'ON' production is sum of base rate and additional effect from the protein level
    if promoter_state == 'ON':
        production = params['basal_rate'] + params['regulation_scale'] * regulation_input
    else:
        production = 0.0

    # Degradation is always occuring - proportional to mRNA level
    degradation = params['degradation_rate'] * mRNA
    return production - degradation
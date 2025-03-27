# Gene and gene interaction setup
genes = ['GeneA', 'GeneB', 'GeneC']
interactions = [(g1, g2) for g1 in genes for g2 in genes if g1 != g2]

# Time settings
dt = 0.1
T = 50

# Time delay effects
delays = {
    'transcription': 2.0,
    'translation': 2.0
}

# Model parameters
params = {
    'transcription': {
        'basal_rate': 0.2,
        'regulation_scale': 0.2,
        'degradation_rate': 0.5
    },
    'translation': {
        'translation_rate': 2.0,
        'degradation_rate': 0.5
    }
}

# Default promoter transition rates
promoter_rates = {
    gene: {'on': 0.9, 'off': 0.1} for gene in genes
}

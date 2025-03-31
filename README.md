## Gene Expression Simulation

This project simulates a gene regulatory network. 

The state of the promoter region is determined by a Markov chain. 
When the promoter region is 'ON' - the mRNA production rate includes an upregulation term, as well as a 'basal' term.
When the promoter region is 'OFF' - only a degradation term is present.
The rate of mRNA upregulation is related to the past levels of protein concentration (weighted by an activation function and the interaction strength). 
The degradation term is related to the current concentration of mRNA.
The level of protein is governed by the past levels of mRNA. 

Due to the delay term involved in each, a Delayed Differential Equation (DDE) is used to calculate the current levels of protein and mRNA expression.

The gene promoter state, mRNA and protein levels are then plotted over time.

Run
```bash
python main.py
```
to begin the simulation.

In the gui that appears you will be able to adjust promotion/ inhibition effect between genes as well as the probability of the promoter region randomly switching state at a point in time.

Requirements:
* Python 3.8+
* tkinter
* numpy
* matplotlib
* scipy
* ddeint

If you wish to add more genes, then you can do so by adding them to the genes list in parameters.py.

TO DO:

* There are probably bugs I haven't found...
* Delay between promoter region turning on and mRNA levels rising - transcription and leaving nuclei also takes time
* Update Markov model to use 3 states - ON, OFF and INITIATION - more realistic 
    - Need to ensure that probabilities do not sum to greater than 1 for promoter region
        - Have 2 sliders in gui
    - Model transcription factors?
* More realistic protein and mRNA degradation
* Proteins should influence promoter region switch probability - i.e. 'on' and 'off' and 'initiation' probabilities - not just promotion/ inhibition of transcription
    - Including self regulation - i.e positive/negative feedback loops
    - More realistic switching on and off of promoter region - entirely random is not realistic
* Make the activation function (protein concentration -> mRNA upregulation) more realistic
    - e.g. sharper threshold
    - sigmoidal
    - Hill functions?
* Variable starting levels of mRNA/ protein + starting state of promoter
* Increase stochastic nature / noise in the system
* Implement splicing so that multiple proteins can be expressed by a single gene
* Relation to a real world system
    - This will probably mean implementing some real units
* Simluating external stimuli that may affect  transcription and/ or translation e.g. drugs
* Make gui nicer - both visually and interactively
    - Develop a better way setting which genes will interact with other parts of the system
* Visualise a graph of the interactions
* Ability to save/ load parameters between different simulations


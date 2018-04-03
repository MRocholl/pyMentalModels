=================
General Structure
=================

.
├── counterexamples.py
├── mental_model_classes.py
├── parser.py
├── Quantified
├── README.rst
├── regex_parser.py
├── Sentential
└── Temporal


TODO:
-----
Aks Johnsson-Laird what the individuals, footnotes and other attributes of the intesions and models are. Will enable me to get a better understanding of how the lisp code works.

Also finish the python skeleton for the Models. Will keep general structure of the lisp code, but with different classes for T, S and Q with different behavior, inheriting from an absract baseclass that defines the commom methods they all share.


* Difference between intention and models
  Models are made up of individual intensions of type, S, T or Q.
  Models are collected into ModelSets.
    
    API.lisp provides most model manipulation functions 
    These functions will be either included in the model class,
    probably in its abstract one.

        * find-referent-in-model-set
                args: referent
                      models
            find-referent-in-model
                args: referent
                      t-model or q-model

            find-referent-in-individual
                args: referent
                      individual

            remove-models
                args: models_to_be_removed
                      model-set


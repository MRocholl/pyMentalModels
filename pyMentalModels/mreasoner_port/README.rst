=================
General Structure
=================

.. code-block:: text

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

Question:
    What is footnote?
    What is test-modelset?
    What is individual in model?
    Indivudials seem to be of the form ((A)(B)), referent either A or B in individual.
    And models seem to be a combination of several individuals.

Maybe ask JL if he can provide me with an example for every 


Also finish the python skeleton for the Models. Will keep general structure of the lisp code, but with different classes for T, S and Q with different behavior, inheriting from an absract baseclass that defines the commom methods they all share.



  * Difference between intention and models
    Models are made up of individual intensions of type, S, T or Q.
    Models are collected into ModelSets.
    
    API.lisp provides most model manipulation functions 
    These functions will be either included in the model class,
    probably in its abstract one.

  * General methods for models
        find-referent-in-model-set
            :args: referent, models
            :Doc: Tries to find referent in set of models. It returns list of all models in which it finds referent
      
        find-referent-in-model
            :args: referent, t-model or q-model

        find-referent-in-individual
            :args: referent, individual
            :Doc: Tries to find a referent in an individual, e.g., (find-referent-in-individual '(A) '((A) (B))) => (A)

        remove-models
            :args: models_to_be_removed, model-set
            :Doc: eliminates one model from modelset (remove-mod '(((A)(B))((A)(B))) test-modelset) => ((((A) (C)) ((A) (C))) (((D) (A)) ((D) (A))) (((D) (B)) ((D) (B)))) 
            :TODO: This should be a method every model has and will hence be implemented in the BaseClass

  *  Q-model-Specific methods
        find-referent-individuals-in-model
            :args: referent, q-model 
            :Doc: Finds and returns all referent individuals in a model.
              (find-referent-individuals-in-model '(A) '(((- A) (B)) ((A) (B)) ((A) (B)) (T20))) => (((A) (B)) ((A) (B)))
              returns the 

        find-subj&obj-in-model
            :args: subj, obj, q-model
            :doc: Finds and returns all referent individuals in a model.  (find-subj&obj-in-model '(A) '(B) '(((- A) (B)) ((A) (- B))  ((A) (B)) ((A) (B)) (T20))) => (((A) (B)) ((A) (B)))
        
        get-referent-cardinality
            :args: referent, q-model
            :docs: Calculates cardinality of model with respect to a given referent, e.g., (get-referent-cardinality '(A) '(((- A) (B)) ((A) (B)) ((A) (B)) (T20))) => 2



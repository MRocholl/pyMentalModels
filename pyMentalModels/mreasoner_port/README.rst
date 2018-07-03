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

MY UNDERSTANDING OF THINGS:
---------------------------
Cardinality etc is defined in classes.lisp the api file provides functions that evalute cardinality-conditions and the builder file verifies if a model satisfies these conditions for the given intension




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

        find-subj&obj-in-model
            :args: subj, obj, q-model
            :doc: Finds and returns all referent individuals in a model.  (find-subj&obj-in-model '(A) '(B) '(((- A) (B)) ((A) (- B))  ((A) (B)) ((A) (B)) (T20))) => (((A) (B)) ((A) (B)))
        
        get-referent-cardinality
            :args: referent, q-model
            :docs: Calculates cardinality of model with respect to a given referent, e.g., (get-referent-cardinality '(A) '(((- A) (B)) ((A) (B)) ((A) (B)) (T20))) => 2

        get-subj&obj-cardinality 
            :args: subj, obj, q_model
            :doc: Calculates cardinality of model subset that includes individuals that are both subj & obj, e.g., (get-subj&obj-cardinality '(A) '(B) '(((A) (C)) ((A) (B)) ((A) (B)) (T20))) => 2

        get-subj-wo-obj-cardinality 
            :args: subj, obj, q_model 
            :doc: Calculates cardinality of model subset that includes individuals that are subjs but NOT objs, e.g., (get-subj-wo-obj-cardinality '(A) '(B) '(((A) (C)) ((A) (B)) ((A) (B)) (T20))) => 1
  

        find-first-referent-individuals-in-model
            :args: referent, q_model
            :doc: This function is very similar find-referent-individuals-in-model Except, instead of returning a set of individuals that have a certain referent, This function returns the INDEX in the model of the first matching individual It does so by iterating through the model and calling MEMBER on each individual If a match is found, exit the loop and return the index number.  (find-referent-individuals-in-model '(A) '(((- A) (B)) ((A) (B)) ((A) (B)) (T20))) => 1

        find-first-subj&obj-in-model
            :args: subj, obj, q_model
            :doc: This function is very similar to find-subj&obj-in-model Except, instead of returning a set of individuals that have a certain sujb & obj, This function returns the INDEX in the model of the first matching individual It does so by iterating through the model and calling MEMBER on each individual If a match is found, exit the loop and return the index number.  Finds and returns the index number of the first matching individual in a model.  (find-subj&obj-in-model '(A) '(B) '(((- A) (B)) ((A) (- B))  ((A) (B)) ((A) (B)) (T20))) => 2
          

        equals
            :args:  a:symbol, b:symbol

        equals
            :args a:list, b:list

        equals
            :args: entity-1:q-model, entity-2:q-model
            :doc: This function returns true or false depending on whether the two input models are equivalent. Equivalent in this case means that for all the individuals in mod1 there is an equivalent individual in mod2. . This ensures that the search is exhaustive.  (is-equivalent-model '(((A))((B))) '(((A))((B)))) => T (is-equivalent-model '(((A))((B))) '(((A)))) => NIL

        equals
            :args: entity-1:intension, entity-2:intension
                   
        create-indiv-according-to-footnotes
            :args: list-of-intensions, indiv
            :doc: Uses mentioned-in-footnotes to modify a potential indiv to be added to a model by consulting footnotes. If a footnote mentions the property to add in the subject position, then add the property to the individual. If no relevant footnotes are found, simply return the property as an individual.
           (add-indiv-according-to-footnotes '((include (A) (B)) (include (B) (C))) '(C)) => ((C))
           (add-indiv-according-to-footnotes '((include (A) (B)) (include (B) (C))) '(A)) => ((A) (B))
           (add-indiv-according-to-footnotes '((include (A) (B)) (include (A) (C))) '(A)) => ((A) (B) (C))
          
        has-negative-properties
            :args: individual
            :doc: Returns True if a list within individual contains '-

        has-negative-entities
            :args: q-model

        combine-fns
            :args: fn1, fn2
            :doc: *ml I know that we have a combine-footnotes -- this is a bit different*
                Combines two footnotes, making sure that neither of them are nill
            :example: (combine-fns nil '(include (A) (B))) =>((INCLUDE (A) (B)))

        remove-nth-from-list
            :args: index, model
            :doc: Given a list of the form '(((A)(C)) ((A)(D)) ((A)(E)) ((A)(F))) and a number, remove the nth individual (counting from 0) and return the resulting model
            :example: (remove-nth-from-list 1 '(((A)(C)) ((A)(D)) ((A)(E)) ((A)(F)))) =>(((A)(C)) ((A)(E)) ((A)(F))))

        remove-nth-entity 
            :args: q_model, entity-num
            :doc: *Note not destructive -- creates NEW model* Creates new instance with entity/individual missing

        replace-nth-from-list
            :args: list, n, elem
            :doc: Given a list, replaces the nth element and returns the list. 
            :example: (replace-nth-from-list (list 1 2 3) 1 4) =>(1 4 3)

        replace-nth-entity
            :args: q-model, n, entity
            :doc: *ml likewise, this should be renamed to replace-nth-indiv* Given a list, replaces the nth element and returns the list.  
            :example: (replace-nth-from-list (list 1 2 3) 1 4)=>(1 4 3)

        make-individuals
            :args: number, arg
            :doc: Given a cardinal number and a property rtns model of that number of individuals
            :example: (make-individuals 3 '(A)) => (((A)) ((A)) ((A)))

        make-complex-individuals 
            :args: number, indiv
            :doc: Given a cardinal number and indiv such as '((c)(-b)) makes that number of them
            :example: (make-complex-individuals 3 '((a)(- b))) => (((A) (- B)) ((A) (- B)) ((A) (- B)))"

        negate-property
            :args: property 
            :doc: Negates a property to be include in individual
            :example: (negate-property '(A)) => (- A)"

        entity-difference
            :args: indivs1, indivs2
            :doc: Returns the # of differences between two individuals.  First, this algorithm iterates through one of the individuals' properties (ind1) and removes all co-occurrences.  Second, it iterates through the remaining properties of ind1 and tests to see if there are any pairs that are identical except for a negation, e.g., (B) and (- B). If there are, increment diff for each one and remove both.  Finally, return diff + length remaining properties in ind1 and ind2.

 * Section 1.2: Intension manipulation functions

        abbreviate:
            :args: model

        abbreviate
            :args: null-intension

        abbreviate
            :args: q-intension
            :doc: Makes an abbreviation of a premise
            :example: (abbreviate (parse '(some a are not b))) => 'Oab'

        abbreviate
            :args: s-intension

        abbreviate
            :args: t-intension
         
        get-syllogistic-figure
            :args: premise-1:q-intension, premise-2:q-intension
            :doc: Determines figure of the two premises by establishing the respective grammatical roles of the two end terms
            :example: (get-syllogistic-figure (parse '(all b are a)) (parse '(all b are c))) => 4
           
        negative-relation
            :args: relation

        convert-intens
            :args: q-intension
            :doc: *ML since subject is q-intension specific, I don't know how to generalize this.* forms converse of intension, by swapping subject and object 
            :example: (convert-intens '((((? 3) (> 2)) (? 3) ((= CARDINALITY)) NIL T) (C) (NEGATE (INCLUDE (C) (A))))) => ((((? 3) (> 2)) (? 3) ((= CARDINALITY)) NIL T) (A) (NEGATE (INCLUDE (A) (C))))"
          (make-instance 'q-intension
                         :card (cardinality intension)
                         :np (numprop intension)
                         :bnd (boundary intension)
                         :pol (polarity intension)
                         :fn (footnotes intension)
                         :subj (object intension)
                         :obj (subject intension)
                         :rel (relation intension)))

        find-cardinality-assumption ((intension q-intension)) ; ssk
          "Given an intension, returns the boundary conditions of the intension, e.g.,
           (find-cardinality-assumption '((((? 4) (> 4)) (? 3) ((<= CARDINALITY) (>= 3)) T NIL) (A) (INCLUDE (A) (B))))
           => ((? 4))"
          (let ((card (cardinality intension))
                (condition nil))
            (dolist (ccond card)
              (when (equal '? (first ccond))
                (push ccond condition)))
            condition))

        find-cardinality-condition ((intension q-intension)) ; ssk
          "Given an intension, returns the cardinality condition of the intension, e.g.,
           (find-cardinality-condition '((((? 4) (> 4)) (? 3) ((<= CARDINALITY) (>= 3)) T NIL) (A) (INCLUDE (A) (B))))
           => ((> 4))"
          (let ((card (cardinality intension))
                (condition nil))
            (dolist (ccond card)
              (when (not (equal '? (first ccond)))
                (push ccond condition)))
            condition))

        find-numprop-condition ((intension q-intension)) ; ssk
          "Given an intension, returns the cardinality condition of the intension, e.g.,
           (find-cardinality-condition '((((? 4) (> 4)) (? 3) ((<= CARDINALITY) (>= 3)) T NIL) (A) (INCLUDE (A) (B))))
           => ((> 4))"
          (when (not (equal '? (first (numprop intension))))
            (numprop-value intension)))

        evaluate-cardinality-conditions (value conditions) ; ssk
          "Given a value and a set of partial cardinality conditions, returns t or nil
           depending on whether all conditions have been met. E.g.,
           (evaluate-cardinality-conditions 5 '((> 3) (> 4) (> 1))) => T
           (evaluate-cardinality-conditions 5 '((> 3) (> 4) (> 100))) => nil"
          (let ((evaluated nil))
            (dolist (condn conditions)
              (push (eval (list (first condn) value (second condn))) evaluated))
            (not (member nil evaluated))))

        evaluate-boundary-conditions (value cardinality condns) ; ssk
          "Given a value and a set of boundary conditions, returns t or nil
           depending on whether all conditions have been met. E.g.,
           (evaluate-boundary-conditions 3 5 '((<= CARDINALITY) (>= 3))) => T
           (evaluate-boundary-conditions 2 5 '((<= CARDINALITY) (>= 3))) => NIL"
          (let ((evaluated nil)
                (eval-list nil)
                (conditions (replace-card-in-condns cardinality condns)))
            (dolist (condn conditions)
              (push (list (first condn) value (second condn)) eval-list)
              (push (eval (list (first condn) value (second condn))) evaluated))
        ;    (print conditions)
        ;    (print eval-list) ; printing for debugging purposes only
        ;    (print evaluated)
            (not (member nil evaluated))))

        replace-card-in-condns (cardinality conditions) ; ssk
          "Given a value for cardinality, this fn replaces all instances of
           the abstract symbol 'cardinality with its actual value, e.g.,
           (replace-card-in-condns 5 '((<= CARDINALITY) (>= 3)))                => ((<= 5) (>= 3))
           (replace-card-in-condns 10 '((< cardinality)(> (* .5 cardinality)))) => ((< 10) (> (* 0.5 10)))
           (replace-card-in-condns 5 '((<= NOT-CARDINALITY) (>= 3)))            => ((<= NOT-CARDINALITY) (>= 3))"
          (subst cardinality 'cardinality conditions))

        negative-intension ((intension q-intension))
          "Checks whether intension is negative by checking that either
           predicate is negative, quantifier is negative, but not both, e.g.,
           (negative-intension '((((? 3) (> 2)) (? 3) ((= CARDINALITY)) NIL T) (A) (INCLUDE (A) (B))))                  => T
           (negative-intension '((((? 3) (> 2)) (? 2) ((< CARDINALITY) (> 0)) T NIL) (A) (NEGATE (INCLUDE (A) (B)))))   => T
           (negative-intension '((((? 3) (> 2)) (? 2) ((< CARDINALITY) (> 0)) NIL NIL) (A) (NEGATE (INCLUDE (A) (B))))) => NIL"
          (let ((neg-quant (not (polarity intension)))
                (neg-rel (negative-relation (relation intension)))) 
            (and (or neg-quant neg-rel)
                 (not (and neg-quant neg-rel)))))
          
        affirmative-intension ((intension intension))
          (not (negative-intension intension)))

        ; ---------------------------------------------------------------------------------
        ; Section 1.3: Helper fns for high level fns
        ; ---------------------------------------------------------------------------------

        terms ((intension q-intension))
          (list (subject intension) (object intension)))

        get-syll-end-terms ((premise1 q-intension) (premise2 intension))
          "Interface for syllogistic premises to get-end-terms"
          (first (get-end-terms (list premise1 premise2))))

        get-end-terms (intensions)
          "Given a set of intensions corresponding to a hypothetical set of premises,
           returns a list contain possible pairs of end terms. The end-terms are derived by
           treating all premises of the word Quant Subj-property Obj-property as a direct link
           from one node, one called subj-property, to another node, called obj-property. This
           information is stored in a matrix called connectivity-matrix. Then, this graph is
           traversed, iterating through all possible starting points, to find a complete list of
           possible paths. This list is then sorted using a custom insertion sort. Currently, there
           are two options for possible sort strategies, though ultimately, this is a theoretical
           question that needs answering. In addition to length, one can also sort by length and then
           use end-term-frequency-p to consider ties (assuming that only one set of end terms is desired).
           Finally, pick end terms is called on the sorted list and chooses the top n paths, where each
           path is tied for the longest length, and reports the end term properties of the start and
           end of the path.

           Function Calls:
           - build-properties-and-frequency-list returns a list, the car of which is the frequency of
             every property in the intensions
           - build-connectivity-matrix uses information to construct a matrix
           - find-all-paths-through matrix uses depth first search to traverse graph created and returns
             a list of paths given a starting node
           - pick-end-terms takes a list of paths that has been sorted and returns the end terms and the
             head and tail of the top n paths where n is the set with the longest length

           Usage: (get-end-terms '( ((((? 3)(> 2)) (? 3) ((= cardinality))       t   t) (A) (include (A) (B)))  
                                    ((((? 3)(> 2)) (? 3) ((= cardinality))       t   t) (B) (include (B) (C))) 
                                    ((((? 3)(> 2)) (? 2) ((< cardinality)(> 0))  t nil) (A) (include (A) (C))) 
                                    ((((? 3)(> 2)) (? 3) ((= cardinality))       t   t) (C) (include (C) (D)))))
                   =>(((A) (D)))"
          (let* ((frequency-count (build-frequency-list intensions))
                 (properties-list (mapcar #'(lambda(x) (car x)) frequency-count))
                 (connectivity-matrix (build-connectivity-matrix intensions properties-list)))    
            ;(princ "Frequency-Count: ")(princ frequency-count)(terpri)
            (let ((all-paths nil))
              (do ((i 0 (+ i 1)))
                  ((= i (length properties-list)))
                (setf all-paths (append (second (find-all-paths-through-matrix connectivity-matrix i (list (list i) (list)))) all-paths)))
              (setf all-paths (path-sort all-paths))
            ;(princ all-paths)(terpri)
            (pick-end-terms all-paths properties-list))))

        build-frequency-list (intensions)
          "Iterates through the list of intensions and builds frequency-count.
           Frequency-Count is a list of the form ((property frequency)(property frequency)...)
           where property is a property ((A) or (- A) for example) and frequency is an integer
           counting how many times it has occurred in both subj and obj positions. Hypothetically,
           if this function were modified, it could construct independent frequency-count lists for
           both subj and obj positions, if this were theoretically motivated.

           It works by checking to see if the property is already in the list. If it is, then it adds
           one to the frequency for that property. If not, then it creates a new entry and appends it to
           the list with frequency 1.

           Usage:
           (build-frequency-list '( ((((? 3)(> 2)) (? 3) ((= cardinality))       t   t) (A) (include (A) (B)))  
                                    ((((? 3)(> 2)) (? 3) ((= cardinality))       t   t) (B) (include (B) (C))) 
                                    ((((? 3)(> 2)) (? 2) ((< cardinality)(> 0))  t nil) (A) (include (A) (C))) 
                                    ((((? 3)(> 2)) (? 3) ((= cardinality))       t   t) (C) (include (C) (D)))))
           =>(((A) 2) ((B) 2) ((C) 3) ((D) 1))"
          (let ((frequency-count (list)))
            (dolist (intension intensions frequency-count)
              (let ((subj (subject intension))
                    (obj  (object intension)))
                (if (not (member subj frequency-count :key #'car :test #'equal))
                    (setf frequency-count (append frequency-count (list (list subj 1))))
                  (let ((subj-freq (cadr (find subj frequency-count :key #'car :test #'equal))))
                    (setf frequency-count (substitute-if (list subj (+ subj-freq 1)) #'(lambda(x) (equal (car x) subj)) frequency-count))))          
                (if (not (member obj frequency-count :key #'car :test #'equal))
                    (setf frequency-count (append frequency-count (list (list obj 1))))
                  (let ((obj-freq (cadr (find obj frequency-count :key #'car :test #'equal))))
                    (setf frequency-count (substitute-if (list obj (+ obj-freq 1)) #'(lambda(x) (equal (car x) obj)) frequency-count))))))))

        pick-end-terms (path properties-list)
          "This function accepts a list of paths and a list of all possible properties.
           It determines the property name of the head and tail of the first path in the list.
           If the next path in the list is of equal length, it recursively calls itself with the
           rest of the paths.

           Usage: (pick-end-terms '((0 1 2 3) (0 2 3) (1 2 3) (2 3) (3)) '((A) (B) (C) (D))) => (((A) (D)))" 
          (let* ((subj-term (elt properties-list (car (first path))))
                 (obj-term (elt properties-list (car (last (first path)))))
                 (end-terms-list (list (list subj-term obj-term))))
        ;    (if (and (> (length path) 1) (equal (length (first path)) (length (second path))))
        ;      (if (not (null freq-count))
        ;          (setf end-terms-list (append end-terms-list (pick-end-terms (rest path) properties-list freq-count)))
        ;        (setf end-terms-list (append end-terms-list (pick-end-terms (rest path) properties-list))))
        ;      end-terms-list)))
            end-terms-list))

        path-sort (paths)
         "Sorts using length and then term order assumes that no path will be repeated (ie have equal
          length and elements)"
          (sort paths  #'(lambda (x y) (if (equal (length x) (length y))
                                           (let ((is-less nil))
                                             (do ((i 0 (+ i 1)))
                                                 ((or (= i (length x)) is-less) is-less)
                                               (if (< (nth i x) (nth i y))
                                                   (setf is-less T))))
                                         (> (length x) (length y))))))                          

        end-terms-more-frequent-p (path1 path2 freq-count)
          "Predicate function which compares the frequency of the sum of the head and tail terms for
           two different paths. The numbers in the path refer to the order index in the frequency list.
           Usage: (end-terms-more-frequent-p '(1 2 3) '(2 3) '(((A) 2) ((B) 2) ((C) 3) ((D) 1))) => NIL
                  (end-terms-more-frequent-p '(2 3) '(1 2 3) '(((A) 2) ((B) 2) ((C) 3) ((D) 1))) => T"
          (let* ((properties-list (mapcar #'(lambda(x) (car x)) freq-count))
                 (path1-head-freq (cadr (elt freq-count (position-if #'(lambda(x) (equal (car x) (elt properties-list (first path1)))) freq-count))))
                 (path2-head-freq (cadr (elt freq-count (position-if #'(lambda(x) (equal (car x) (elt properties-list (first path2)))) freq-count))))
                 (path1-tail-freq (cadr (elt freq-count (position-if #'(lambda(x) (equal (car x) (elt properties-list (car (last path1))))) freq-count))))
                 (path2-tail-freq (cadr (elt freq-count (position-if #'(lambda(x) (equal (car x) (elt properties-list (car (last path2))))) freq-count)))))
            (> (+ path1-head-freq path1-tail-freq) (+ path2-head-freq path2-tail-freq))))


        build-connectivity-matrix (intensions properties-list)
          "Given a set of intensions, constructs a matrix that represents a directed graph. The matrix
           will be n x n, where n = length of properties-list. For every intension of the form Quant
           Subj-Prop Obj-Prop, it searches properties-list to and finds the index of that property and
           then puts a one in row subj-index-number in column obj-number. Note that these 1s are not
           considered symmetrical so there is no entry in the inverse.

           Usage:
           (build-connectivity-matrix '( ((((? 3)(> 2)) (? 3) ((= cardinality))      t   t) (A) (include (A) (B)))  
                                         ((((? 3)(> 2)) (? 3) ((= cardinality))      t   t) (B) (include (B) (C))) 
                                         ((((? 3)(> 2)) (? 2) ((< cardinality)(> 0)) t nil) (A) (include (A) (C))) 
                                         ((((? 3)(> 2)) (? 3) ((= cardinality))      t   t) (C) (include (C) (D))))
                                                '((A)(B)(C)(D)))
            =>#2A((X 1 1 X) (X X 1 X) (X X X 1) (X X X X))"
          (let ((connectivity-matrix (make-array (list (length properties-list) (length properties-list)) :initial-element 'x)))
            (dolist (intension intensions connectivity-matrix)
              (let* ((subj (subject intension))
                     (obj  (object intension))
                     (subj-number (position subj properties-list :test #'equal))
                     (obj-number (position obj properties-list :test #'equal)))
                (setf (aref connectivity-matrix subj-number obj-number) 1)
                (setf (aref connectivity-matrix obj-number subj-number) 1)))))
          
        find-all-paths-through-matrix (matrix row-number paths)
          "Given a matrix representing a directed graph, returns a list of all paths that originate at the
           node specified by row-number by recursively exploring unseen nodes (nodes not in visited-list.
           The function works by checking each value in the current row. If its a 1, that means there is a
           connection and it recursively calls itself starting at the connected node (which can't be itself
           or an already visited node) with an updated visited list. When it reaches a node that has no viable
           connections, it returns. 
           Usage:
           (find-all-paths-through-matrix #2A((X 1 1 X) (X X 1 X) (X X X 1) (X X X X)) 0 (list (list 0) (list)))
           => ((0) ((0 2 3) (0 1 2 3)))"
          (let ((cur-row-contents (extract-matrix-row matrix row-number))
                (visited-list (car paths)))
            (if (terminal-node-p cur-row-contents)
                (list visited-list (list visited-list))
              (setf visited-list (find-all-sub-paths matrix row-number paths cur-row-contents)))))

        extract-matrix-row (matrix row)
          (let ((row-contents (list)))
            (dotimes (cur-col-num (array-dimension matrix 0) row-contents)
              (setf row-contents (append row-contents (list (aref matrix row cur-col-num)))))))

        terminal-node-p (row)
          (not (member 1 row :test #'equal)))

        find-all-sub-paths (matrix row-number paths cur-row-contents )
          (let ((sub-paths (list))
                (found-unvisited-node nil)
                (visited-list (car paths)))
            (do ((cur-col-num 0 (+ cur-col-num 1)))
                ((equal cur-col-num (length cur-row-contents)))
              (if (and 
                   (equal (nth cur-col-num cur-row-contents) 1) 
                   (not (equal cur-col-num row-number)) ;reflexive, should be impossible
                   (not (member cur-col-num visited-list)))
                  (let* ((new-stuff (find-all-paths-through-matrix matrix cur-col-num (list (append visited-list (list cur-col-num)) (list))))
                         (new-list-of-paths (cadr new-stuff)))
                    (setf sub-paths (append new-list-of-paths sub-paths))
                    (setf found-unvisited-node t))))              
            (if (not found-unvisited-node)
                (setf sub-paths (list visited-list)))
            (list visited-list sub-paths)))

        ; ---------------------------------------------------------------------------------
        ; Section 1.4: Low level model functions
        ; ---------------------------------------------------------------------------------

        negate ((models list))
          "Negates models
           if models is t, nil, of single item, '(a), calls neg to 
           negate else makes list of all atoms in model and generates 
           complement of models"
          (cond((or (atom models)(atom (first models)))(neg models))
               (t (comp models (allpos (first models))))))

        allpos(model)
          "OK generates all possible models from one model
           null.cdr.model sets up two seed models in a list, e.g. (((d))((- d)))
           stick on car.model to each model in recursive call, and negate.car.model 
           appending the two lists
           (allpos '((a)(b)(c)(d)))(allpos nil)(allpos '((a)))(allpos '((a)(- b)))"
        (cond((null (rest model))(list (list (first model))(list (neg (first model)))))
             (t (append (mapcar #'(lambda(mod)(cons (first model) mod))(allpos (rest model)))
                          (mapcar #'(lambda(mod)(cons (neg(first model)) mod))(allpos (rest model)))))))

        neg(property)
          "(neg '(a)) => (- a)
           possibly add line to negate an already neg property"
          (cons '- property))

        comp (models allposmodels)
          "rtns the complement to a set of models from allposmodels"
        (cond((null models) allposmodels)
             (t (comp (rest models)(remove-itm (first models) allposmodels)))))

        mapjoin(mod models)
          "Adds model, perhaps of only one item, to each member of models
           AND with list drops nil combinations from result"
          (mapcan #'(lambda(m)(and (join m mod)(list(join m mod)))) models))

        contra (item mod)
          "If item is a contradiction of member of mod rtns t
           if item neg tries to match unnegated item;  if item is 
           affirmative, tries to match negated item  --  either 
           case signifies contradiction"
          (cond((null mod) nil)
               (t (match (negate item) mod))))

        remove-itm (itm lis)
          "Removes itm, which must be a list, from lis-of-lis,
           e.g. '(a) '((b)(a)(c)) -> '((b)(c))  
           scales up where first parameter at one level less than 
           second,  and will remove lis even if order of items differs."
          (cond((null lis) nil)
               ((matchlists itm (first lis))(remove-itm itm (rest lis)))
               (t (cons (first lis) (remove-itm itm (rest lis))))))

        matchlists (lis1 lis2)
          "Rtns lis2 iff it and lis1 have identical members,e.g. 
           ((a)(b)) = ((b)(a))
           & so can be used to compare models. "
          (cond((equal lis1 lis2) lis2)
               ((null lis1) nil)
               ((and (matchl lis1 lis2)(matchl lis2 lis1)) lis2)))

        matchl (lis1 lis2)
          "Checks that each member of lis1 is in lis2, e.g. 
           '((a)(b)) in '((b)(a)(c)) => T; ignores negation if itms 
           are directly compared, e.g. 
           '(a) and '(- a) => T; but not if mods are compared"
          (cond((null lis1) t)
               ((match (first lis1) lis2)(matchl (rest lis1) lis2))))

        match (item mod)
          "Matchs item with list, e.g. 'a and '(b a) -> t; '(a) 
           and '((b)(a)) => t;
           '((a)(b)) and '( ((a)(b)) c) => t provided order of elements 
           in item is same as in mod;  item can be atom, lis, 
           or lis-of-lis"
          (cond((null mod) nil)
               ((equal item (first mod)) t)
               (t (match item (rest mod)))))

        ; ---------------------------------------------------------------------------------
        ; Section 1.5: Property Functions
        ; ---------------------------------------------------------------------------------

        property-equal (property-1 property-2)
        "This function compares two properties using the standard equality function.
        (property-equal '(A) '(A)) => T
        (property-equal '(A) '(B)) => NIL
        (property-equal '(A) '(- A)) => NIL"
          (equal property-1 property-2))

        negative-property (property)
        "Checks whether a property is negative.
        (negative-property '(A)) => NIL
        (negative-property '(- A)) => T"
          (and
           ;(p-property-p property)
           (equal (car property) '-)))

        ###################################################################################
         Section 1.6: Individual Functions
        ###################################################################################

        individual-equal (individual-1 individual-2)
        "This function returns true if the individuals have the same set of properties, regardless of ordering. 
        It assumes that individuals will be properly formed (ie, no repeat properties).
        (individual-equal '((A)) '((A))) => T
        (individual-equal '((A)) '((A)(B))) => NIL"
          (have-all-properties individual-1 individual-2))

        has-property (property individual)
        "This function determines whether a property is part of a list of properties.
        (has-property '(A) '((A)(B))) => T
        (has-property '(A) '((B)(C))) => NIL"
          (member property individual :test #'property-equal))

        have-all-properties (indiv-1 indiv-2)
        "Checks whether either indiv is a subset (in terms of properties) of the other."
          (and
           (subsetp indiv-1 indiv-2 :test #'property-equal)
           (subsetp indiv-2 indiv-1 :test #'property-equal)))

        conflicting-properties (indiv-1 indiv-2)
        "A check to see whether two indivs are compatible. If they contain the same propety but negated, they are not.
        Ex: A B -C and A B C - the Cs are the same but negated.
        (conflicting-properties '((A) (B) (- C)) '((A) (B) )) => T"
        (let ((cartesian-product (cartesian-product indiv-1 indiv-2)))
          (and 
           (remove-if-not #'(lambda(x) (equal (negate-property (first x)) (second x))) cartesian-product) 
           T)))

        merge-individuals (indiv-1 indiv-2)
          (remove-duplicates (append indiv-1 indiv-2) :test #'property-equal))

        ; ---------------------------------------------------------------------------------
        ; Section 1.7: Model Functions
        ; ---------------------------------------------------------------------------------

        model-has-entity (entity (model q-model))
          "Checks whether a model contains an individual.
           (model-has-indivs '((A)) '( ((A)(B)) ((A)) (T0) ) ) => T
           (model-has-indivs '((A)) '( ((A)(B)) ((C)) (T0) ) ) => NIL"
          (member entity (individuals model) :test #'individual-equal))

        add-footnote ((model model) (new-intension intension))
          "DESTRUCTIVE
           Takes a model and an intension and updates the footnote in the model."
          (setf (footnote model) (append (footnote model) (list (copy-class-instance new-intension))))
          model)

        ; ---------------------------------------------------------------------------------
        ; Section 1.8: Footnote Functions
        ; ---------------------------------------------------------------------------------

        get-footnote-position (footnotes property)
          "Returns a list corresponding to the indices within footnotes in which the property is mentioned in the subj. position. Returns nil if there are none.
           Usage:
           (mentioned-in-footnotes '((include (A) (B)) (include (A) (C))) '(A)) => (0 1)
           (mentioned-in-footnotes '((include (A) (B)) (include (B) (C))) '(C)) => NIL"
          (let ((list-of-positions))
            (do* ((i 0 (+ i 1))
                  (cur-fn (nth i footnotes) (nth i footnotes)))
                ((= (length footnotes) i))
              (if (equal (subject cur-fn) property)
                  (push  i list-of-positions)))
            list-of-positions))

        ; ---------------------------------------------------------------------------------
        ; Section 1.9: Intension Functions
        ; ---------------------------------------------------------------------------------

        cardinality-value ((intension q-intension))
          "Returns concrete value of cardinality, e.g.,
           (cardinality-value Iab) => 4"
          (let
              ((assumption)
               (exact-value))
            (dolist (condition (cardinality intension))
              (if (equal (first condition) '?)
                  (setf assumption (second condition))
                (if (equal (first condition) '=)
                    (setf exact-value (second condition)))))
            (if exact-value
                exact-value
              assumption)))

        numprop-value ((intension q-intension))
          "Returns concrete value of numprop, e.g.,
           (numprop-value Iab) => 2"
          (cadr (numprop intension)))

        is-setmem ((intension q-intension) &key (n (numprop-value intension)))
          "If intension is a set membership relation, rtn it, else nil"
          (when (and (equalp (numprop intension) `(= ,n))
                     (equalp (boundary intension) `((= ,n)))
                     (polarity intension) (footnotes intension))
            intension))

        is-most ((intension q-intension))
          "If intension specifies 'most', rtn it, else nil"
          (when (and (equalp (boundary intension) '((< CARDINALITY) (> (* 0.5 CARDINALITY))))
                     (polarity intension)
                     (footnotes intension))
            intension))

        is-few ((intension q-intension))
          "If intension specifies 'few', rtn it, else nil"
          (when (and (equalp (boundary intension) '((< (* 0.5 CARDINALITY)) (> 0)))
                     (polarity intension)
                     (footnotes intension))
            intension))
          
        is-all ((intension q-intension))
          "If intension is in mood A, rtn it, else nil"
          (when (and (equalp (boundary intension) '((= CARDINALITY)))
                     (polarity intension)
                     (footnotes intension))
            intension))

        is-none ((intension q-intension))
          "If intension is in mood E, rtn it, else nil"
          (when (and (equalp (boundary intension) '((= CARDINALITY)))
                     (not (polarity intension))
                     (footnotes intension))
            intension))

        is-some ((intension q-intension))
          "If intension is in mood I, rtn it, else nil"
          (when (and (equalp (boundary intension) '((<= CARDINALITY) (> 0)))
                     (not (negative-intension intension)))
            intension))

        is-some-not ((intension q-intension))
          "If intension is in mood O, rtn it, else nil"
          (when (and (equalp (boundary intension) '((<= CARDINALITY) (> 0)))
                     (negative-intension intension))
            intension))

        mood ((intension q-intension))
          "Outputs mood of assertion
           (mood (parse '(some a are not b))) => O "
            (cond
             ((is-all intension)      'A)
             ((is-some-not intension) 'O)
             ((is-none intension)     'E)
             ((is-some intension)     'I)
             ((is-most intension)     'M)
             ((is-few intension)      'F)
             ((is-setmem intension)  `(X ,(is-setmem intension)))
             (t (error "Assertion cannot be intrepreted"))))

        is-before ((intension t-intension))
          "If intension is 'before' relation, rtn it, else nil"
          (when (equal (first (precedence intension)) '<)
            intension))

        is-after ((intension t-intension))
          "If intension is 'after' relation, rtn it, else nil"
          (when (equal (first (precedence intension)) '>)
            intension))

        is-while ((intension t-intension))
          "If intension is 'while' relation, rtn it, else nil"
          (when (equal (first (precedence intension)) 'include)
            intension))

        is-during ((intension t-intension))
          "If intension is 'during' relation, rtn it, else nil"
          (when (equal (first (precedence intension)) 'properly-include)
            intension))

        relation ((intension t-intension))
          "Outputs relation of assertion
           (relation (parse '(A happened before B))) => B "
          (cond
           ((is-before intension) 'B)
           ((is-after intension) 'A)
           ((is-while intension) 'W)
           ((is-during intension) 'D)
           (t (error "Assertion cannot be intrepreted"))))

        is-affirmative-atom ((intension s-intension))
          "If intension is an affirmative atom 'A', rtn it, else nil"
          (when (and (equal (first-only intension)  'possible)
                     (equal (second-only intension)  'impossible)
                     (equal (both intension)    'impossible)
                     (equal (neither intension) 'impossible)
                     (null (second-clause intension)))
            intension))

        is-negative-atom ((intension s-intension))
          "If intension is a negative atom '-A', rtn it, else nil"
          (when (and (equal (first-only intension)  'impossible)
                     (equal (second-only intension)  'impossible)
                     (equal (both intension)    'impossible)
                     (equal (neither intension) 'possible)
                     (null (second-clause intension)))
            intension))

        is-atom ((intension s-intension))
          "If intension is an atom (A or -A), rtn it, else nil"
          (or (is-affirmative-atom intension)
              (is-negative-atom intension)))

        is-and ((intension s-intension))
          "If intension is a conjunction (A and B), rtn it, else nil"
          (when (and (equal (first-only intension)  'impossible)
                     (equal (second-only intension)  'impossible)
                     (equal (both intension)    'possible)
                     (equal (neither intension) 'impossible))
            intension))

        is-ori ((intension s-intension))
          "If intension is an inclusive disjunction (A v B), rtn it, else nil"
          (when (and (equal (first-only intension)  'possible)
                     (equal (second-only intension)  'possible)
                     (equal (both intension)    'possible)
                     (equal (neither intension) 'impossible))
            intension))

        is-ore ((intension s-intension))
          "If intension is an inclusive disjunction (A xor B), rtn it, else nil"
          (when (and (equal (first-only intension)  'possible)
                     (equal (second-only intension)  'possible)
                     (equal (both intension)    'impossible)
                     (equal (neither intension) 'impossible))
            intension))

        is-if ((intension s-intension))
          "If intension is a conditional (A -> B), rtn it, else nil"
          (when (and (equal (first-only intension)  'impossible)
                     (equal (second-only intension)  'possible)
                     (equal (both intension)    'possible)
                     (equal (neither intension) 'possible))
            intension))

        is-iff ((intension s-intension))
          "If intension is a biconditional (A <-> B), rtn it, else nil"
          (when (and (equal (first-only intension)  'impossible)
                     (equal (second-only intension)  'impossible)
                     (equal (both intension)    'possible)
                     (equal (neither intension) 'possible))
            intension))

        reverse-modal (x)
          "Returns reversed modal status, i.e., impossible <-> possible"
          (if (equal x 'possible) 'impossible
            (if (equal x 'impossible) 'possible)))

        negate ((int s-intension))
          "Negates an s-intension by swapping impossible states to possible
           and vice versa. Handles atoms specially (swaps between first-only and
           neither)"
          (cond
           ((is-affirmative-atom int)
            (make-instance 's-intension
                           :first-clause  (first-clause int)
                           :second-clause (second-clause int)
                           :first-only    'impossible
                           :second-only   'impossible
                           :both          'impossible
                           :neither       'possible))
           ((is-negative-atom int)
            (make-instance 's-intension
                           :first-clause  (first-clause int)
                           :second-clause (second-clause int)
                           :first-only  'possible
                           :second-only  'impossible
                           :both    'impossible
                           :neither 'impossible))
           (t
            (make-instance 's-intension
                           :first-clause  (first-clause int)
                           :second-clause (second-clause int)
                           :first-only  (reverse-modal (first-only int))
                           :second-only  (reverse-modal (second-only int))
                           :both    (reverse-modal (both int))
                           :neither (reverse-modal (neither int)))))
          int)


        ; ---------------------------------------------------------------------------------
        ; Section 1.10: Utility Functions
        ; ---------------------------------------------------------------------------------

        cartesian-product (list-1 list-2)
          (let ((cartesian-product))
            (dolist (elt-1 list-1 cartesian-product)
              (dolist (elt-2 list-2)
                (push (list elt-1 elt-2) cartesian-product)))))

        ; ---------------------------------------------------------------------------------
        ; Section 1.11: Tracer classes and functions
        ; ---------------------------------------------------------------------------------

        (defclass tracer ()
          ((enabled :accessor enabled :initarg :e   :initform nil)
           (steps   :accessor steps   :initarg :s   :initform -1)
           (verbose :accessor verbose :initarg :v   :initform nil)
           (runtime :accessor runtime :initarg :r   :initform (get-internal-run-time))
           (response      :accessor response :initarg :r :initform nil)
           (initial-model :accessor initial-model :initarg :im :initform nil)
           (final-model :accessor final-model :initarg :fm :initform nil)
           (trace         :accessor trace-output   :initarg :tr  :initform nil))
          (:documentation "Class for tracer logging"))

        (defparameter *tracer* (make-instance 'tracer))

        compute-runtime ()
          "Converts runtime to process cycle"
          (- (get-internal-run-time) (runtime *tracer*)))

        trace-header ()
          "Adds header to system trace on initial output of tracer and on every tracer reset"
          (case (steps *tracer*)
            (-1
             (format t "---- --------- ----------------------------------------------------------------- ------- ~%")
             (format t "Step System    Description                                                       Runtime  ~%")
             (format t "---- --------- ----------------------------------------------------------------- ------- ~%")
             (setf (runtime *tracer*) (get-internal-run-time))
             (incf (steps *tracer*))
             (format t "~4@<~A~> ~9@<~A~> ~65@<~A~> ~7@<~A~>~%"
                     (steps *tracer*) "--" "Initialized trace" (compute-runtime)))
            (0
             (format t "---- --------- ----------------------------------------------------------------- ------- ~%")
             (setf (runtime *tracer*) (get-internal-run-time))
             (format t "~4@<~A~> ~9@<~A~> ~65@<~A~> ~7@<~A~>~%"
                     (steps *tracer*) "--" "Reset trace" (compute-runtime)))))

        tracer (system description &key (model nil))
          "Adds tracing line to system trace"
          (let ((model (cond
                        ((null model) nil)
                        ((listp model) (mapcar #'copy-class-instance model))
                        (model         (copy-class-instance model)))))
            (when (enabled *tracer*)
                (when (member system (list "System 1" "System 2" "Control" "Language") :test #'string-equal)
                  (incf (steps *tracer*)))
                (push (list (if (string-equal system "") "" (steps *tracer*)) system description (compute-runtime) model)
                      (trace-output *tracer*))
              (when (verbose *tracer*)
                (trace-header)
                (format t "~4@<~A~> ~9@<~A~> ~65@<~A~> ~7@<~A~>~%" (if (string-equal system "") "" (steps *tracer*))
                        system description (compute-runtime))))))

        trc (system description &key (m nil))
          "Abbreviation wrapper fn for tracer"
          (tracer system description :model m))

        initialize-tracer (&key (enabled t) (steps -2) (verbose nil) (runtime (get-internal-run-time)))
          "Initializes tracer to defaults based on parameters"
          (setf *tracer* (make-instance 'tracer :e enabled :s steps :v verbose :r runtime)))

        enable-tracer (&key (verbose nil))
          "Enables tracer and sets trace verbosity"
          (if *tracer*
              (progn
                (setf (enabled *tracer*) t)
                (setf (verbose *tracer*) verbose))
            (initialize-tracer :v verbose)))

        disable-tracer ()
          "Disables tracer"
          (setf (enabled *tracer*) nil))

        reset-tracer ()
          "Resets tracer"
          (unless (< (steps *tracer*) 0)
            (setf (steps *tracer*) -1))
          (setf (trace-output *tracer*) nil)
          (setf (response *tracer*) nil)
          (setf (initial-model *tracer*) nil)
          (setf (final-model *tracer*) nil)
          (setf (runtime *tracer*) (get-internal-run-time)))

        trace-model (model)
          "Outputs model in tracer format"
          (let (lines
                (output (make-array 0
                                    :element-type 'character 
                                    :adjustable t 
                                    :fill-pointer 0)))
            (print-model model :template nil :output output)
            (setf lines (rest (split-sequence (format nil "~%") output)))
            (trc "Printer" (format nil "Printing model ~A" model))
            (dolist (line lines)
              (trc "" line))))

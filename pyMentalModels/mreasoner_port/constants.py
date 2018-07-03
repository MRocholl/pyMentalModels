#: Global variable that controls the combinatoric depth of the exhaustic search algorithms defined in Counterexamples.lisp
exhaustive_search_depth = 7

#: Parameter that enables or disables stochastic system.
stochastic = False

#: Parameter that establishes the number of attempts to build a stochastic model before the system stops trying.
build_attempts = 1000

#: Parameter that control the execution of system 2 processes (i.e., sigma = search) across the system as a whole. When sigma = 0, system 2 processes are never called.  When sigma = 1, system 2 processes are always called. When sigma = .6, there is a 60% chance that system 2 processes will be called.
sigma = 0.0

#: Parameter that controls the size of models. Lambda denotes the lambda parameter Poisson distribution. By default, lambda = 4. To set a model's size, the system will sample from a left_truncated Poisson distribution with lambda parameter = 4. The system will sample from the distribution and use that sample as the size (cardinality) of the model.)
poisson_lambda_size_models = 4.0

#: Parameter that controls the construction of canonical models, i.e., models whose individuals are specified in the intensions, i.e., epsilon = error. When epsilon = 0, the system always builds canonical models. When epsilon = 1, every time the system needs to build a token in a model, it will do so with respect to the intensional constraints alone. When epsilon = .6, every time the system needs to build a token in a model, there will be a 60% chance that the system will draw from canonical tokens.
epsilon = 0.0

#: Parameter that controls whether individuals weaken their initial conclusion after finding a counterexample or whether they simply report 'NVC' once a counterexample is found. When omega = 1.0, weakening always occurs; when omega = 0.0, individuals always report 'NVC' when a counterexample is found. When omega = 0.6, there's a 60% chance that weakening will occur.)
omega = 1.0


synthetic_data = False


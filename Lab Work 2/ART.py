from randomizer import randomizer as rnd

class ART1:
    '''How to use:
       set_parameters -> set_random_database -> perform'''

    def __init__(self):
        # Number of item types
        self.max_items = 0
        # Number of customers
        self.max_customers = 0
        # Number of prototype vectors
        self.total_prototype_vectors = 0
        # Beta parameter
        self.beta = 0
        # Vigilance parameter
        self.vigilance = 0
        # Prototype vectors for each cluster
        self.prototype_vectors = []
        # Purchase database
        self.database = []
        # Clusters that store similar feature vectors
        self.clusters = [[]]

        self.membership = []

        self.recommendations = []

    def get_clusters(self):
        clusters_str = ''
        pos = 1
        for cluster in self.clusters:
            clusters_str += 'Prototype vector:\n{}\nCluster {}:\n'.format(self.prototype_vectors[pos - 1], pos)
            for row in cluster:
                clusters_str += '{}\n'.format(row)
            pos += 1
        return clusters_str

    def perform(self):
        # Check similarity of all feature vectors with prototype vectors
        pos = 0
        is_changed = True
        old_clusters = []
        while is_changed:
            old_clusters = self.clusters
            for E in self.database:
                is_complete = False
                i = 0
                for P in self.prototype_vectors:
                    ''' || P_i and E||    ||E||
                        -------------- > --------
                        beta + ||P_i||   beta + d   '''
                    a = self.get_vector_magnitude(self.and_vectors(P, E))
                    b = self.beta + self.get_vector_magnitude(P)
                    c = self.get_vector_magnitude(E)
                    d = self.beta + len(E)
                    is_similar = (a / b) > (c / d)
                    # Check for vigilance
                    if is_similar:
                        '''||P_i and E||
                           ------------- < ρ
                               ||E||          '''
                        a = self.get_vector_magnitude(self.and_vectors(P, E))
                        b = self.get_vector_magnitude(E)
                        is_vigilante = (a / b) <= self.vigilance
                        # If the feature vector passed all checks
                        if is_vigilante:
                            ''' P_i = P_i and E '''
                            self.prototype_vectors[i] = self.and_vectors(P, E)
                            self.clusters[i].append(E)
                            is_complete = True
                            break
                    i += 1
                # All prototypes were checked, but the vector was not placed in a cluster
                if not is_complete:
                    # Create a new prototype vector
                    self.prototype_vectors.append(E.copy())
                    self.clusters.append([])
                    self.clusters[len(self.clusters) - 1].append(E.copy())
                pos += 1
            if old_clusters == self.clusters:
                is_changed = False
        return

    def get_recommendation(self, customer):
        pass

    # Set input parameters for the algorithm
    def set_parameters(self, max_items, max_customers, total_prototype_vectors, beta, vigilance):
        self.max_items = max_items
        self.max_customers = max_customers
        self.total_prototype_vectors = total_prototype_vectors
        self.beta = beta
        self.vigilance = vigilance

    # Generate a random purchase database
    def set_random_database(self):
        for i in range(0, self.max_customers):
            self.database.append(rnd.get_int_list(self.max_items, 0, 1))
        # Initialize the first prototype vector
        self.prototype_vectors.append(self.database[0].copy())
        return

    # Returns the purchase database
    def get_database(self):
        return self.database

    # Returns the number of non-zero objects
    def get_vector_magnitude(self, vector):
        magnitude = vector.count(1)
        return magnitude

    # Bitwise multiplication of vectors v and w
    def and_vectors(self, v, w):
        result = [x and y for x, y in zip(v, w)]
        return result

    # Sets the database as in the documentation (PROGRAMMING)
    def set_debug_values(self):
        self.database = [[0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
                         [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                         [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
                         [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
                         [1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
                         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                         [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
                         [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
                         [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0]]
        self.prototype_vectors.append(self.database[0].copy())
        self.set_parameters(11, 10, 5, 1.0, 0.9)

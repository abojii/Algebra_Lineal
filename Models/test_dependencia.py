from metodos import are_vectors_dependent

def test_dependent_vectors():
    vectors = [
        [1, 2, 3],
        [2, 4, 6],
        [3, 6, 9]
    ]
    assert are_vectors_dependent(vectors) == True
    print("Test 1 - Vectores dependientes: Correcto")

def test_independent_vectors():
    vectors = [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]
    assert are_vectors_dependent(vectors) == False
    print("Test 2 - Vectores independientes: Correcto")

def test_empty_vectors():
    vectors = []
    assert are_vectors_dependent(vectors) == False
    print("Test 3 - Vectores vacíos: Correcto")

def test_more_vectors_than_dimension():
    vectors = [
        [1, 0],
        [0, 1],
        [1, 1]
    ]
    assert are_vectors_dependent(vectors) == True
    print("Test 4 - Más vectores que dimensión: Correcto")

if __name__ == "__main__":
    test_dependent_vectors()
    test_independent_vectors()
    test_empty_vectors()
    test_more_vectors_than_dimension()

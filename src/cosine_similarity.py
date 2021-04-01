import math

#                                   Sum[n,i=1](Ai * Bi)
#similarity(A,B) = -------------------------------------------------------
#                   Sqrt(Sum[n,i=1](Ai * Ai)) * Sqrt(Sum[n,i=1](Bi * Bi))

def cosine_similarity(A, B):
    denominator_A, denominator_B, numerator = 0, 0, 0
    #numerator = sum()
    numerator     = sum([(a*b)  for a, b in zip(A,B)])
    denominator_A = sum([(a**2) for a    in A])
    denominator_B = sum([(b**2) for b    in B])
    result = (numerator)/(math.sqrt(denominator_A)*math.sqrt(denominator_B))
    print(result)
    return result

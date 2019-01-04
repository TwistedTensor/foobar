from copy import deepcopy
class Frac:
    def __init__(self,num,den):
        d = gcd(num,den)
        num //= d
        den //= d
        self.num = num
        self.den = den
    
    def __add__(self,other):
        num = self.num*other.den + other.num*self.den
        den = self.den*other.den
        result = Frac(num,den)
        return result
        
    def __sub__(self,other):
        num = self.num*other.den - other.num*self.den
        den = self.den*other.den
        result = Frac(num,den)
        return result
    
    def __mul__(self,other):
        num = self.num*other.num
        den = self.den*other.den
        result = Frac(num,den)
        return result
    
    def __div__(self,other):
        num = self.num*other.den
        den = self.den*other.num
        result = Frac(num,den)
        return result
    
    def __eq__(self,other):
        if type(other) == type(self):
            return (self.num * other.den) == (self.den * other.num)
        else:
            return (self.num*1./self.den) == other
    
    def __repr__(self):
        return '{}/{}'.format(self.num,self.den)
        
class Matrix:
    def __init__(self,rows):
        self.rows = rows
        self.columns = [[row[i] for row in rows] for i in range(len(rows[0]))]
    
    def pivot(self,i,j):
        pivot = self.rows[i][j]
        if pivot == 0:
            return Matrix(deepcopy(self.rows))
        pivot_row = [v/pivot for v in self.rows[i]]
        new_rows = []
        for k,row in enumerate(self.rows):
            if k == i:
                new_rows.append(pivot_row)
            else:
                c = row[j]
                new_row = [row[l]-c*p for l,p in enumerate(pivot_row)]
                new_rows.append(new_row)
        return Matrix(new_rows)
    
    def next_pivot(self):
        pivot_row = 0
        for i,column in enumerate(self.columns):
            non_pivots_are_zero = all([v == 0 for j,v in enumerate(column) if j != pivot_row])
            if non_pivots_are_zero & (column[pivot_row]==1):
                if pivot_row == len(self.rows)-1:
                    return pivot_row,i
                pivot_row += 1
                continue
            if non_pivots_are_zero & (column[pivot_row]==0):
                continue
            return pivot_row,i
        
    def rref(self):
        current_m = Matrix(deepcopy(self.rows))
        while True:
            next_piv = current_m.next_pivot()
            next_m = current_m.pivot(*next_piv)
            if next_m == current_m:
                return current_m
            current_m = next_m
    
    def dot(self,other):
        product = [[Frac(0,1) for col in other.columns] for row in self.rows]
        for i,row in enumerate(self.rows):
            for j,col in enumerate(other.columns):
                for k in range(len(row)):
                    product[i][j] += row[k]*col[k]
        return product
    
    def augment(self,new_col):
        new_rows = []
        for i,row in enumerate(self.rows):
            new_row = row.append(new_col[i])
            new_rows.append(row)
        return Matrix(new_rows)
            
    def __add__(self,other):
        m = len(self.rows)
        n = len(self.columns)
        new_rows = [[self.rows[i][j]+other.rows[i][j] for j in range(n)] for i in range(m)]
        return Matrix(new_rows)
    
    def __sub__(self,other):
        m = len(self.rows)
        n = len(self.columns)
        new_rows = [[self.rows[i][j]-other.rows[i][j] for j in range(n)] for i in range(m)]
        return Matrix(new_rows)
    
    def __eq__(self,other):
        return self.rows == other.rows
        
    def __repr__(self):
        return self.rows.__repr__()

def gcd(a,b):
    while b:
        a,b = b,a%b
    return a
        
def common(*fracs):
    first,rest = fracs[0],fracs[1:]
    if len(fracs)==1:
        return [first.num,first.den]
    common_rest = common(*rest)
    den_rest = common_rest[-1]   # get old denominator
    d = gcd(first.den,den_rest)  # gcd of new denominator and old denominator
    a = den_rest//d              # factor to multiply new numerator by
    b = first.den//d             # factor to multiply old numerators by
    cd = (first.den*den_rest)//d # new common denominator
    nums = [a*first.num]+[b*r for r in common_rest[:-1]]+[cd]
    return nums
    
def answer(m):
    non_term = []
    term = []
    for row in m:
        row_sum = sum(row)
        if row_sum == 0:
            term.append(row)
        else:
            row = [Frac(v,row_sum) for v in row]
            non_term.append(row)
    m = non_term + term
    k = len(non_term)
    l = len(term)
    a = Matrix([[m[i][j] for i in range(k)] for j in range(k)])
    b = Matrix([[m[i][j] for i in range(k)] for j in range(k,l+k)])
    I = Matrix([[Frac(int(i==j),1) for i in range(k)] for j in range(k)])
    e_i = [Frac(int(i==0),1) for i in range(k)]
    aug = (I-a).augment(e_i)
    last_col = aug.rref().columns[-1]
    v_0 = Matrix([[val] for val in last_col])
    v = b.dot(v_0)
    ans = common(*[f[0] for f in v])
    details = {
        'a':a,
        'b':b,
        'I':I,
        'e_i':e_i,
        'aug':aug,
        'last_col':last_col,
        'v_0':v_0,
        'v':v
    }
    return ans

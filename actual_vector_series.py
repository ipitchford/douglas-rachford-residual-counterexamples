"""Direct rational truncated-series check of Appendix A's actual vector."""
from fractions import Fraction as F
import json

def require(x,message):
    if not x: raise ArithmeticError(message)

def add(a,b):return [x+y for x,y in zip(a,b)]
def mul(a,b):return [sum(a[j]*b[k-j] for j in range(k+1)) for k in range(3)]
def scale(a,s):return [s*x for x in a]
Z=[F(0)]*3
O=[F(1),F(0),F(0)]
def mm(a,b):return [[add(mul(a[i][0],b[0][j]),mul(a[i][1],b[1][j])) for j in range(2)] for i in range(2)]
def ma(a,b):return [[add(a[i][j],b[i][j]) for j in range(2)] for i in range(2)]
def ms(a,s):return [[scale(a[i][j],s) for j in range(2)] for i in range(2)]

def main():
    I=[[O,Z],[Z,O]]
    Q=[[[F(1),F(0),-F(3,4)],[F(0),F(1,2),F(0)]],
       [[F(0),-F(1,2),F(0)],[F(1),F(0),-F(3,4)]]]
    P=I;S=[[Z,Z],[Z,Z]]
    for _ in range(8):S=ma(S,P);P=mm(Q,P)
    R=ma(ms(Q,2),ms(I,-1))
    D=add(mm(R,S)[0][0],O)
    require(D==[F(9),F(0),F(-61)],"D coefficient mismatch")
    inv=[1/D[0],-D[1]/D[0]**2,D[1]**2/D[0]**3-D[2]/D[0]**2]
    row=mm(R,P)[0]
    K=mm(P,ma(ma(I,ms(Q,-1)),[[mul(row[0],inv),mul(row[1],inv)],[Z,Z]]))
    expected=[[[F(1,9),F(0),F(1,324)],[F(0),F(1,18),F(0)]],
              [[F(0),F(1,18),F(0)],[F(0),F(0),F(19,36)]]]
    require(K==expected,"K coefficient mismatch")
    v=[add(K[i][0],mul(K[i][1],[F(0),F(1,2),F(0)])) for i in range(2)]
    ratio=mul(add(mul(v[0],v[0]),mul(v[1],v[1])),[F(1),F(0),-F(1,4)])
    require(ratio==[F(1,81),F(0),F(5,729)],"Actual vector coefficient mismatch")
    print(json.dumps({"ratio_coefficients":[str(x) for x in ratio],"status":"PASS","scope":"Exact degree-two coefficients only; analytic remainder and branch validity require written proof"}))
if __name__=="__main__":main()

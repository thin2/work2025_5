import re
import math
from fractions import Fraction

class Quad:
    __slots__ = ('a','b')
    def __init__(self, a=0, b=0):
        self.a, self.b = Fraction(a), Fraction(b)
    def __add__(self, o): return Quad(self.a+o.a, self.b+o.b)
    def __sub__(self, o): return Quad(self.a-o.a, self.b-o.b)
    def __mul__(self, o):
        if isinstance(o, Quad):
            return Quad(self.a*o.a + 2*self.b*o.b, self.a*o.b + self.b*o.a)
        return Quad(self.a*o, self.b*o)
    def __neg__(self): return Quad(-self.a, -self.b)
    def __truediv__(self, s): return Quad(self.a/s, self.b/s)
    def to_float(self): return float(self.a + self.b*math.sqrt(2))
    def __str__(self):
        parts=[]
        if self.a: parts.append(str(self.a))
        if self.b:
            b=self.b; unit = "√2" if abs(b)==1 else f"{abs(b)}√2"
            parts.append(("" if b>0 and parts else "-") + unit)
        return ' + '.join(parts).replace('+ -','- ') or '0'

# 预计算 trig:{deg:(cos, sin)} 二次表达式
COS_SIN = {deg:(Quad(*c), Quad(*s)) for deg,(c,s) in {
    0:  ((1,0),(0,0)), 45:((0,1),(0,1)), 90:((0,0),(1,0)),
    135:((0,-1),(0,1)),180:(-1,0),(0,0),225:((0,-1),(0,-1)),
    270:((0,0),(-1,0)),315:((0,1),(0,-1)}.items()}

SHAPES = {
    'TangGrandTri':[(0,0),(2,0),(2,2)],
    'TangMoyTri':  [(0,0),(1,1),(2,0)],
    'TangPetTri':  [(0,0),(1,0),(1,1)],
    'TangCar':     [(0,0),(1,0),(1,1),(0,1)],
    'TangPara':    [(0,0),(1,0),(2,1),(1,1)],
}

class Piece:
    def __init__(self, shape, opts, xs, ys):
        xf = 'xscale=-1' in opts; yf = 'yscale=-1' in opts
        r = int(re.search(r'rotate=([+-]?\d+)', opts or '0').group(1))%360
        if xf and yf: r=(r+180)%360; xf=yf=False
        self.xm, self.ym = self._eval(xs), self._eval(ys)
        ce, se = COS_SIN[r]
        pts = []
        for x0,y0 in SHAPES[shape]:
            xr = Quad(x0)*ce - Quad(y0)*se
            yr = Quad(x0)*se + Quad(y0)*ce
            if xf: xr = -xr
            if yf: yr = -yr
            pts.append((xr+self.xm, yr+self.ym))
        self.vertices = self._order(pts)

    def _eval(self, e):
        e = e.strip('{}')
        b = sum(Fraction(m.group()) for m in re.finditer(r'[+-]?\d+(?:/\d+)?(?=\*?sqrt)', e))
        a_expr = re.sub(r'[+-]?\d+(?:/\d+)?\*?sqrt\(2\)', '', e) or '0'
        return Quad(Fraction(eval(a_expr, {'__builtins__':None}, {})), b)

    @staticmethod
    def _order(pts):
        cx = sum(p[0].to_float() for p in pts)/len(pts)
        cy = sum(p[1].to_float() for p in pts)/len(pts)
        ang = lambda p:-math.atan2(p[1].to_float()-cy, p[0].to_float()-cx)
        ps = sorted(pts, key=ang)
        top = max(ps, key=lambda p:p[1].to_float()); i=ps.index(top)
        return ps[i:]+ps[:i]

class Tangram:
    def __init__(self, fname):
        self.pieces=[]
        txt = re.sub(r'%.*','', open(fname, encoding='utf-8').read()).replace(' ','')
        for opts,xs,ys,sh in re.findall(
            r'\\PieceTangram\[([^\]]*)\](?:<[^>]*>)?\((\{[^}]*\}),(\{[^}]*\})\)\{([^}]+)\}', txt):
            name = {'TangGrandTri':'Large triangle','TangMoyTri':'Medium triangle',
                    'TangPetTri':'Small triangle','TangCar':'Square','TangPara':'Parallelogram'}[sh]
            self.pieces.append((name, Piece(sh, opts, xs, ys)))

    def draw_pieces(self, out):
        xs=[v[0].to_float() for _,p in self.pieces for v in p.vertices]
        ys=[v[1].to_float() for _,p in self.pieces for v in p.vertices]
        bounds = min(xs), max(xs), min(ys), max(ys)
        with open(out, 'w', encoding='utf-8') as f:
            f.write("""\\documentclass{standalone}
\\usepackage{tikz}
\\begin{document}
\\begin{tikzpicture}
""")
            f.write(f"\\draw[step=5mm] ({bounds[0]-0.5},{bounds[2]-0.5}) grid ({bounds[1]+0.5},{bounds[3]+0.5});\n")
            for _,p in self.pieces:
                pts = ' -- '.join(f"({str(v[0])},{str(v[1])})" for v in p.vertices)
                f.write(f"\\draw[ultra thick] {pts} -- cycle;\n")
            f.write("\\fill[red] (0,0) circle (3pt);\n\\end{tikzpicture}\\end{document}")
# T = TangramPuzzle('cat.tex')
# T.draw_pieces('cat1.tex')
# for piece in T.transformations:
#     print(f'{piece:16}', T.transformations[piece], sep=': ')
# print(T)
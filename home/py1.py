
import re
import math
from fractions import Fraction

def frac(val):
    return Fraction(val)

class QuadraticExpr:
    def __init__(self, a=0, b=0):

        self.a = Fraction(a)
        self.b = Fraction(b)

    def __add__(self, other):
        return QuadraticExpr(self.a + other.a, self.b + other.b)

    def __sub__(self, other):
        return QuadraticExpr(self.a - other.a, self.b - other.b)

    def __mul__(self, other):

        if isinstance(other, QuadraticExpr):
            a = self.a * other.a + 2 * self.b * other.b
            b = self.a * other.b + self.b * other.a
            return QuadraticExpr(a, b)
        else:
            return QuadraticExpr(self.a * other, self.b * other)
    def __truediv__(self, scalar):

        return QuadraticExpr(self.a / scalar, self.b / scalar)

    def __str__(self):
        a, b = self.a, self.b
        if b == 0:
            return simplify_fraction(a)
        if a == 0:
            if b == 1: return "√2"
            if b == -1: return "-√2"
            return f"{simplify_fraction(b)}√2"
        # both a and b
        a_str = simplify_fraction(a)
        if b == 1:
            b_str = "√2"
        elif b == -1:
            b_str = "√2"
            a_str = f"{a_str} -"
            return f"{a_str} √2"
        else:
            b_str = f"{simplify_fraction(abs(b))}√2"
        sign = " + " if b > 0 else " - "
        return f"{a_str}{sign}{b_str}"

    def to_float(self):
        return float(self.a + self.b * math.sqrt(2))

RAW_VERTICES = {
    'TangGrandTri': [(0,0), (2,0), (2,2)],
    'TangMoyTri':   [(0,0), (1,1), (2,0)],
    'TangPetTri':   [(0,0), (1,0), (1,1)],
    'TangCar':      [(0,0), (1,0), (1,1), (0,1)],
    'TangPara':     [(0,0), (1,0), (2,1), (1,1)],

}

COS_SIN_MAP = {
    0:   (QuadraticExpr(1,0),       QuadraticExpr(0,0)),
    45:  (QuadraticExpr(0,1)/2,     QuadraticExpr(0,1)/2),
    90:  (QuadraticExpr(0,0),       QuadraticExpr(1,0)),
    135: (QuadraticExpr(0,-1)/2,    QuadraticExpr(0,1)/2),
    180: (QuadraticExpr(-1,0),      QuadraticExpr(0,0)),
    225: (QuadraticExpr(0,-1)/2,    QuadraticExpr(0,-1)/2),
    270: (QuadraticExpr(0,0),       QuadraticExpr(-1,0)),
    315: (QuadraticExpr(0,1)/2,     QuadraticExpr(0,-1)/2),
}



def find_left_top(pts):
    vals = [(p[0].to_float(), p[1].to_float(), p) for p in pts]
    max_y = max(y for x,y,_ in vals)
    cands = [t for t in vals if abs(t[1]-max_y)<1e-6]
    return min(cands, key=lambda t: t[0])[2]


def sort_clockwise(pts):

    cx = sum(p[0].to_float() for p in pts) / len(pts)
    cy = sum(p[1].to_float() for p in pts) / len(pts)

    def angle_from_center(p):
        dx = p[0].to_float() - cx
        dy = p[1].to_float() - cy

        return -math.atan2(dy, dx)

    pts_sorted = sorted(pts, key=angle_from_center)

    lt = find_left_top(pts_sorted)
    i = pts_sorted.index(lt)
    return pts_sorted[i:] + pts_sorted[:i]


class Piece:
    def __init__(self, kind, xflip, yflip, rotate, x_move_expr, y_move_expr):
        self.kind   = kind
        self.xflip  = xflip
        self.yflip  = yflip
        self.rotate = rotate % 360

        self.x_move = QuadraticExpr(0, 0)
        self.y_move = QuadraticExpr(0, 0)

        self.x_move = self._eval_coord(x_move_expr)
        self.y_move = self._eval_coord(y_move_expr)
        self.vertices = self._compute_vertices()

    def _eval_coord(self, expr):
        e = expr.strip()
        if e.startswith('{') and e.endswith('}'):
            e = e[1:-1].strip()
        a = Fraction(0)
        b = Fraction(0)

        pattern = r'([+-]?(?:\d+(?:/\d+)?|\d*\.\d+))\*?sqrt\(2\)|([+-]?)sqrt\(2\)'

        for m in re.finditer(pattern, e):
            if m.group(1):
                coef = Fraction(m.group(1))
            else:
                coef = Fraction(1)
                if m.group(2) == '-':
                    coef = -coef
            b += coef


        e_no = re.sub(pattern, '', e)
        if e_no.strip() not in ('', '+', '-'):
            a = Fraction(eval(e_no, {'__builtins__': None}, {}))
        elif e_no.strip() == '-':
            a = Fraction(-1)

        return QuadraticExpr(a, b)
    def _compute_vertices(self):
        angle = self.rotate
        if angle not in COS_SIN_MAP:
            raise ValueError(f"Unsupported rotate angle: {angle}")
        cos_e, sin_e = COS_SIN_MAP[angle]
        res = []
        for x0, y0 in RAW_VERTICES[self.kind]:

            vx = QuadraticExpr(x0, 0)
            vy = QuadraticExpr(y0, 0)

            xr = vx * cos_e - vy * sin_e
            yr = vx * sin_e + vy * cos_e

            if self.xflip:
                xr = QuadraticExpr(0,0) - xr
            if self.yflip:
                yr = QuadraticExpr(0,0) - yr

            px = xr + self.x_move
            py = yr + self.y_move
            res.append((px, py))

        return sort_clockwise(res)


    def left_top_vertex(self):
        return find_left_top(self.vertices)

def simplify_fraction(frac):
    return str(frac.numerator) if frac.denominator == 1 else f"{frac.numerator}/{frac.denominator}"


class TangramPuzzle:
    def __init__(self, filename):
        self.transformations = {}
        self.pieces = []
        self._parse_file(filename)

    def _parse_file(self, filename):
        text = open(filename, encoding='utf-8').read()
        text = re.sub(r"%.*", "", text)
        text = text.replace(' ', '')
        pattern = re.compile(r"""
            \\PieceTangram\[[^\]]*\]
            (?:<([^>]*)>)?
            \(\{([^}]*)\},\{([^}]*)\}\)
            \{([^}]+)\}
        """, re.VERBOSE)
        matches = pattern.findall(text)

        counts = {'TangGrandTri':0, 'TangMoyTri':0, 'TangPetTri':0}
        for opts, xs, ys, shape in matches:
            xflip = 'xscale=-1' in (opts or '')
            yflip = 'yscale=-1' in (opts or '')
            m = re.search(r"rotate=([+-]?\d+)", opts or '')
            rotate = int(m.group(1)) if m else 0
            if xflip and yflip:
                rotate += 180
                xflip = False
                yflip = False
            rotate %= 360


            if shape == 'TangGrandTri':
                counts['TangGrandTri'] += 1
                name = f"Large triangle {counts['TangGrandTri']}"
            elif shape == 'TangMoyTri':
                name = "Medium triangle"
            elif shape == 'TangPetTri':
                counts['TangPetTri'] += 1
                name = f"Small triangle {counts['TangPetTri']}"
            elif shape == 'TangCar':
                name = "Square"
            elif shape == 'TangPara':
                name = "Parallelogram"
            else:
                continue
            self.transformations[name] = {'rotate':rotate,'xflip':xflip}
            piece = Piece(shape, xflip, yflip, rotate, xs, ys)
            self.pieces.append((name, piece))

    def _eval_coord(self, expr):
        e = expr.strip()
        if e.startswith('{') and e.endswith('}'):
            e = e[1:-1].strip()
        e = e.replace('sqrt(2)', 'math.sqrt(2)')
        val = eval(e, {'__builtins__':None}, {'math':math})
        if isinstance(val, set):
            if len(val) == 1:
                val = next(iter(val))
            else:
                raise ValueError(f"Ambiguous coordinate set: {val}")
        if not isinstance(val, (int, float)):
            raise ValueError(f"Invalid coordinate value: {val}")
        return float(val)

    def __str__(self):
        def format_expr(expr):
            a, b = expr.a, expr.b
            parts = []
            if a != 0:
                parts.append(simplify_fraction(a))
            if b != 0:
                if b == 1:
                    parts.append("√2")
                elif b == -1:
                    parts.append("-√2")
                else:
                    b_str = f"({simplify_fraction(b)})" if b.denominator != 1 else simplify_fraction(b)
                    parts.append(f"{b_str}√2")
            return " + ".join(parts).replace("+ (-", "- (").replace('+ -', "- ") if parts else "0"

        sorted_pieces = sorted(
            self.pieces,
            key=lambda np: (

                -sort_clockwise(np[1].vertices)[0][1].to_float(),
                 sort_clockwise(np[1].vertices)[0][0].to_float(),
                 sort_clockwise(np[1].vertices)[1][1].to_float(),
                 sort_clockwise(np[1].vertices)[1][0].to_float(),
            )
        )
        self.pieces = sorted_pieces
        lines = []
        for name, piece in self.pieces:
            coords = [f"({format_expr(vx)}, {format_expr(vy)})" for vx, vy in piece.vertices]
            lines.append(f"{name[:15].ljust(15)}: [" + ", ".join(coords)+ "]")
        return "\n".join(lines)

    def draw_pieces(self, outname):
        def get_bounds():
            all_x, all_y = [], []
            for _, piece in self.pieces:
                for v in piece.vertices:
                    all_x.append(v[0].to_float())
                    all_y.append(v[1].to_float())
            return min(all_x), max(all_x), min(all_y), max(all_y)

        def grid_limit(val, step=0.5):

            frac = val - math.floor(val)
            if frac==0:
                return math.floor(val)+0.5
            elif frac <=0.5:
                return math.floor(val) + 1.0
            else:
                return math.floor(val) + 1.5

        sorted_pieces = sorted(
            self.pieces,
            key=lambda np: (
                -sort_clockwise(np[1].vertices)[0][1].to_float(),
                sort_clockwise(np[1].vertices)[0][0].to_float(),
                sort_clockwise(np[1].vertices)[1][1].to_float(),
                sort_clockwise(np[1].vertices)[1][0].to_float(),
            )
        )

        xmin, xmax, ymin, ymax = get_bounds()
        xmin_g = -grid_limit(-xmin)
        xmax_g = grid_limit(xmax)
        ymin_g = -grid_limit(-ymin)
        ymax_g = grid_limit(ymax)

        def texify_expr(expr):
            expr = str(expr)
            expr = expr.replace('√2', 'sqrt(2)')
            expr = expr.replace(' ', '')

            expr = re.sub(r'(?<=\d)(?=sqrt\(2\))', '*', expr)

            expr = re.sub(r'(\d+)/(\d+)(?=\*?sqrt\(2\))', r'\1/\2', expr)

            return expr

        with open(outname, 'w', encoding='utf-8') as f:
            f.write("\\documentclass{standalone}\n\\usepackage{tikz}\n\\begin{document}\n\n")
            f.write(f"\\begin{{tikzpicture}}\n")
            f.write(f"\\draw[step=5mm] ({xmin_g}, {ymin_g}) grid ({xmax_g}, {ymax_g});\n")

            for name, piece in sorted_pieces:
                pts = " -- ".join(
                    f"({{{texify_expr(v[0])}}}, {{{texify_expr(v[1])}}})" for v in piece.vertices
                )
                f.write(f"\\draw[ultra thick] {pts} -- cycle;\n")

            f.write("\\fill[red] (0,0) circle (3pt);\n")
            f.write("\\end{tikzpicture}\n\n\\end{document}\n")








#

# T = TangramPuzzle('kangaroo.tex')
#
#
T = TangramPuzzle('cat.tex')
T.draw_pieces('cat1.tex')
for piece in T.transformations:
    print(f'{piece:16}', T.transformations[piece], sep=': ')
print(T)
# T = TangramPuzzle('goose.tex')
# for piece in T.transformations:
#     print(f'{piece:16}', T.transformations[piece], sep=': ')
# print(T)
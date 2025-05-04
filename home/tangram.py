import re
import math
from fractions import Fraction


def simplify_fraction(frac: Fraction) -> str:
    return str(frac.numerator) if frac.denominator == 1 else f"{frac.numerator}/{frac.denominator}"


class QuadraticExpr:
    def __init__(self, coeff_a=0, coeff_b=0):
        self.a = Fraction(coeff_a)
        self.b = Fraction(coeff_b)

    def __add__(self, other):
        return QuadraticExpr(self.a + other.a, self.b + other.b)

    def __sub__(self, other):
        return QuadraticExpr(self.a - other.a, self.b - other.b)

    def __mul__(self, other):
        if isinstance(other, QuadraticExpr):
            new_a = self.a * other.a + 2 * self.b * other.b
            new_b = self.a * other.b + self.b * other.a
            return QuadraticExpr(new_a, new_b)
        return QuadraticExpr(self.a * other, self.b * other)

    def __truediv__(self, scalar):
        return QuadraticExpr(self.a / scalar, self.b / scalar)

    def __neg__(self):
        return QuadraticExpr(-self.a, -self.b)

    def __str__(self):
        a, b = self.a, self.b
        a_str = simplify_fraction(a) if a != 0 else None
        b_str = None

        if b != 0:
            if b == 1:
                b_str = "√2"
            elif b == -1:
                b_str = "-√2"
            else:
                b_str = f"{simplify_fraction(abs(b))}√2"
                if b < 0:
                    b_str = f"- {b_str}" if a_str else f"-{b_str}"

        if a_str and b_str:

            sign = " + " if b > 0 else " - "
            return f"{a_str}{sign}{b_str.replace('-', '') if b < 0 else b_str}"
        elif a_str:
            return a_str
        elif b_str:
            return b_str
        else:
            return "0"  # a=0, b=0

    def to_float(self) -> float:
        return float(self.a + self.b * math.sqrt(2))


RAW_VERTICES = {
    'TangGrandTri': [(0, 0), (2, 0), (2, 2)],
    'TangMoyTri': [(0, 0), (1, 1), (2, 0)],
    'TangPetTri': [(0, 0), (1, 0), (1, 1)],
    'TangCar': [(0, 0), (1, 0), (1, 1), (0, 1)],
    'TangPara': [(0, 0), (1, 0), (2, 1), (1, 1)],
}

COS_SIN_TABLE = {
    0: (QuadraticExpr(1, 0), QuadraticExpr(0, 0)),
    45: (QuadraticExpr(0, 1) / 2, QuadraticExpr(0, 1) / 2),
    90: (QuadraticExpr(0, 0), QuadraticExpr(1, 0)),
    135: (QuadraticExpr(0, -1) / 2, QuadraticExpr(0, 1) / 2),
    180: (QuadraticExpr(-1, 0), QuadraticExpr(0, 0)),
    225: (QuadraticExpr(0, -1) / 2, QuadraticExpr(0, -1) / 2),
    270: (QuadraticExpr(0, 0), QuadraticExpr(-1, 0)),
    315: (QuadraticExpr(0, 1) / 2, QuadraticExpr(0, -1) / 2),
}


def find_left_top_vertex(points):
    entries = [(p[0].to_float(), p[1].to_float(), p) for p in points]
    max_y = max(y for _, y, _ in entries)
    top = [e for e in entries if abs(e[1] - max_y) < 1e-6]
    return min(top, key=lambda t: t[0])[2]


def sort_1(points):
    cx = sum(p[0].to_float() for p in points) / len(points)
    cy = sum(p[1].to_float() for p in points) / len(points)

    def ang(p): return -math.atan2(p[1].to_float() - cy, p[0].to_float() - cx)

    ordered = sorted(points, key=ang)
    lt = find_left_top_vertex(ordered)
    i = ordered.index(lt)
    return ordered[i:] + ordered[:i]


class Piece:
    def __init__(self, shape, flip_x, flip_y, rotation, expr_x, expr_y):
        self.shape = shape
        self.flip_x = flip_x
        self.flip_y = flip_y
        self.rotation = rotation % 360
        self.shift_x = self._parse_coord(expr_x)
        self.shift_y = self._parse_coord(expr_y)
        self.vertices = self._compute_vertices()

    def _parse_coord(self, expr: str) -> QuadraticExpr:
        s = expr.strip().strip('{}')
        a = Fraction(0)
        b = Fraction(0)
        pattern = r'([+-]?(?:\d+(?:/\d+)?|\d*\.\d+))\*?sqrt\(2\)|([+-]?)sqrt\(2\)'
        for m in re.finditer(pattern, s):
            coef = Fraction(m.group(1)) if m.group(1) else Fraction(1)
            if m.group(2) == '-': coef = -coef
            b += coef
        rem = re.sub(pattern, '', s).strip()
        if rem and rem not in ('+', '-'):
            a = Fraction(eval(rem, {'__builtins__': None}, {}))
        elif rem == '-':
            a = Fraction(-1)
        return QuadraticExpr(a, b)

    def _compute_vertices(self):
        if self.rotation not in COS_SIN_TABLE:
            raise ValueError(f"Unsupported rotation: {self.rotation}")
        cos_r, sin_r = COS_SIN_TABLE[self.rotation]
        pts = []
        for x0, y0 in RAW_VERTICES[self.shape]:
            vx, vy = QuadraticExpr(x0), QuadraticExpr(y0)
            xr = vx * cos_r - vy * sin_r
            yr = vx * sin_r + vy * cos_r
            if self.flip_x: xr = -xr
            if self.flip_y: yr = -yr
            pts.append((xr + self.shift_x, yr + self.shift_y))
        return sort_1(pts)


class TangramPuzzle:
    def __init__(self, filepath):
        self.transformations = {}
        self.pieces = []
        self._load_file(filepath)

    def _load_file(self, filepath):
        data = open(filepath, encoding='utf-8').read()
        data = re.sub(r'%.*', '', data).replace(' ', '')
        pattern = re.compile(
            r"\\PieceTangram\[[^\]]*\](?:<([^>]*)>)?\(\{([^}]*)\},\{([^}]*)\}\)\{([^}]+)\}",
            re.VERBOSE
        )
        counters = {'TangGrandTri': 0, 'TangPetTri': 0}
        for opts, xs, ys, shape in pattern.findall(data):
            fx = 'xscale=-1' in (opts or '')
            fy = 'yscale=-1' in (opts or '')
            m = re.search(r'rotate=([+-]?\d+)', opts or '')
            rot = int(m.group(1)) if m else 0
            if fx and fy:
                rot += 180;
                fx = fy = False
            rot %= 360

            if shape in ('TangGrandTri', 'TangPetTri'):
                counters[shape] += 1
            name = {
                'TangGrandTri': f"Large triangle {counters['TangGrandTri']}",
                'TangMoyTri': "Medium triangle",
                'TangPetTri': f"Small triangle {counters['TangPetTri']}",
                'TangCar': "Square",
                'TangPara': "Parallelogram"
            }[shape]

            self.transformations[name] = {'rotate': rot, 'xflip': fx}
            self.pieces.append((name, Piece(shape, fx, fy, rot, xs, ys)))

    def __str__(self):
        def format_expr(expr):
            a, b = expr.a, expr.b
            remains = []
            if a != 0:
                remains.append(simplify_fraction(a))
            if b != 0:
                if b == 1:
                    remains.append("√2")
                elif b == -1:
                    remains.append("-√2")
                else:
                    b_str = f"({simplify_fraction(b)})" if b.denominator != 1 else simplify_fraction(b)
                    remains.append(f"{b_str}√2")
            return " + ".join(remains).replace("+ (-", "- (").replace('+ -', "- ") if remains else "0"

        ordered = sorted(
            self.pieces,
            key=lambda np: (
                -sort_1(np[1].vertices)[0][1].to_float(),
                sort_1(np[1].vertices)[0][0].to_float(),
                sort_1(np[1].vertices)[1][0].to_float(),
                sort_1(np[1].vertices)[1][1].to_float()
            )
    )
        lines = []
        for name, piece in ordered:
            coords = [f"({format_expr(x)}, {format_expr(y)})" for x, y in piece.vertices]
            lines.append(f"{name[:15].ljust(15)}: [{', '.join(coords)}]")
        return "\n".join(lines)


    def draw_pieces(self, outname):
        def bounds():
            xs = [x.to_float() for _, pc in self.pieces for x, _ in pc.vertices]
            ys = [y.to_float() for _, pc in self.pieces for _, y in pc.vertices]
            return min(xs), max(xs), min(ys), max(ys)

        def grid_limit(v):
            frac = v - math.floor(v)
            if frac == 0:
                return math.floor(v) + 0.5
            return math.floor(v) + (1.0 if frac <= 0.5 else 1.5)

        xmin, xmax, ymin, ymax = bounds()
        xmin_g, xmax_g = -grid_limit(-xmin), grid_limit(xmax)
        ymin_g, ymax_g = -grid_limit(-ymin), grid_limit(ymax)

        def texify(e: QuadraticExpr):
            s = str(e).replace('√2', 'sqrt(2)').replace(' ', '')
            s = re.sub(r'(?<=\d)(?=sqrt\(2\))', '*', s)
            s = re.sub(r'(\d+)/(\\d+)(?=\\*?sqrt\\(2\\))', r'\\1/\\2', s)
            return s

        with open(outname, 'w', encoding='utf-8') as f:
            f.write("\\documentclass{standalone}\n\\usepackage{tikz}\n\\begin{document}\n\n")
            f.write("\\begin{tikzpicture}\n")
            f.write(f"\\draw[step=5mm] ({xmin_g}, {ymin_g}) grid ({xmax_g}, {ymax_g});\n")
            ordered = sorted(
                self.pieces,
                key=lambda np: (
                    -sort_1(np[1].vertices)[0][1].to_float(),
                    sort_1(np[1].vertices)[0][0].to_float(),
                    sort_1(np[1].vertices)[1][0].to_float(),
                    sort_1(np[1].vertices)[1][1].to_float()
                )
            )
            for name, piece in ordered:
                pts = " -- ".join(
                    f"({{{texify(x)}}}, {{{texify(y)}}})"
                    for x, y in piece.vertices
                )
                f.write(f"\\draw[ultra thick] {pts} -- cycle;\n")
            f.write("\\fill[red] (0,0) circle (3pt);\n")
            f.write("\\end{tikzpicture}\n\n\\end{document}\n")


#
T = TangramPuzzle('cat.tex')
T.draw_pieces('cat1.tex')
for piece in T.transformations:
    print(f'{piece:16}', T.transformations[piece], sep=': ')
print(T)

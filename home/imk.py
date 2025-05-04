import re
import math
from fractions import Fraction


def frac(val):
    return Fraction(val)


class Point:
    def __init__(self, a=0, b=0):

        self.a = Fraction(a)
        self.b = Fraction(b)

    def __add__(self, other):
        return Point(self.a + other.a, self.b + other.b)

    def __sub__(self, other):
        return Point(self.a - other.a, self.b - other.b)

    def __mul__(self, other):

        if isinstance(other, Point):
            a = self.a * other.a + 2 * self.b * other.b
            b = self.a * other.b + self.b * other.a
            return Point(a, b)
        else:
            return Point(self.a * other, self.b * other)

    def __truediv__(self, scalar):
        return Point(self.a / scalar, self.b / scalar)

    def __str__(self):
        a, b = self.a, self.b
        parts = []
        if a != 0:
            parts.append(func(a))
        if b != 0:
            if b == 1:
                parts.append("√2")
            elif b == -1:
                parts.append("-√2")
            else:
                parts.append(f"{func(abs(b))}√2" if b > 0 else f"-{func(abs(b))}√2")
        return " + ".join(parts).replace("+ -", "- ") if parts else "0"

    def to_float(self):
        return float(self.a + self.b * math.sqrt(2))


ORGINAL = {
    'TangGrandTri': [(0, 0), (2, 0), (2, 2)],
    'TangMoyTri': [(0, 0), (1, 1), (2, 0)],
    'TangPetTri': [(0, 0), (1, 0), (1, 1)],
    'TangCar': [(0, 0), (1, 0), (1, 1), (0, 1)],
    'TangPara': [(0, 0), (1, 0), (2, 1), (1, 1)],

}

CONSTANT = {
    0: (Point(1, 0), Point(0, 0)),
    45: (Point(0, 1) / 2, Point(0, 1) / 2),
    90: (Point(0, 0), Point(1, 0)),
    135: (Point(0, -1) / 2, Point(0, 1) / 2),
    180: (Point(-1, 0), Point(0, 0)),
    225: (Point(0, -1) / 2, Point(0, -1) / 2),
    270: (Point(0, 0), Point(-1, 0)),
    315: (Point(0, 1) / 2, Point(0, -1) / 2),
}


def find(pts):
    vals = [(p[0].to_float(), p[1].to_float(), p) for p in pts]
    max_y = max(y for x, y, _ in vals)
    cands = [t for t in vals if abs(t[1] - max_y) < 1e-6]
    return min(cands, key=lambda t: t[0])[2]


def sort_func(pts):
    cx = sum(p[0].to_float() for p in pts) / len(pts)
    cy = sum(p[1].to_float() for p in pts) / len(pts)

    def angle_from_center(p):
        dx = p[0].to_float() - cx
        dy = p[1].to_float() - cy
        return -math.atan2(dy, dx)

    pts_sorted = sorted(pts, key=angle_from_center)
    lt = find(pts_sorted)
    i = pts_sorted.index(lt)
    return pts_sorted[i:] + pts_sorted[:i]


class Piece:
    def __init__(self, kind, xflip, yflip, rotate, x_move_expr, y_move_expr):
        self.kind = kind
        self.xflip = xflip
        self.yflip = yflip
        self.rotate = rotate % 360
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
                num = Fraction(m.group(1))
            else:
                num = Fraction(1)
                if m.group(2) == '-':
                    num = -num
            b += num
        e_no = re.sub(pattern, '', e)
        if e_no.strip() not in ('', '+', '-'):
            a = Fraction(eval(e_no, {'__builtins__': None}, {}))
        elif e_no.strip() == '-':
            a = Fraction(-1)

        return Point(a, b)

    def _compute_vertices(self):
        angle = self.rotate
        cos_e, sin_e = CONSTANT[angle]
        res = []
        for x0, y0 in ORGINAL[self.kind]:

            vx = Point(x0, 0)
            vy = Point(y0, 0)

            xr = vx * cos_e - vy * sin_e
            yr = vx * sin_e + vy * cos_e
            if self.xflip:
                xr = Point(0, 0) - xr
            if self.yflip:
                yr = Point(0, 0) - yr

            res.append((xr + self.x_move, yr + self.y_move))
        return sort_func(res)

    def left_top_vertex(self):
        return find(self.vertices)


def func(frac):
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

        counts = {'TangGrandTri': 0, 'TangMoyTri': 0, 'TangPetTri': 0}
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

            shape_names = {
                'TangGrandTri': 'Large triangle',
                'TangMoyTri': 'Medium triangle',
                'TangPetTri': 'Small triangle',
                'TangCar': 'Square',
                'TangPara': 'Parallelogram'
            }
            if shape in ['TangGrandTri', 'TangPetTri']:
                counts[shape] += 1
                name = f"{shape_names[shape]} {counts[shape]}"
            else:
                name = shape_names[shape]

            self.transformations[name] = {'rotate': rotate, 'xflip': xflip}
            piece = Piece(shape, xflip, yflip, rotate, xs, ys)
            self.pieces.append((name, piece))

    def _eval_coord(self, expr):
        e = expr.strip()
        if e.startswith('{') and e.endswith('}'):
            e = e[1:-1].strip()
        e = e.replace('sqrt(2)', 'math.sqrt(2)')
        val = eval(e, {'__builtins__': None}, {'math': math})
        return float(val)

    def __str__(self):
        def format_expr(expr):
            a, b = expr.a, expr.b
            remains = []
            if a != 0:
                remains.append(func(a))
            if b != 0:
                if b == 1:
                    remains.append("√2")
                elif b == -1:
                    remains.append("-√2")
                else:
                    b_str = f"({func(b)})" if b.denominator != 1 else func(b)
                    remains.append(f"{b_str}√2")
            return " + ".join(remains).replace("+ (-", "- (").replace('+ -', "- ") if remains else "0"

        sorted_pieces = sorted(
            self.pieces,
            key=lambda np: (
                -sort_func(np[1].vertices)[0][1].to_float(),
                sort_func(np[1].vertices)[0][0].to_float(),
                sort_func(np[1].vertices)[1][1].to_float(),
                sort_func(np[1].vertices)[1][0].to_float(),
            )
        )
        self.pieces = sorted_pieces
        return "\n".join(
            f"{name[:15]:<15}: [{', '.join(f'({format_expr(vx)}, {format_expr(vy)})' for vx, vy in piece.vertices)}]"
            for name, piece in self.pieces
        )

    def draw_pieces(self, outname):
        def get_bounds():
            all_x, all_y = [], []
            for _, piece in self.pieces:
                for v in piece.vertices:
                    all_x.append(v[0].to_float())
                    all_y.append(v[1].to_float())
            return min(all_x), max(all_x), min(all_y), max(all_y)

        def grid_limit(val, step=0.5):
            base = math.floor(val)
            frac = val - base
            return base + 0.5 if frac == 0 else base + (1.0 if frac <= step else 1.5)

        sorted_pieces = sorted(
            self.pieces,
            key=lambda np: (
                -sort_func(np[1].vertices)[0][1].to_float(),
                sort_func(np[1].vertices)[0][0].to_float(),
                sort_func(np[1].vertices)[1][1].to_float(),
                sort_func(np[1].vertices)[1][0].to_float(),
            )
        )

        xmin, xmax, ymin, ymax = get_bounds()
        xmin_g = -grid_limit(-xmin)
        xmax_g = grid_limit(xmax)
        ymin_g = -grid_limit(-ymin)
        ymax_g = grid_limit(ymax)

        def texify_expr(expr):
            expr = str(expr).replace(' ', '').replace('√2', 'sqrt(2)')
            expr = re.sub(r'(?<=\d)(?=sqrt\(2\))', '*', expr)
            return expr

        with open(outname, 'w', encoding='utf-8') as f:
            header = (
                "\\documentclass{standalone}\n"
                "\\usepackage{tikz}\n"
                "\\begin{document}\n\n"
                "\\begin{tikzpicture}\n"
                f"\\draw[step=5mm] ({xmin_g}, {ymin_g}) grid ({xmax_g}, {ymax_g});\n"
            )
            f.write(header)

            for name, piece in sorted_pieces:
                pts = " -- ".join(
                    f"({{{texify_expr(x)}}}, {{{texify_expr(y)}}})"
                    for x, y in piece.vertices
                )
                f.write(f"\\draw[ultra thick] {pts} -- cycle;\n")

            footer = (
                "\\fill[red] (0,0) circle (3pt);\n"
                "\\end{tikzpicture}\n\n"
                "\\end{document}\n"
            )
            f.write(footer)

import re
import math
from fractions import Fraction
from collections import defaultdict # 用于 segment 计数

# --- QuadraticExpr Class (修正版) ---

# 辅助函数：简化分数表示 (用于 __str__)
def _simplify_fraction_str(frac: Fraction) -> str:
    if frac.denominator == 1:
        return str(frac.numerator)
    else:
        # 括号在 __str__ 中根据上下文添加
        return f"{frac.numerator}/{frac.denominator}"

class QuadraticExpr:
    # 初始化和基本运算 (+, -, *, /scalar, neg) 保持不变
    def __init__(self, coeff_a=0, coeff_b=0):
        # 使用 Fraction 保证精度
        self.a = Fraction(coeff_a)
        self.b = Fraction(coeff_b)

    def __add__(self, other):
        if not isinstance(other, QuadraticExpr):
             # Allow adding integers/floats treated as rational part
             other = QuadraticExpr(other)
        return QuadraticExpr(self.a + other.a, self.b + other.b)

    def __radd__(self, other):
         return self.__add__(other) # Handle 0 + QuadraticExpr

    def __sub__(self, other):
        if not isinstance(other, QuadraticExpr):
             other = QuadraticExpr(other)
        return QuadraticExpr(self.a - other.a, self.b - other.b)
    
    def __rsub__(self, other):
         # Handle 0 - QuadraticExpr
         return QuadraticExpr(other) - self

    def __mul__(self, other):
        if isinstance(other, QuadraticExpr):
            # (a1 + b1*sqrt2)(a2 + b2*sqrt2) = (a1a2 + 2*b1b2) + (a1b2 + b1a2)*sqrt2
            new_a = self.a * other.a + 2 * self.b * other.b
            new_b = self.a * other.b + self.b * other.a
            return QuadraticExpr(new_a, new_b)
        # 允许乘以标量 (int, float, Fraction)
        scalar = Fraction(other)
        return QuadraticExpr(self.a * scalar, self.b * scalar)

    def __rmul__(self, other):
        return self.__mul__(other) # Handle scalar * QuadraticExpr

    def __truediv__(self, scalar):
        scalar = Fraction(scalar)
        if scalar == 0:
            raise ZeroDivisionError("Division by zero")
        return QuadraticExpr(self.a / scalar, self.b / scalar)

    def __neg__(self):
        return QuadraticExpr(-self.a, -self.b)

    def to_float(self) -> float:
        # 用于近似比较或排序，注意精度问题
        return float(self.a + self.b * math.sqrt(2))

    # --- 再次修正 __str__ 方法 ---
    def __str__(self):
        a, b = self.a, self.b

        # 处理零
        if a == 0 and b == 0:
            return "0"

        parts = []
        # 处理有理数部分 a
        if a != 0:
            # 不需要括号，因为 a 只是一个数或分数
            parts.append(_simplify_fraction_str(a))

        # 处理含 sqrt(2) 的部分 b
        if b != 0:
            b_is_fraction = (b.denominator != 1)
            b_is_pm_one = (abs(b) == 1) # 检查是否为 +/- 1

            b_formatted_str = ""
            if b_is_pm_one:
                 # 系数是 +/- 1，只显示符号（如果需要）和 √2
                 b_formatted_str = "√2"
                 # 符号在后面处理
            else:
                 # 系数不是 +/- 1
                 b_simple_str = _simplify_fraction_str(b) # 获取带符号的简化表示
                 if b_is_fraction:
                      # 如果是分数，添加括号
                      b_formatted_str = f"({b_simple_str})√2"
                 else:
                      # 如果是整数，不加括号
                      b_formatted_str = f"{b_simple_str}√2"

            # 组合 a 和 b 部分
            if parts: # 如果 a 部分存在
                sign = " + " if b > 0 else " - "
                # 如果 b 是 +/- 1，需要去掉 b_formatted_str 中的隐式符号
                if b_is_pm_one:
                     term_b = "√2"
                else:
                     # 对于非 +/- 1 的情况，b_formatted_str 已经包含了符号和值
                     # 但我们需要用 sign 连接符，所以要用 abs(b) 的表示
                     abs_b = abs(b)
                     abs_b_simple_str = _simplify_fraction_str(abs_b)
                     if abs_b.denominator != 1:
                          term_b = f"({abs_b_simple_str})√2"
                     else:
                          term_b = f"{abs_b_simple_str}√2"

                parts.append(sign)
                parts.append(term_b)

            else: # 如果只有 b 部分
                 # b_formatted_str 已经包含了符号（如果非 +/- 1 且为负）
                 # 或者需要手动加负号（如果为 -1）
                 if b == -1:
                     parts.append("-√2")
                 elif b == 1:
                     parts.append("√2")
                 else:
                     # 对于其他情况，b_formatted_str 已处理好
                     parts.append(b_formatted_str)

        return "".join(parts)

    # --- 比较和哈希方法 ---
    def __eq__(self, other):
        if not isinstance(other, QuadraticExpr):
            # Allow comparison with numbers (assuming rational part only)
            return self.b == 0 and self.a == Fraction(other)
        return self.a == other.a and self.b == other.b

    def __lt__(self, other):
        # 使用浮点数比较，注意可能的精度问题！
        # 更精确的比较需要处理 a + b*sqrt(2) < c + d*sqrt(2) 的代数形式
        if not isinstance(other, QuadraticExpr):
             other = QuadraticExpr(other)
        # 添加一个小的容差来处理浮点数比较问题
        tolerance = 1e-9
        return self.to_float() < other.to_float() - tolerance

    def __le__(self, other):
        if not isinstance(other, QuadraticExpr):
             other = QuadraticExpr(other)
        tolerance = 1e-9
        return self.to_float() <= other.to_float() + tolerance
        
    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)


    def __hash__(self):
        # 基于精确的分数进行哈希
        return hash((self.a.numerator, self.a.denominator, self.b.numerator, self.b.denominator))

# --- 全局常量和辅助函数 ---
RAW_VERTICES = { # 保持不变
    'TangGrandTri': [(0,0), (2,0), (2,2)],
    'TangMoyTri':   [(0,0), (1,1), (2,0)],
    'TangPetTri':   [(0,0), (1,0), (1,1)],
    'TangCar':      [(0,0), (1,0), (1,1), (0,1)],
    'TangPara':     [(0,0), (1,0), (2,1), (1,1)],
}
SQRT2_EXPR = QuadraticExpr(0, 1)
COS_SIN_TABLE = { # 使用 QuadraticExpr 初始化
    0:   (QuadraticExpr(1), QuadraticExpr(0)),
    45:  (SQRT2_EXPR / 2, SQRT2_EXPR / 2),
    90:  (QuadraticExpr(0), QuadraticExpr(1)),
    135: (-SQRT2_EXPR / 2, SQRT2_EXPR / 2),
    180: (QuadraticExpr(-1), QuadraticExpr(0)),
    225: (-SQRT2_EXPR / 2, -SQRT2_EXPR / 2),
    270: (QuadraticExpr(0), QuadraticExpr(-1)),
    315: (SQRT2_EXPR / 2, -SQRT2_EXPR / 2),
}

# 查找最左上角顶点 (使用 QuadraticExpr 比较)
def find_left_top_vertex(points):
    if not points: return None
    # 找到最高的 y 坐标 (精确比较)
    max_y = max(p[1] for p in points)
    # 筛选出 y 坐标接近最高的点 (考虑精度)
    top_points = [p for p in points if abs(p[1].to_float() - max_y.to_float()) < 1e-9]
    # 在最高点中找到 x 坐标最小的点 (精确比较)
    return min(top_points, key=lambda p: p[0])

# 顺时针排序 (使用 QuadraticExpr, 但角度计算仍用 float)
def sort_clockwise(points):
    if len(points) < 3: return points # 点少于3个无需排序
    # 计算质心 (近似值)
    cx_f = sum(p[0].to_float() for p in points) / len(points)
    cy_f = sum(p[1].to_float() for p in points) / len(points)
    # 按角度排序 (使用 float)
    def ang(p): return -math.atan2(p[1].to_float() - cy_f, p[0].to_float() - cx_f)
    ordered = sorted(points, key=ang)
    # 找到最左上角的顶点
    lt = find_left_top_vertex(ordered) # 使用精确比较找到的顶点
    if lt is None: return ordered # Fallback
    try:
        i = ordered.index(lt) # 查找精确顶点
        return ordered[i:] + ordered[:i] # 旋转列表
    except ValueError:
         # 如果因为精度问题找不到精确匹配，回退到近似查找
         lt_f = find_left_top_vertex(ordered) # float based one might work
         float_ordered = [(p[0].to_float(), p[1].to_float(), p) for p in ordered]
         lt_entry = min((e for e in float_ordered if abs(e[1] - lt_f[1].to_float()) < 1e-7), key=lambda x:x[0])
         try:
             idx = [i for i, p in enumerate(ordered) if p == lt_entry[2]][0]
             return ordered[idx:] + ordered[:idx]
         except IndexError:
              print("Warning: Could not reliably find start vertex for sorting.")
              return ordered # Fallback


# --- Piece Class (修正版) ---
class Piece:
    def __init__(self, shape, flip_x, flip_y, rotation, expr_x, expr_y):
        self.shape = shape
        # 这些是用于计算顶点的原始变换参数
        self.raw_flip_x = flip_x
        self.raw_flip_y = flip_y
        self.raw_rotation = rotation % 360
        # 解析位移
        self.shift_x = self._parse_coord(expr_x)
        self.shift_y = self._parse_coord(expr_y)
        # 计算最终顶点
        self.vertices = self._compute_vertices()

    # --- 改进后的 _parse_coord (更安全，但可能仍需完善) ---
    def _parse_coord(self, expr: str) -> QuadraticExpr:
        s = expr.strip().strip('{}').replace(' ', '') # 清理输入
        if not s: return QuadraticExpr(0)

        a = Fraction(0) # 有理数部分系数
        b = Fraction(0) # sqrt(2) 部分系数

        # 匹配 sqrt(2) 项 (包括系数)
        # Pattern Breakdown:
        # ([+-]?)             : Optional sign before coefficient or sqrt(2)
        # (                    : Start capturing coefficient group (optional)
        #   \d+(?:/\d+)?      : Integer or fraction (e.g., 3, 1/2)
        #   |                  : OR
        #   \d*\.\d+           : Floating point number (e.g., 1.5, .5) - converted to Fraction later
        # )?                   : Coefficient is optional (for cases like sqrt(2) or -sqrt(2))
        # (\*?)                : Optional '*' between coefficient and sqrt(2)
        # sqrt\(2\)            : Literal 'sqrt(2)'
        sqrt2_pattern = r'([+-]?)(\d+(?:/\d+)?|\d*\.\d+)?(\*?)sqrt\(2\)'

        remaining_s = s
        for match in re.finditer(sqrt2_pattern, s):
            sign = match.group(1) or '+'
            coeff_str = match.group(2)
            
            if coeff_str:
                try:
                    coeff = Fraction(coeff_str) # 直接转 Fraction (处理整数、分数、小数)
                except ValueError:
                    print(f"Warning: Could not parse coefficient '{coeff_str}' as Fraction.")
                    coeff = Fraction(0)
            else:
                # No coefficient string means coefficient is 1
                coeff = Fraction(1)

            if sign == '-':
                b -= coeff
            else:
                b += coeff
            
            # 从剩余字符串中移除已匹配的部分，为解析 a 做准备
            remaining_s = remaining_s.replace(match.group(0), '', 1)

        # 解析剩余部分 (有理数 a)
        remaining_s = remaining_s.strip()
        # 移除可能由于减法残留的 '+' 号 (例如 "sqrt(2)+1" 移除 sqrt(2) 后剩 "+1")
        if remaining_s.startswith('+'):
             remaining_s = remaining_s[1:]
             
        if remaining_s:
            try:
                # 尝试直接转换为 Fraction
                a = Fraction(remaining_s)
            except ValueError:
                # 如果直接转换失败，可能需要更复杂的解析，但避免 eval
                print(f"Warning: Could not parse rational part '{remaining_s}' as Fraction.")
                # 这里可以添加更复杂的解析逻辑，但目前仅警告
                pass # a 保持 0

        return QuadraticExpr(a, b)


    def _compute_vertices(self):
        if self.raw_rotation not in COS_SIN_TABLE:
            # 应该在 _load_file 中确保 rot % 360 且为 45 的倍数
            raise ValueError(f"Unsupported rotation: {self.raw_rotation}")

        cos_r, sin_r = COS_SIN_TABLE[self.raw_rotation]
        pts = []
        for x0, y0 in RAW_VERTICES[self.shape]:
            vx, vy = QuadraticExpr(x0), QuadraticExpr(y0) # 初始顶点坐标
            # 应用旋转
            xr = vx * cos_r - vy * sin_r
            yr = vx * sin_r + vy * cos_r
            # 应用翻转 (注意：这里的 flip_x/y 是从文件直接解析的，可能不是最终归一化状态)
            if self.raw_flip_x: xr = -xr
            if self.raw_flip_y: yr = -yr
            # 应用平移
            pts.append((xr + self.shift_x, yr + self.shift_y))
        # 排序顶点
        return sort_clockwise(pts)

# --- TangramPuzzle Class (修正版) ---
class TangramPuzzle:
    def __init__(self, filepath):
        self.transformations = {} # 存储归一化的变换 {'rotate':..., 'xflip':...}
        self.pieces = []          # 存储 (name, Piece 对象)
        self._load_file(filepath)
        # 可以在这里计算所有顶点，方便后续使用
        self.all_vertices_coords = {name: piece.vertices for name, piece in self.pieces}


    def _load_file(self, filepath):
        try:
            with open(filepath, encoding='utf-8') as f:
                data = f.read()
        except FileNotFoundError:
            print(f"Error: File not found at {filepath}")
            return
        except IOError as e:
            print(f"Error reading file {filepath}: {e}")
            return
            
        # 移除注释，但保留换行符以便调试
        data_no_comments = re.sub(r'%.*', '', data)
        # 移除 EnvTangramTikz 环境之外的空行或只包含空格的行
        lines = [line for line in data_no_comments.splitlines() if line.strip()]
        data_cleaned = "\n".join(lines)


        # 正则表达式匹配 \PieceTangram 命令
        # 注意: 使用 re.DOTALL 让 . 匹配换行符，因为坐标可能跨行
        # 注意: 移除了 replace(' ', '') 以正确处理带空格的坐标表达式
        pattern = re.compile(
            r"\\PieceTangram\[[^\]]*\]"  # \PieceTangram[...]
            r"(?:<([^>]*)>)?"          # 可选的 <options> (Group 1)
            r"\s*"                      # 可选空格
            r"\(\s*\{([^}]*)\}\s*,\s*\{([^}]*)\}\s*\)" # ({x_expr}, {y_expr}) (Groups 2, 3) - 允许内部空格
            r"\s*"                      # 可选空格
            r"\{([^}]+)\}",             # {Shape} (Group 4)
            re.DOTALL # 让 . 匹配换行符
        )

        counters = {'TangGrandTri':0, 'TangPetTri':0}
        for match in pattern.finditer(data_cleaned):
            opts, xs, ys, shape = match.groups()
            opts_str = opts or ''
            opts_str_cleaned = opts_str.strip() # 清理首尾空格

            # --- 修正后的变换参数解析 (使用 Regex) ---
            # 查找 xscale = -1 (忽略空格)
            match_fx = re.search(r'xscale\s*=\s*-1', opts_str_cleaned)
            raw_fx = bool(match_fx) # 如果找到匹配项则为 True

            # 查找 yscale = -1 (忽略空格)
            match_fy = re.search(r'yscale\s*=\s*-1', opts_str_cleaned)
            raw_fy = bool(match_fy) # 如果找到匹配项则为 True

            # 查找 rotate = value (忽略空格)
            match_rot = re.search(r'rotate\s*=\s*([+-]?\d+)', opts_str_cleaned)
            raw_rot = int(match_rot.group(1)) if match_rot else 0 # 如果找到匹配项则提取值
            
            # --- 确定 Piece 顶点计算所需的变换 ---
            # 这里我们直接使用解析出的 raw_rot, raw_fx, raw_fy 来创建 Piece 对象
            # Piece._compute_vertices 会应用这些变换
            
            # --- 计算归一化的变换 (用于 self.transformations) ---
            # 这部分逻辑需要仔细推导，确保结果符合 (rotation + optional x-flip)
            # 基本思路：
            # 1. y-flip 可以通过 x-flip 和 rotation 组合实现 (yflip = xflip + rot180)
            # 2. 合并所有旋转和翻转效果到一个最终的旋转角和最终的 x-flip 状态
            
            final_rot = raw_rot
            final_xflip = raw_fx
            if raw_fy:
                 final_rot += 180
                 final_xflip = not final_xflip
            final_rot %= 360
            
            # 确保旋转是 45 的倍数 (增加稳健性)
            if final_rot % 45 != 0:
                 original_calculated_rot = final_rot
                 final_rot = round(final_rot / 45) * 45
                 final_rot %= 360 # 确保在范围内
                 print(f"警告: 形状 {shape} 计算出的旋转角度 {original_calculated_rot} 不是 45 的倍数。已近似处理为 {final_rot}。请检查输入或逻辑。")

            # --- 拼块命名 ---
            if shape in ('TangGrandTri','TangPetTri'):
                counters[shape] += 1
                name = {
                    'TangGrandTri': f"Large triangle {counters['TangGrandTri']}",
                    'TangPetTri':   f"Small triangle {counters['TangPetTri']}",
                }[shape]
            elif shape == 'TangMoyTri': name = "Medium triangle"
            elif shape == 'TangCar':    name = "Square"
            elif shape == 'TangPara':   name = "Parallelogram"
            else:
                print(f"Warning: Unknown shape '{shape}' encountered.")
                name = "Unknown Piece"

            # --- 存储结果 ---
            # 存储归一化变换结果
            self.transformations[name] = {'rotate': final_rot, 'xflip': final_xflip}
            # 创建 Piece 对象 (使用原始解析参数计算顶点)
            try:
                 piece_obj = Piece(shape, raw_fx, raw_fy, raw_rot, xs, ys)
                 self.pieces.append((name, piece_obj))
            except Exception as e:
                 print(f"Error creating piece '{name}' from file: {e}")
                 print(f"  Shape: {shape}, Opts: '{opts_str}', X: '{xs}', Y: '{ys}'")


    # --- 修正后的 __str__ 方法 ---
    def __str__(self):
        if not self.pieces:
             return "TangramPuzzle is empty."
             
        # 排序 pieces 列表
        try:
             # 使用精确比较找到的最左上角顶点进行排序
             ordered_pieces = sorted(
                 self.pieces,
                 key=lambda np: (
                     -find_left_top_vertex(np[1].vertices)[1], # 按 y 降序 (top first)
                      find_left_top_vertex(np[1].vertices)[0]  # 按 x 升序 (left first)
                 )
             )
        except Exception as e:
             print(f"Warning: Error during piece sorting for __str__: {e}. Using original order.")
             ordered_pieces = self.pieces

        lines = []
        for name, piece in ordered_pieces:
            # 使用修正后的 QuadraticExpr.__str__ 进行格式化
            coords_str = [f"({str(x)}, {str(y)})" for x, y in piece.vertices]
            # 确保名称占用固定宽度
            lines.append(f"{name[:15].ljust(15)}: [{', '.join(coords_str)}]")
            
        return "\n".join(lines)

    # --- 修正后的 draw_pieces ---
    def draw_pieces(self, outname):
         if not self.pieces:
              print("Cannot draw pieces: No pieces loaded.")
              return
              
         # 获取所有顶点，用于计算边界
         all_coords_flat = [coord for _, piece in self.pieces for coord in piece.vertices]
         if not all_coords_flat:
             print("Cannot draw pieces: No vertices found.")
             return

         xs_f = [x.to_float() for x, y in all_coords_flat]
         ys_f = [y.to_float() for x, y in all_coords_flat]
         min_x_f, max_x_f, min_y_f, max_y_f = min(xs_f), max(xs_f), min(ys_f), max(ys_f)

         # 使用 _calculate_grid_bounds (与 draw_outline 统一)
         xmin_g, ymin_g, xmax_g, ymax_g = self._calculate_grid_bounds(
             QuadraticExpr(min_x_f), QuadraticExpr(max_x_f),
             QuadraticExpr(min_y_f), QuadraticExpr(max_y_f)
         )

         # --- 修正后的 texify ---
         def texify(qe: QuadraticExpr) -> str:
             # 假设 QuadraticExpr.__str__ 使用 √2
             s = str(qe).replace('√2', 'sqrt(2)')
             # 添加 '*' 在 数字/括号 和 sqrt(2) 之间
             s = re.sub(r'(\d|\))sqrt\(2\)', r'\1*sqrt(2)', s)
             # 处理分数括号: (num/den) -> {num/den} in TikZ coords
             # This might be tricky; let's assume str(qe) gives correct form first
             # Ensure no extra spaces are within the coordinate expression
             s = s.replace(' ', '') 
             # For TikZ, fractions like a/b might need {}
             # s = re.sub(r'(\d+/\d+)', r'{\1}', s) # This might overcomplicate... test first.
             return s

         # 排序用于绘制 (与 __str__ 逻辑一致)
         try:
             ordered_pieces_draw = sorted(
                  self.pieces,
                  key=lambda np: (
                     -find_left_top_vertex(np[1].vertices)[1], # Top first
                      find_left_top_vertex(np[1].vertices)[0]  # Left first

                  )
             )
         except Exception as e:
             print(f"Warning: Error during piece sorting for draw_pieces: {e}. Using original order.")
             ordered_pieces_draw = self.pieces


         try:
             with open(outname, 'w', encoding='utf-8') as f:
                 f.write("\\documentclass{standalone}\n\\usepackage{tikz}\n\\begin{document}\n")
                 f.write("\\begin{tikzpicture}\n")
                 f.write(f"\\draw[step=5mm] ({xmin_g:.1f}, {ymin_g:.1f}) grid ({xmax_g:.1f}, {ymax_g:.1f});\n")
                 
                 for name, piece in ordered_pieces_draw:
                     # 格式化顶点坐标 for TikZ
                     pts_str = " -- ".join(
                         # 使用花括号包围每个坐标表达式
                         f"({{{texify(x)}}}, {{{texify(y)}}})"
                         for x, y in piece.vertices
                     )
                     f.write(f"\\draw[ultra thick] {pts_str} -- cycle;\n") # 添加 cycle 闭合图形
                     
                 f.write("\\fill[red] (0,0) circle (3pt);\n")
                 f.write("\\end{tikzpicture}\n\\end{document}\n")
         except IOError as e:
             print(f"Error writing file {outname}: {e}")


    # --- draw_outline (结构和边界计算已修正，核心逻辑待实现) ---

    def _get_all_segments(self):
        """
        【待实现】从所有拼块收集所有 *有方向* 的线段 (p1, p2)。
        需要遍历 self.pieces, 获取 piece.vertices, 生成 (v_i, v_{i+1})。
        返回一个列表，例如: [((x1,y1), (x2,y2)), ((x2,y2), (x3,y3)), ...]
        """
        all_directed_segments = []
        for name, piece in self.pieces:
            vertices = piece.vertices
            num_vertices = len(vertices)
            if num_vertices < 2: continue # Skip pieces with too few vertices
            for i in range(num_vertices):
                p1 = vertices[i]
                p2 = vertices[(i + 1) % num_vertices] # Wrap around for the last segment
                all_directed_segments.append((p1, p2))
        print(f"Debug: Generated {len(all_directed_segments)} directed segments.") # Debug
        return all_directed_segments

    def _find_outline_segments(self, all_directed_segments):
        """
        【待实现】找出只出现一次的有方向线段。
        思路:
        1. 创建一个字典 segment_map，键是规范化的线段（如排序后的端点），值是原始有方向线段的列表。
           segment_map[tuple(sorted((p1, p2)))] = [(p1, p2), (p2, p1), ...]
        2. 遍历 all_directed_segments，填充 segment_map。
        3. 遍历 segment_map，找到那些值列表长度为 1 的项。这些就是外轮廓线段。
        4. 返回这些外轮廓线段（保持原始方向）。
        需要精确处理坐标比较（使用 QuadraticExpr.__eq__）。
        """
        # 使用 frozenset 作为 key 以便处理元组的可哈希性
        segment_pairs = defaultdict(list)
        for p1, p2 in all_directed_segments:
             # Use a hashable, order-independent key for the segment
             segment_key = frozenset([p1, p2]) 
             segment_pairs[segment_key].append((p1, p2))

        outline_segments = []
        processed_keys = set() # Avoid double counting symmetric segments

        for key, directed_segments in segment_pairs.items():
            if key in processed_keys: continue
            
            p1, p2 = next(iter(key)) # Get the two points from the key
            reverse_key = frozenset([p2, p1]) # Should be the same as key, but check explicitly

            # Find the opposing segment if it exists
            opposing_segments = segment_pairs.get(reverse_key, [])
            
            # An outline segment exists if its exact opposite does not exist
            # Or more simply: if a normalized segment appears only once (no opposite pair)
            # Count occurrences of the normalized segment (key)
            
            count = 0
            segment_directions = {} # Store counts for each direction
            
            # Count occurrences for the key (p1, p2) and (p2, p1)
            current_segments = segment_pairs.get(key, [])
            for seg_dir in current_segments:
                 segment_directions[seg_dir] = segment_directions.get(seg_dir, 0) + 1
                 count += 1
                 
            # It's an outline segment if the normalized segment appears only once
            # across all pieces.
            
            # A simpler approach might be needed: Count directed segments.
            # If segment (A, B) exists but (B, A) does not, (A, B) is an outline segment.
            
        # --- Revised simpler approach for outline finding ---
        directed_segment_set = set(all_directed_segments)
        outline_segments = []
        for p1, p2 in all_directed_segments:
             # If the reverse segment (p2, p1) is NOT present, then (p1, p2) is an outline segment
             if (p2, p1) not in directed_segment_set:
                 outline_segments.append((p1, p2))
                 
        print(f"Debug: Found {len(outline_segments)} potential outline segments.") # Debug
        # Ensure no duplicates in outline_segments if a segment was generated multiple times
        # Using a set then list conversion might be safer if duplicates are possible
        # outline_segments = list(set(outline_segments)) # Check if this changes results
        
        return outline_segments


    def _sort_and_merge_outline(self, outline_segments):
        """
        【待实现】排序外部线段，合并共线线段。
        思路:
        1. 找到最左上角的顶点 start_vertex。
        2. 构建一个映射 segment_map = {起点: 终点}。
        3. 从 start_vertex 开始，使用 segment_map 追踪路径，得到有序顶点列表 path。
        4. 合并共线顶点：
           - 遍历 path[1:-1]。
           - 对每个顶点 p_curr，检查 p_prev, p_curr, p_next 是否共线。
           - 使用叉积或其他精确方法 (基于 QuadraticExpr) 判断共线性。
           - 如果不共线，则将 p_curr 加入 merged_path。
           - 处理好路径起点和终点的连接。
        返回合并后的顶点列表。
        """
        if not outline_segments: return []

        # 1. 构建起点到终点的映射
        segment_map = {start: end for start, end in outline_segments}
        if len(segment_map) != len(outline_segments):
             # Check for duplicate start points, indicates an issue
             print("Warning: Duplicate start points found in outline segments, path tracing may fail.")
             # You might need to handle cases where multiple segments start from the same point
             # if the shape has antenna-like structures, though tangrams typically don't.

        # 2. 找到起点 (最左上角)
        all_outline_points = {p for seg in outline_segments for p in seg}
        if not all_outline_points: return []
        start_vertex = find_left_top_vertex(list(all_outline_points)) # Pass as list

        # 3. 追踪路径
        path = [start_vertex]
        current_vertex = start_vertex
        visited_in_trace = {start_vertex} # Track visited to detect loops/errors

        while True:
            next_vertex = segment_map.get(current_vertex)

            if next_vertex is None:
                print(f"Error: Outline path broken at vertex {current_vertex}.")
                return [] # Path broken

            if next_vertex == start_vertex:
                # Path closed successfully
                break

            if next_vertex in visited_in_trace:
                print(f"Error: Outline path loops back to vertex {next_vertex} unexpectedly.")
                # This might happen if outline_segments contained interior edges somehow.
                return [] # Loop detected

            path.append(next_vertex)
            visited_in_trace.add(next_vertex)
            current_vertex = next_vertex

            # Safety break
            if len(path) > len(outline_segments) + 2: # Should not need more steps than segments
                print("Error: Outline path tracing seems too long, potential issue.")
                return []
                
        print(f"Debug: Raw outline path length: {len(path)}") # Debug

        # 4. 合并共线顶点 (【需要精确实现】)
        if len(path) < 3: return path # Cannot merge if fewer than 3 points

        merged_path = [path[0]] # Start with the first point
        
        # Helper function for collinearity check (using cross-product with QuadraticExpr)
        def are_collinear(p1, p2, p3):
             # Calculate (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)
             cross_product = (p2[0] - p1[0]) * (p3[1] - p1[1]) - \
                             (p2[1] - p1[1]) * (p3[0] - p1[0])
             # Check if the cross product is zero (within tolerance if needed, but Fraction should be exact)
             # Since we use Fraction, direct comparison to 0 should work.
             return cross_product == 0 # Use precise comparison

        for i in range(1, len(path) - 1):
            p_prev = merged_path[-1]
            p_curr = path[i]
            p_next = path[i+1]
            
            # If p_prev, p_curr, p_next are NOT collinear, keep p_curr
            if not are_collinear(p_prev, p_curr, p_next):
                merged_path.append(p_curr)
                
        # Handle the wrap-around case for the last segment connecting back to the start
        # Check collinearity of the last point in merged path, the last point of raw path (which is start_vertex technically), and the point after start_vertex
        p_last_merged = merged_path[-1]
        p_start = path[0] # which is == path[-1]
        p_after_start = path[1]
        
        if not are_collinear(p_last_merged, p_start, p_after_start):
             # If the closing segment creates an angle, the last point added might
             # need to be re-evaluated, or simply means the path ends here before cycle.
             # In TikZ "cycle", the last point implicitly connects to the first.
             # So, we just need the vertices forming the corners.
             pass # The logic seems correct, merged_path contains corners.

        print(f"Debug: Merged outline path length: {len(merged_path)}") # Debug
        return merged_path

    # --- 修正后的 draw_outline ---
    def draw_outline(self, filename):
        """ 生成包含轮廓和网格的 .tex 文件 """

        # 1. 获取所有顶点坐标 (从 self.pieces)
        all_coords = [v for _, piece in self.pieces for v in piece.vertices]
        if not all_coords:
            print("No vertices found to draw outline.")
            return

        # --- 调用核心逻辑 (这些方法需要被正确实现!) ---
        all_segments = self._get_all_segments()
        outline_segments = self._find_outline_segments(all_segments)
        outline_vertices = self._sort_and_merge_outline(outline_segments)
        # --- End Core Logic Call ---

        if not outline_vertices:
             print(f"Could not determine outline vertices for {filename}")
             # 可以在此写入一个空的或提示错误的 tex 文件
             return

        # 5. 计算网格边界 (使用 QuadraticExpr)
        # 需要找到精确的 min/max，然后传递给 _calculate_grid_bounds
        if not all_coords: return # Should have been caught earlier
        
        # Find min/max using QuadraticExpr comparison
        min_x = min(c[0] for c in all_coords)
        max_x = max(c[0] for c in all_coords)
        min_y = min(c[1] for c in all_coords)
        max_y = max(c[1] for c in all_coords)
        
        xmin_g, ymin_g, xmax_g, ymax_g = self._calculate_grid_bounds(min_x, max_x, min_y, max_y)

        # --- 修正 texify for outline (与 draw_pieces 一致) ---
        def texify_outline(qe: QuadraticExpr) -> str:
            s = str(qe).replace('√2', 'sqrt(2)')
            s = re.sub(r'(\d|\))sqrt\(2\)', r'\1*sqrt(2)', s)
            s = s.replace(' ', '')
            # Ensure fractions are enclosed if needed by TikZ, e.g. {1/2}
            # Testing needed - TikZ might handle a/b directly in coordinates.
            # Let's assume for now TikZ handles it or use {} around full coord expr.
            return s

        # 6. 生成 .tex 字符串
        tex_content = "\\documentclass{standalone}\n"
        tex_content += "\\usepackage{tikz}\n"
        tex_content += "\\begin{document}\n\n"
        tex_content += "\\begin{tikzpicture}\n"
        # 网格绘制
        tex_content += f"\\draw[step=5mm] ({xmin_g:.1f}, {ymin_g:.1f}) grid ({xmax_g:.1f}, {ymax_g:.1f});\n"
        # 轮廓绘制
        tex_content += "\\draw[ultra thick]\n"
        formatted_vertices = []
        for v in outline_vertices:
            # 使用修正后的格式化，并用 {} 包裹坐标表达式
            formatted_vertices.append(f"    ({{ {texify_outline(v[0])} }}, {{ {texify_outline(v[1])} }})")

        tex_content += " --\n".join(formatted_vertices)
        tex_content += " -- cycle;\n" # 闭合路径
        # 原点红点
        tex_content += "\\fill[red] (0,0) circle (3pt);\n"
        tex_content += "\\end{tikzpicture}\n\n"
        tex_content += "\\end{document}\n"

        # 7. 写入文件
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(tex_content)
        except IOError as e:
            print(f"Error writing file {filename}: {e}")

    # --- 边界计算 (使用 QuadraticExpr 输入) ---
    def _calculate_grid_bounds(self, min_x_qe, max_x_qe, min_y_qe, max_y_qe):
        grid_step = 0.5 # 5mm
        # 使用浮点数进行边界计算，因为最终输出是 .1f 格式
        min_x = min_x_qe.to_float()
        max_x = max_x_qe.to_float()
        min_y = min_y_qe.to_float()
        max_y = max_y_qe.to_float()

        # 规则: 至少留一个单位(0.5)，严格少于两个单位(1.0) 的边距
        # Math: We need grid_min <= min_coord - grid_step  AND grid_min > min_coord - 2*grid_step
        #       We need grid_max >= max_coord + grid_step  AND grid_max < max_coord + 2*grid_step
        # Using floor/ceil seems appropriate.
        # xmin: Find largest multiple of grid_step <= min_x - grid_step
        xmin = math.floor((min_x - grid_step) / grid_step) * grid_step
        # Check if this leaves too much space (< min_x - 2*grid_step)
        if xmin < min_x - 2 * grid_step + 1e-9: # Add tolerance for float comparison
             xmin += grid_step

        # xmax: Find smallest multiple of grid_step >= max_x + grid_step
        xmax = math.ceil((max_x + grid_step) / grid_step) * grid_step
        # Check if this leaves too much space (> max_x + 2*grid_step)
        if xmax > max_x + 2 * grid_step - 1e-9: # Add tolerance
             xmax -= grid_step

        # Repeat for y
        ymin = math.floor((min_y - grid_step) / grid_step) * grid_step
        if ymin < min_y - 2 * grid_step + 1e-9:
             ymin += grid_step
        ymax = math.ceil((max_y + grid_step) / grid_step) * grid_step
        if ymax > max_y + 2 * grid_step - 1e-9:
             ymax -= grid_step

        # Fallback / Sanity check: ensure range is positive
        if xmax <= xmin: xmax = xmin + grid_step
        if ymax <= ymin: ymax = ymin + grid_step

        #print(f"Debug Bounds: Input min/max x=({min_x:.3f}, {max_x:.3f}), y=({min_y:.3f}, {max_y:.3f})")
        #print(f"Debug Bounds: Grid x=({xmin:.1f}, {xmax:.1f}), y=({ymin:.1f}, {ymax:.1f})")
        return xmin, ymin, xmax, ymax


# --- Bonus Task Placeholder ---
def solve_tangram_puzzle(outline_filename):
    """
    【待实现 - 附加题】
    接收轮廓文件名，返回解出的 TangramPuzzle 对象。
    需要实现：
    1. 解析 outline_filename 中的轮廓顶点。
    2. 实现搜索算法（如回溯法）来寻找拼块的放置方案。
    3. 验证方案（无重叠、匹配轮廓）。
    4. 根据找到的方案构建并返回 TangramPuzzle 对象。
    """
    print(f"Function 'solve_tangram_puzzle' for {outline_filename} is not implemented.")
    # 返回一个空的或示例 Puzzle 对象，以便代码能运行但不解决问题
    # return TangramPuzzle(...) # Requires creating a puzzle from found solution
    return None # Placeholder

# --- 示例用法 (取消注释以测试) ---
# if __name__ == '__main__':
#     try:
#         # --- 测试文件加载和 __str__ ---
#         print("--- Testing cat.tex ---")
#         cat_puzzle = TangramPuzzle('cat.tex')
#         print("Transformations:")
#         for name, trans in cat_puzzle.transformations.items():
#              print(f"  {name:16}: {trans}")
#         print("\nPiece Coordinates (__str__):")
#         print(cat_puzzle)
#
#         # --- 测试 draw_pieces ---
#         print("\nGenerating cat_pieces_test.tex...")
#         cat_puzzle.draw_pieces('cat_pieces_test.tex')
#         print("Done.")
#
#         # --- 测试 draw_outline (主要测试结构和边界) ---
#         print("\nGenerating cat_outline_test.tex (outline logic needs implementation)...")
#         cat_puzzle.draw_outline('cat_outline_test.tex')
#         print("Done.")
#
#         # --- 可以添加 goose.tex 和 kangaroo.tex 的测试 ---
#         # print("\n--- Testing goose.tex ---")
#         # goose_puzzle = TangramPuzzle('goose.tex')
#         # print(goose_puzzle)
#         # goose_puzzle.draw_pieces('goose_pieces_test.tex')
#         # goose_puzzle.draw_outline('goose_outline_test.tex')
#
#     except Exception as e:
#         print(f"\nAn error occurred during testing: {e}")
#         import traceback
#         traceback.print_exc()

"""Draws a nested-box architecture diagram: Main contains Sensors, Brain,
and Actuators; each folder becomes a nested box; leaf files show their
public functions. Data-flow arrows are drawn only between the three
top-level entities, since deeper levels represent containment, not
data movement."""

import ast
from pathlib import Path

import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT_ENTITIES = ["sensors", "brain", "actuators"]

# Paler, softer base hues -- fill opacity is layered on top of these (see depth_alpha)
PALETTE = {
    "sensors": "#a9c9e8",
    "brain": "#eab9a8",
    "actuators": "#a7d9bc",
}
NEUTRAL_BORDER = "#aaaaaa"
TEXT_COLOR = "#222222"
FUNC_COLOR = "#444444"
PADDING = 0.014
TITLE_H = 0.045
FUNC_LINE_H = 0.02
FUNC_TOP_PAD = 0.01
CHILD_GAP = 0.016

def extract_public_functions(file_path: Path) -> list[str]:
    """Returns top-level function names in a file, skipping private (_x) helpers."""
    tree = ast.parse(file_path.read_text(encoding="utf-8"), filename=str(file_path))
    return [
        node.name for node in tree.body
        if isinstance(node, ast.FunctionDef) and not node.name.startswith("_")
    ]


def build_dir_node(dir_path: Path) -> dict:
    """Recursively builds a tree: each dir/file becomes {functions, children}."""
    node = {"functions": [], "children": {}}
    init_file = dir_path / "__init__.py"
    if init_file.exists():
        node["functions"] = extract_public_functions(init_file)

    for entry in sorted(dir_path.iterdir()):
        if entry.name in {"__pycache__", "__init__.py"}:
            continue
        if entry.is_dir():
            child = build_dir_node(entry)
            if child["functions"] or child["children"]:
                node["children"][entry.name] = child
        elif entry.suffix == ".py":
            funcs = extract_public_functions(entry)
            if funcs:
                node["children"][entry.stem] = {"functions": funcs, "children": {}}

    return node


def build_tree(root_dir: str) -> dict:
    root = Path(root_dir)
    return {name: build_dir_node(root / name) for name in ROOT_ENTITIES if (root / name).exists()}


def compute_height(node: dict) -> float:
    """Bottom-up pass: computes and caches the natural (shrink-to-fit) height of a node."""
    h = TITLE_H
    if node["functions"]:
        h += FUNC_TOP_PAD + FUNC_LINE_H * len(node["functions"])
    if node["children"]:
        child_heights = [compute_height(child) for child in node["children"].values()]
        h += PADDING * 2 + max(child_heights)
    else:
        h += PADDING
    node["height"] = h
    return h


def depth_alpha(depth: int) -> float:
    """Fill opacity grows with depth, so nested boxes visibly layer on top of parents."""
    return min((depth + 3) * 0.1, 0.95)


def hex_to_rgb01(hex_color: str) -> tuple:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i + 2], 16) / 255 for i in (0, 2, 4))


def darken(hex_color: str, factor: float) -> str:
    """Blends a hex color toward black by `factor` (0 = no change, 1 = black)."""
    r, g, b = (int(c * 255) for c in hex_to_rgb01(hex_color))
    r, g, b = (int(c * (1 - factor)) for c in (r, g, b))
    return f"#{r:02x}{g:02x}{b:02x}"


def layout_node(ax, node: dict, x: float, top: float, w: float,
                 title: str, border_color: str, depth: int) -> tuple:
    """Draws one box (shrink-to-fit height) and recursively its children.
    `top` is the y-coordinate of the box's TOP edge; the box grows downward."""
    h = node["height"]
    y = top - h

    face_rgba = (*hex_to_rgb01(border_color), depth_alpha(depth))
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.001,rounding_size=0.008",
        linewidth=1.3, edgecolor=border_color, facecolor=face_rgba,
    )
    ax.add_patch(box)

    title_color = darken(border_color, 0.35)
    ax.text(x + 0.012, top - 0.02, title.capitalize(), fontsize=max(11 - depth, 8),
             fontweight="bold", color=title_color, va="top", ha="left")

    cursor_y = top - TITLE_H
    for func in node["functions"]:
        ax.text(x + 0.02, cursor_y, f"· {func}()", fontsize=7.5, color=FUNC_COLOR,
                 va="top", ha="left", family="monospace")
        cursor_y -= FUNC_LINE_H
    if node["functions"]:
        cursor_y -= FUNC_TOP_PAD

    children = node["children"]
    if children:
        children_top = cursor_y - PADDING
        n = len(children)
        child_w = (w - 2 * PADDING - CHILD_GAP * (n - 1)) / n
        cx = x + PADDING
        for name, child in children.items():
            layout_node(ax, child, cx, children_top, child_w, name, border_color, depth + 1)
            cx += child_w + CHILD_GAP

    return (x, y, w, h)


def draw_arrow(ax, start_box: tuple, end_box: tuple, label: str, color: str = "#555555"):
    """Draws a curved labeled arrow from the right of start_box to the left of end_box."""
    sx, sy, sw, sh = start_box
    ex, ey, ew, eh = end_box
    start_point = (sx + sw, sy + sh * 0.5)
    end_point = (ex, ey + eh * 0.5)

    ax.annotate(
        "", xy=end_point, xytext=start_point,
        arrowprops=dict(arrowstyle="-|>", color=color, lw=1.6,
                         connectionstyle="arc3,rad=-0.25"),
    )
    mid = ((start_point[0] + end_point[0]) / 2, (start_point[1] + end_point[1]) / 2 + 0.03)
    ax.text(mid[0], mid[1], label, fontsize=8, color=color, ha="center",
             style="italic")


def get_return_annotation(file_path: Path, func_name: str) -> str:
    """Reads a function's return type annotation from source, e.g. 'str'."""
    if not file_path.exists():
        return "data"
    tree = ast.parse(file_path.read_text(encoding="utf-8"), filename=str(file_path))
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == func_name and node.returns:
            return ast.unparse(node.returns)
    return "data"


def draw_diagram(root_dir: str, output_path: str = "visualisation/architecture.png"):
    root = Path(root_dir)
    tree = build_tree(root_dir)
    for node in tree.values():
        compute_height(node)

    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Helvetica", "Arial", "DejaVu Sans"]

    fig, ax = plt.subplots(figsize=(13, 8))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    # Outer "Main" container -- always full-size, it's just the frame
    main_box = FancyBboxPatch(
        (0.02, 0.05), 0.96, 0.88,
        boxstyle="round,pad=0.002,rounding_size=0.012",
        linewidth=1.6, edgecolor=NEUTRAL_BORDER, facecolor="#fbfbfb",
    )
    ax.add_patch(main_box)
    ax.text(0.03, 0.90, "Main", fontsize=14, fontweight="bold", color=TEXT_COLOR)

    # Three root entities side by side inside Main, each shrink-to-fit
    entity_boxes = {}
    inner_x, inner_top, inner_w = 0.05, 0.84, 0.90
    n = len(tree)
    gap = 0.02
    box_w = (inner_w - gap * (n - 1)) / n
    cx = inner_x
    for name in ROOT_ENTITIES:
        if name not in tree:
            continue
        rect = layout_node(ax, tree[name], cx, inner_top, box_w,
                             name, PALETTE[name], depth=0)
        entity_boxes[name] = rect
        cx += box_w + gap

    # Data-flow arrows: only between top-level entities (see design note above)
    if "sensors" in entity_boxes and "brain" in entity_boxes:
        sensors_type = get_return_annotation(root / "sensors/read/__init__.py", "read")
        draw_arrow(ax, entity_boxes["sensors"], entity_boxes["brain"], sensors_type)
    if "brain" in entity_boxes and "actuators" in entity_boxes:
        brain_type = get_return_annotation(root / "brain/__init__.py", "process")
        draw_arrow(ax, entity_boxes["brain"], entity_boxes["actuators"], brain_type)

    plt.title("Datrius | Architecture", fontsize=15, fontweight="bold",
               color=TEXT_COLOR, pad=15)
    plt.tight_layout()
    plt.savefig(output_path, dpi=170, facecolor="white")
    print(f"Saved to {output_path}")
    plt.show()


if __name__ == "__main__":
    draw_diagram(".")
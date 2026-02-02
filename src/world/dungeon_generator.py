import random
from utils.layout import LayoutCell


class DungeonGenerator:
    """
    Генерирует только геометрию подземелья.
    НЕ содержит игровой логики.
    """

    def __init__(self, width=64, height=64):
        self.width = width
        self.height = height
        self.grid = [[LayoutCell.VOID for _ in range(width)] for _ in range(height)]
        self.rooms = []

    def generate(self):
        self.grid = [[LayoutCell.VOID for _ in range(self.width)] for _ in range(self.height)]
        self.rooms.clear()

        self._place_rooms()
        self._connect_all_rooms()
        self._place_exits()
        self._ensure_connectivity()

        return self.grid

    # ---------- ROOMS ----------

    def _place_rooms(self):
        attempts = 0
        while len(self.rooms) < 20 and attempts < 500:
            attempts += 1

            sizes = [(1, 1), (2, 3), (3, 2), (3, 4), (4, 3)]
            w, h = random.choice(sizes)

            x = random.randint(1, self.width - w - 1)
            y = random.randint(1, self.height - h - 1)

            if self._can_place_room(x, y, w, h, 3):
                self._create_room(x, y, w, h)
                self.rooms.append((x + w // 2, y + h // 2))

    def _can_place_room(self, x, y, w, h, spacing):
        for dy in range(-spacing, h + spacing):
            for dx in range(-spacing, w + spacing):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if self.grid[ny][nx] != LayoutCell.VOID:
                        return False
        return True

    def _create_room(self, x, y, w, h):
        for dy in range(h):
            for dx in range(w):
                self.grid[y + dy][x + dx] = LayoutCell.FLOOR

    # ---------- CORRIDORS ----------

    def _connect_all_rooms(self):
        if len(self.rooms) < 2:
            return

        connected = {0}
        unconnected = set(range(1, len(self.rooms)))

        while unconnected:
            min_dist = float("inf")
            best = None

            for c in connected:
                for u in unconnected:
                    dist = self._manhattan(self.rooms[c], self.rooms[u])
                    if dist < min_dist:
                        min_dist = dist
                        best = (c, u)

            if best:
                self._create_corridor(self.rooms[best[0]], self.rooms[best[1]])
                connected.add(best[1])
                unconnected.remove(best[1])

    def _manhattan(self, p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def _create_corridor(self, start, end):
        x1, y1 = start
        x2, y2 = end

        if random.choice([True, False]):
            self._draw_line(x1, y1, x2, y1)
            self._draw_line(x2, y1, x2, y2)
        else:
            self._draw_line(x1, y1, x1, y2)
            self._draw_line(x1, y2, x2, y2)

    def _draw_line(self, x1, y1, x2, y2):
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                if self.grid[y][x1] == LayoutCell.VOID:
                    self.grid[y][x1] = LayoutCell.FLOOR
        else:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                if self.grid[y1][x] == LayoutCell.VOID:
                    self.grid[y1][x] = LayoutCell.FLOOR

    # ---------- EXITS ----------

    def _place_exits(self):
        floor_cells = [
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if self.grid[y][x] == LayoutCell.FLOOR
        ]

        for x, y in random.sample(floor_cells, min(3, len(floor_cells))):
            self.grid[y][x] = LayoutCell.EXIT

    # ---------- CONNECTIVITY ----------

    def _ensure_connectivity(self):
        start = self.get_valid_start_position()

        exits = [
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if self.grid[y][x] == LayoutCell.EXIT
        ]

        for e in exits:
            if not self._is_reachable(start, e):
                self._create_path(start, e)

    def get_valid_start_position(self):
        cx, cy = self.width // 2, self.height // 2

        for r in range(10):
            for dx in range(-r, r + 1):
                for dy in range(-r, r + 1):
                    x, y = cx + dx, cy + dy
                    if (
                        0 <= x < self.width
                        and 0 <= y < self.height
                        and self.grid[y][x] == LayoutCell.FLOOR
                    ):
                        return x, y

        self.grid[cy][cx] = LayoutCell.FLOOR
        return cx, cy

    def _is_reachable(self, start, end):
        visited = set()
        queue = [start]

        while queue:
            x, y = queue.pop(0)
            if (x, y) == end:
                return True

            if (x, y) in visited:
                continue
            visited.add((x, y))

            for dx, dy in [(0,1),(0,-1),(1,0),(-1,0)]:
                nx, ny = x + dx, y + dy
                if (
                    0 <= nx < self.width
                    and 0 <= ny < self.height
                    and self.grid[ny][nx] != LayoutCell.VOID
                    and (nx, ny) not in visited
                ):
                    queue.append((nx, ny))

        return False

    def _create_path(self, start, end):
        x, y = start
        ex, ey = end

        while x != ex:
            x += 1 if x < ex else -1
            self.grid[y][x] = LayoutCell.FLOOR

        while y != ey:
            y += 1 if y < ey else -1
            self.grid[y][x] = LayoutCell.FLOOR

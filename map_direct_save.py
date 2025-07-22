import pandas as pd
import matplotlib.pyplot as plt
from collections import deque
import itertools

def bfs_shortest_length(start, end, min_x, max_x, min_y, max_y, block_set):
    queue = deque([(start, 0)])
    visited = set([start])
    dx = [1, -1, 0, 0]
    dy = [0, 0, 1, -1]
    while queue:
        (x, y), dist = queue.popleft()
        if (x, y) == end:
            return dist
        for d in range(4):
            nx, ny = x + dx[d], y + dy[d]
            if (min_x <= nx <= max_x and min_y <= ny <= max_y and
                (nx, ny) not in block_set and (nx, ny) not in visited):
                queue.append(((nx, ny), dist + 1))
                visited.add((nx, ny))
    return float('inf')

def main():
    try:
        plt.rcParams['font.family'] = 'AppleGothic'  # Mac에서 한글 O
        plt.rcParams['axes.unicode_minus'] = False   # 마이너스 깨짐 방지

        df = pd.read_csv('temp.csv')
        blocks = set((row['x'], row['y']) for _, row in df.iterrows() if row['ConstructionSite'] == 1)
        struct_dict = {(row['x'], row['y']): str(row['struct']).strip() for _, row in df.iterrows()}

        # min_x, min_y를 1로 고정
        min_x, max_x = 1, df['x'].max()
        min_y, max_y = 1, df['y'].max()

        target_types = {'MyHome', 'Apartment', 'Building', 'BandalgomCoffee'}
        structures = [(xy, struct) for xy, struct in struct_dict.items() if struct in target_types and xy not in blocks]
        print('count:', len(structures))

        myhome_count = sum(1 for _, struct in structures if struct == 'MyHome')
        if myhome_count == 1:
            structures.sort(key=lambda x: 0 if x[1] == 'MyHome' else 1)
        else:
            raise ValueError('error: data file error')

        positions = [xy for xy, _ in structures]
        labels = [struct for _, struct in structures]
        n = len(positions)

        dist_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                dist_matrix[i][j] = bfs_shortest_length(
                    positions[i], positions[j], min_x, max_x, min_y, max_y, blocks
                )

        best_len = float('inf')
        best_path = None
        idxs = range(n)
        for perm in itertools.permutations(idxs[1:]):
            order = [0] + list(perm)
            path_len = sum(dist_matrix[order[i]][order[i+1]] for i in range(n - 1))
            if path_len < best_len:
                best_len = path_len
                best_path = order

        if best_len == float('inf'):
            raise ValueError('error: data file error')
        
        print('최소 총 거리:', best_len)
        print('방문 순서:', [labels[i] for i in best_path])
        print('구조물 좌표:', [positions[i] for i in best_path])
        
        # 실제 경로 구간별 BFS로 합쳐서 저장
        full_path = []
        for i in range(n - 1):
            seg = []
            queue = deque([(positions[best_path[i]], [positions[best_path[i]]])])
            visited = set([positions[best_path[i]]])
            found = False
            while queue and not found:
                (x, y), path = queue.popleft()
                if (x, y) == positions[best_path[i + 1]]:
                    seg = path
                    found = True
                    break
                for d in range(4):
                    nx, ny = x + [1, -1, 0, 0][d], y + [0, 0, 1, -1][d]
                    if (min_x <= nx <= max_x and min_y <= ny <= max_y and
                        (nx, ny) not in blocks and (nx, ny) not in visited):
                        queue.append(((nx, ny), path + [(nx, ny)]))
                        visited.add((nx, ny))
            if i > 0 and seg:
                seg = seg[1:]
            full_path.extend(seg)

        path_df = pd.DataFrame({'x': [p[0] for p in full_path], 'y': [p[1] for p in full_path]})
        path_df.to_csv('home_to_cafe_tsp.csv', index=False)

        plt.figure(figsize=(7, 7))
        for x in range(min_x, max_x + 1):
            plt.axvline(x - 0.5, color='lightgray', linewidth=0.8, zorder=0)
        for y in range(min_y, max_y + 1):
            plt.axhline(y - 0.5, color='lightgray', linewidth=0.8, zorder=0)
        for (x, y) in blocks:
            plt.gca().add_patch(plt.Rectangle((x - 0.5, y - 0.5), 1, 1, color='gray', zorder=3, alpha=0.8))
        for i, ((x, y), struct) in enumerate(structures):
            if struct in ('Apartment', 'Building'):
                plt.scatter(x, y, s=400, color='#A0522D', marker='o', edgecolor='black', zorder=2)
            elif struct == 'BandalgomCoffee':
                plt.gca().add_patch(plt.Rectangle((x - 0.4, y - 0.4), 0.8, 0.8, color='green', zorder=2, alpha=0.8))
            elif struct == 'MyHome' or struct == 'Start':
                triangle = plt.Polygon([
                    (x, y + 0.45), (x - 0.4, y - 0.35), (x + 0.4, y - 0.35)
                ], closed=True, color='green', zorder=2, alpha=0.8)
                plt.gca().add_patch(triangle)
        if full_path:
            path_x, path_y = zip(*full_path)
            plt.plot(path_x, path_y, color='red', linewidth=3, zorder=5, label='최적 경로')
        plt.xlim(min_x - 0.5, max_x + 0.5)
        plt.ylim(max_y + 0.5, min_y - 0.5)
        plt.xticks(range(min_x, max_x + 1))
        plt.yticks(range(min_y, max_y + 1))
        plt.gca().set_aspect('equal')
        plt.title('모든 구조물 방문 최적 경로', fontsize=15)
        plt.tight_layout()
        plt.savefig('map_final.png', dpi=150)
        plt.close()
        print('모든 구조물 방문 경로와 이미지 저장 완료!')

    except ValueError as e:
        print(e)

if __name__ == '__main__':
    main()

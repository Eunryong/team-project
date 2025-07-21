import pandas as pd
import matplotlib.pyplot as plt
from collections import deque

def bfs_shortest_path(start, end, min_x, max_x, min_y, max_y, block_set):
    queue = deque([(start, [start])])
    visited = set([start])
    dx = [1, -1, 0, 0]
    dy = [0, 0, 1, -1]
    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == end:
            return path
        for d in range(4):
            nx, ny = x + dx[d], y + dy[d]
            # 지도 범위 내 & 건설현장(X) & 미방문
            if (min_x <= nx <= max_x and min_y <= ny <= max_y and
                (nx, ny) not in block_set and (nx, ny) not in visited):
                queue.append(((nx, ny), path + [(nx, ny)]))
                visited.add((nx, ny))
    return None


def main():
    df = pd.read_csv('area1_data.csv')
    blocks = set((row['x'], row['y']) for _, row in df.iterrows() if row['ConstructionSite'] == 1)
    struct_dict = {(row['x'], row['y']): str(row['struct']).strip() for _, row in df.iterrows()}

    min_x, max_x = df['x'].min(), df['x'].max()
    min_y, max_y = df['y'].min(), df['y'].max()

    start = (1, 1)
    cafe_points = [k for k, v in struct_dict.items() if v == 'BandalgomCoffee']
    end = cafe_points[0]

    if start in blocks:
        print('시작점이 건설 현장입니다. 출발할 수 없습니다.')
        return

    path = bfs_shortest_path(start, end, min_x, max_x, min_y, max_y, blocks)
    if not path:
        print('경로를 찾을 수 없습니다.')
        return

    # 경로 저장
    path_df = pd.DataFrame({'x': [p[0] for p in path], 'y': [p[1] for p in path]})
    path_df.to_csv('home_to_cafe.csv', index=False)

    # 시각화
    plt.rcParams['font.family'] = 'AppleGothic'
    plt.rcParams['axes.unicode_minus'] = False

    plt.figure(figsize=(7, 7))
    min_x, max_x = df['x'].min(), df['x'].max()
    min_y, max_y = df['y'].min(), df['y'].max()
    for x in range(min_x, max_x + 1):
        plt.axvline(x - 0.5, color='lightgray', linewidth=0.8, zorder=0)
    for y in range(min_y, max_y + 1):
        plt.axhline(y - 0.5, color='lightgray', linewidth=0.8, zorder=0)
    for (x, y) in blocks:
        plt.gca().add_patch(plt.Rectangle((x - 0.5, y - 0.5), 1, 1, color='gray', zorder=3, alpha=0.8))
    for _, row in df.iterrows():
        x, y = row['x'], row['y']
        struct = str(row['struct']).strip()
        if (x, y) in blocks:
            continue
        if struct in ('Apartment', 'Building'):
            plt.scatter(x, y, s=400, color='#A0522D', marker='o', edgecolor='black', zorder=2)
        elif struct == 'BandalgomCoffee':
            plt.gca().add_patch(plt.Rectangle((x - 0.4, y - 0.4), 0.8, 0.8, color='green', zorder=2, alpha=0.8))
        elif struct == 'MyHome':
            triangle = plt.Polygon([
                (x, y + 0.45), (x - 0.4, y - 0.35), (x + 0.4, y - 0.35)
            ], closed=True, color='green', zorder=2, alpha=0.8)
            plt.gca().add_patch(triangle)

    path_x, path_y = zip(*path)
    plt.plot(path_x, path_y, color='red', linewidth=3, zorder=5, label='최단 경로')
    plt.xlim(min_x - 0.5, max_x + 0.5)
    plt.ylim(max_y + 0.5, min_y - 0.5)
    plt.xticks(range(min_x, max_x + 1))
    plt.yticks(range(min_y, max_y + 1))
    plt.gca().set_aspect('equal')
    plt.title('최단 경로 시각화', fontsize=15)
    plt.tight_layout()
    plt.savefig('map_final.png', dpi=150)
    plt.close()
    print('경로와 이미지 저장 완료!')

if __name__ == '__main__':
    main()

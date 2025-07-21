import pandas as pd
import matplotlib.pyplot as plt

def draw_map():
    # 데이터 불러오기
    merged = pd.read_csv('area1_data.csv')   # area1만 또는 전체 병합본 사용

    # 좌표 범위 계산
    min_x, max_x = 1, merged['x'].max()
    min_y, max_y = 1, merged['y'].max()

    plt.rcParams['font.family'] = 'AppleGothic'  # Mac에서 한글 폰트 지정
    plt.rcParams['axes.unicode_minus'] = False   # 마이너스(-) 깨짐 방지

    plt.figure(figsize=(max_x, max_y))  # 사이즈 자동 조정

    # 1. 그리드 그리기
    for x in range(min_x, max_x + 1):
        plt.axvline(x - 0.5, color='lightgray', linewidth=0.8, zorder=0)
    for y in range(min_y, max_y + 1):
        plt.axhline(y - 0.5, color='lightgray', linewidth=0.8, zorder=0)

    # 2. 구조물/건설 현장 표시
    for _, row in merged.iterrows():
        x, y = row['x'], row['y']
        construction = row.get('ConstructionSite', 0)
        struct = str(row.get('struct', '')).strip()

        # 건설 현장이 우선
        if construction == 1:
            plt.gca().add_patch(plt.Rectangle((x - 0.5, y - 0.5), 1, 1, color='gray', zorder=3, alpha=0.8))
        elif struct in ('Apartment', 'Building'):
            plt.scatter(x, y, s=400, color='#A0522D', marker='o', edgecolor='black', zorder=2, label=struct)
        elif struct == 'BandalgomCoffee':
            plt.gca().add_patch(plt.Rectangle((x - 0.4, y - 0.4), 0.8, 0.8, color='green', zorder=2, alpha=0.8))
        elif struct == 'MyHome':
            # 삼각형 (녹색)
            triangle = plt.Polygon([
                (x, y + 0.45), (x - 0.4, y - 0.35), (x + 0.4, y - 0.35)
            ], closed=True, color='green', zorder=2, alpha=0.8)
            plt.gca().add_patch(triangle)

    # 3. 좌표축 설정: (1,1)이 좌상단이 되도록 y축 뒤집기
    plt.xlim(min_x - 0.5, max_x + 0.5)
    plt.ylim(max_y + 0.5, min_y - 0.5)
    plt.xticks(range(min_x, max_x + 1))
    plt.yticks(range(min_y, max_y + 1))

    plt.gca().set_aspect('equal')

    # 4. 범례 (보너스)
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Apartment/Building', markerfacecolor='#A0522D', markeredgecolor='black', markersize=15),
        Line2D([0], [0], marker='s', color='w', label='BandalgomCoffee', markerfacecolor='green', markersize=15),
        Line2D([0], [0], marker=(3,0,0), color='w', label='MyHome', markerfacecolor='green', markersize=15),
        Line2D([0], [0], marker='s', color='gray', label='ConstructionSite', markerfacecolor='gray', markersize=15)
    ]
    plt.legend(handles=legend_elements, loc='upper right', fontsize=11, frameon=True)

    plt.title('지역 지도 시각화', fontsize=15)
    plt.tight_layout()
    plt.savefig('map.png', dpi=150)
    plt.close()
    
if __name__ == '__main__':
    draw_map()
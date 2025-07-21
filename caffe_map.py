import pandas as pd

def read_merge_csv():
    area_map = pd.read_csv('area_map.csv')
    area_struct = pd.read_csv('area_struct.csv')
    area_category = pd.read_csv('area_category.csv')

    area_category.columns = area_category.columns.str.strip()

    merged_struct = area_struct.merge(area_category, on='category', how='left')

    merged = area_map.merge(merged_struct, on=['x', 'y'], how='left')

    merged_sorted = merged.sort_values(by='area')

    area1_data = merged_sorted[merged_sorted['area'] == 1]

    area1_data.to_csv('area1_data.csv', index=False)

    # (보너스) 구조물 종류별 요약 통계 리포트
    print('\n[구조물 종류별 요약 통계]')
    category_describe = merged_sorted['struct'].describe()
    print(category_describe)
    category_counts = merged_sorted['struct'].value_counts()
    print(category_counts)

if __name__ == '__main__':
    read_merge_csv()
import torch
from transformers import AutoModel, AutoTokenizer
import numpy as np

# 모델 로드
tokenizer = AutoTokenizer.from_pretrained('BM-K/KoSimCSE-roberta-multitask')
model = AutoModel.from_pretrained('BM-K/KoSimCSE-roberta-multitask')

# 수학 세부 중분류 정의
categories_math_subfields = [
    "대수학",
    "해석학",
    "기하학",
    "위상수학",
    "정수론",
    "확률론",
    "통계학",
    "미분방정식",
    "선형대수학",
    "복소해석학",
    "함수해석학",
    "미분기하학",
    "대수기하학",
    "수리논리",
    "조합론",
    "수치해석학",
    "이산수학",
    "암호학"
]

# 코사인 유사도 계산 함수
def cal_score(a, b):
    if len(a.shape) == 1: a = a.unsqueeze(0)
    if len(b.shape) == 1: b = b.unsqueeze(0)

    a_norm = a / a.norm(dim=1, keepdim=True)
    b_norm = b / b.norm(dim=1, keepdim=True)
    
    return torch.mm(a_norm, b_norm.transpose(0, 1)).item()

# 클러스터링 로직 구현 (데이터 1개씩 추가하며 처리)
def cluster_items_incrementally(items, model, tokenizer, similarity_threshold=0.60, max_clusters=6): 
    clusters = []
    cluster_reps = []
    cluster_embeddings_list = []

    # 모든 아이템의 임베딩을 미리 계산
    item_embeddings_map = {}
    for item in items:
        inputs = tokenizer(item, padding=True, truncation=True, return_tensors="pt")
        with torch.no_grad():
            embeddings = model(**inputs).last_hidden_state 
        item_embeddings_map[item] = embeddings[0][0] # [CLS] 토큰 임베딩 사용

    # 첫 번째 아이템 처리
    first_item = items[0]
    first_embedding = item_embeddings_map[first_item]

    clusters.append([first_item])
    cluster_reps.append(first_embedding)
    cluster_embeddings_list.append([first_embedding])

    # 나머지 아이템들 순차 처리
    for current_item in items[1:]:
        current_embedding = item_embeddings_map[current_item] 
        
        best_sim_above_threshold = -1.0 
        idx_above_threshold = -1 

        best_sim_overall = -float('inf') 
        idx_overall_best = -1

        for cluster_idx, rep_vec in enumerate(cluster_reps):
            sim_score = cal_score(current_embedding, rep_vec) 

            if sim_score > best_sim_overall:
                best_sim_overall = sim_score
                idx_overall_best = cluster_idx

            if sim_score >= similarity_threshold and sim_score > best_sim_above_threshold:
                best_sim_above_threshold = sim_score
                idx_above_threshold = cluster_idx
                
        target_cluster_idx = -1 

        if idx_above_threshold != -1:
            target_cluster_idx = idx_above_threshold
        elif len(clusters) >= max_clusters:
            target_cluster_idx = idx_overall_best 
        else:
            target_cluster_idx = -1 

        if target_cluster_idx != -1:
            clusters[target_cluster_idx].append(current_item)
            cluster_embeddings_list[target_cluster_idx].append(current_embedding)
            
            updated_rep_vec = torch.mean(torch.stack(cluster_embeddings_list[target_cluster_idx]), dim=0)
            cluster_reps[target_cluster_idx] = updated_rep_vec
        
        else:
            clusters.append([current_item])
            cluster_reps.append(current_embedding)
            cluster_embeddings_list.append([current_embedding])
            
    return clusters

# 클러스터링 실행 및 결과 출력
# 수학 분야는 개념 간의 연관성이 매우 강하고 추상적이므로, threshold를 조절하며 최적의 값을 찾아야 합니다.
# similarity_threshold를 0.60으로, max_clusters를 6개로 설정했습니다.
clustered_groups = cluster_items_incrementally(categories_math_subfields, model, tokenizer, 
                                               similarity_threshold=0.85, max_clusters=7) 

print("--- 수학 중분류 클러스터링 결과 ---")
print(f"총 클러스터 개수: {len(clustered_groups)}개")

for i, cluster in enumerate(clustered_groups):
    print(f"\n**클러스터 {i+1}** ({len(cluster)}개 항목):")
    if cluster:
        for item in cluster:
            print(f"- {item}")
    else:
        print("- (비어있음)")
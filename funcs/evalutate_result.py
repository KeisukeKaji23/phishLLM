import json


def analyze_phishing_results(result_files, output_file):
    models_data = []

    for model_name, files in result_files.items():
        # フィッシングサイトの結果ファイルを読み込む
        with open(files["phishing"]) as file:
            phishing_data = json.load(file)

        # 正規サイトの結果ファイルを読み込む
        with open(files["legitimate"]) as file:
            legitimate_data = json.load(file)

        # フィッシングサイトの判定結果を分析
        phishing_count = len(phishing_data)
        true_positives = sum(
            1 for result in phishing_data.values() if result["isPhishing"]
        )
        false_negatives = phishing_count - true_positives

        # 正規サイトの判定結果を分析
        legitimate_count = len(legitimate_data)
        true_negatives = sum(
            1 for result in legitimate_data.values() if not result["isPhishing"]
        )
        false_positives = legitimate_count - true_negatives

        # 指標を計算
        total_count = phishing_count + legitimate_count
        accuracy = (true_positives + true_negatives) / total_count
        precision = true_positives / (true_positives + false_positives)
        recall = true_positives / (true_positives + false_negatives)
        f1_score = 2 * (precision * recall) / (precision + recall)

        models_data.append(
            {
                "model_name": model_name,
                "total_count": total_count,
                "phishing_count": phishing_count,
                "legitimate_count": legitimate_count,
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1_score": f1_score,
                "true_positives": true_positives,
                "false_positives": false_positives,
                "true_negatives": true_negatives,
                "false_negatives": false_negatives,
            }
        )

    # 結果をマークダウンファイルに出力
    with open(output_file, "w") as file:
        file.write("# フィッシングサイト判定結果の分析\n\n")

        for model_data in models_data:
            file.write(f"## モデル: {model_data['model_name']}\n\n")
            file.write("### 概要\n\n")
            file.write(f"- 総サイト数: {model_data['total_count']}\n")
            file.write(f"- フィッシングサイト数: {model_data['phishing_count']}\n")
            file.write(f"- 正規サイト数: {model_data['legitimate_count']}\n\n")
            file.write("### 指標\n\n")
            file.write(f"- Accuracy: {model_data['accuracy']:.2%}\n")
            file.write(f"- Precision: {model_data['precision']:.2%}\n")
            file.write(f"- Recall: {model_data['recall']:.2%}\n")
            file.write(f"- F1-score: {model_data['f1_score']:.2%}\n\n")
            file.write("### 混同行列\n\n")
            file.write("| | 予測: フィッシング | 予測: 正規 |\n")
            file.write("|-|-------------------|------------|\n")
            file.write(
                f"| 実際: フィッシング | {model_data['true_positives']} | {model_data['false_negatives']} |\n"
            )
            file.write(
                f"| 実際: 正規 | {model_data['false_positives']} | {model_data['true_negatives']} |\n\n"
            )


# 使用例
result_files = {
    "common person": {
        "phishing": "/home/keisukekaji/my-study/result/phishing/common_person_phishing_result.json",
        "legitimate": "/home/keisukekaji/my-study/result/benign/common_person_benign_result.json",
    },
    "common person with knowledge": {
        "phishing": "/home/keisukekaji/my-study/result/phishing/common_person_with_knowledge_phishing_result.json",
        "legitimate": "/home/keisukekaji/my-study/result/benign/common_person_with_knowledge_benign_result.json",
    },
    "expert": {
        "phishing": "/home/keisukekaji/my-study/result/phishing/expert_phishing_result.json",
        "legitimate": "/home/keisukekaji/my-study/result/benign/expert_benign_result.json",
    },
}
output_file = "analysis_results.md"

analyze_phishing_results(result_files, output_file)

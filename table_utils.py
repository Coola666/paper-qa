import json
import re


def extract_tables_from_llm(client, text):

    if client is None:
        raise ValueError("LLM client 未初始化")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": "你是论文表格分析助手"
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )

    return response.choices[0].message.content


def analyze_sota_vs_baseline(table_data):
    """
    ⭐ 自动SOTA分析 + best model detection
    """

    if not table_data:
        return "No structured data extracted."

    # group by model
    model_scores = {}

    for item in table_data:
        model = item.get("model", "unknown")
        value = item.get("value", 0)

        if model not in model_scores:
            model_scores[model] = []

        model_scores[model].append(float(value))

    # compute avg
    model_avg = {
        m: sum(v) / len(v)
        for m, v in model_scores.items()
        if len(v) > 0
    }

    if not model_avg:
        return "No valid metrics found."

    best_model = max(model_avg, key=model_avg.get)

    baseline = min(model_avg, key=model_avg.get)

    analysis = f"""
## 🏆 SOTA Analysis

### Best Model:
- {best_model} ({model_avg[best_model]:.4f})

### Baseline:
- {baseline} ({model_avg[baseline]:.4f})

### Model Ranking:
"""

    sorted_models = sorted(model_avg.items(), key=lambda x: x[1], reverse=True)

    for m, v in sorted_models:
        analysis += f"- {m}: {v:.4f}\n"

    improvement = model_avg[best_model] - model_avg[baseline]

    analysis += f"""

### 📈 Improvement:
- Absolute gain: {improvement:.4f}
- Relative gain: {(improvement / (model_avg[baseline] + 1e-6)):.2%}
"""

    return analysis
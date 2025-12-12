# LLM Evaluation Tool

This is a small Python project I made for checking LLM answers.
It gives 3 scores:
- relevance
- completeness
- hallucination

I used a small sentence-transformer model for embeddings.

To run:
python main.py --chat sample_inputs/chat.json --context sample_inputs/context.json --out report.json

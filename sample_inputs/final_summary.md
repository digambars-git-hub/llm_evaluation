This project is a small evaluation tool I made to check how well an LLM responds to a user query. The idea was to compare the model’s answer with the context information and give some basic scores like relevance, completeness, hallucination, and latency.

I created a few Python files for this:

main.py → loads the input files and runs the evaluator

evaluator.py → has the logic for scoring

utils.py → helper functions like embeddings, cosine similarity etc.

The input format is simple JSON. One file has the chat (user + assistant message) and the other file has the reference context that the answer should follow.

How the evaluation works (in simple terms)

Relevance: I embed the answer and the context using a small sentence-transformer model and check how similar they are.

Completeness: I take the main words from the user’s question and see if the answer covers them.

Hallucination: Sentences that are too different from the context are counted as hallucinated.

Latency: Just the time difference between user and assistant timestamps.

These methods are not perfect, but they are enough for a basic evaluation assignment.

What tests I ran

I made 6 different chat + context files covering topics like:

Ada Lovelace

Gravity

Photosynthesis

CPU vs GPU

Water cycle

Internet

I ran all of them through the tool and generated separate report files (report1.json to report6.json). Each report gave the 4 scores mentioned above. This helped me confirm that the tool works for different inputs and not just one example.

Issues I faced

While building this, I ran into a few errors:

JSONDecodeError because one of my JSON files was empty

Import error from VS Code (Pylance) which I fixed by adding __init__.py

Vector dimension mismatch because I used short vectors by mistake

Some formatting issues in the context files

Fixing these helped me understand how the code flows and where it breaks.

Final note

The tool is simple but does the job. It can evaluate small conversations and generate meaningful scores. I kept the logic easy to follow so I can improve it later if needed.
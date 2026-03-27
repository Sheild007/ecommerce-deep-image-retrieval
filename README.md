# Deep Metric Learning for Image Retrieval

## Installation

```bash
pip install -r requirements.txt
```

## Run main.py

Train all models and evaluate:

```bash
python main.py --epochs 30 --batch-size 64 --lr 0.001 --weight-decay 1e-4
```

Options:
- `--epochs`: Number of epochs (default: 30)
- `--batch-size`: Batch size (default: 32)
- `--lr`: Learning rate (default: 0.001)
- `--weight-decay`: Weight decay (default: 1e-4)
- `--skip-train`: Skip training phase
- `--skip-embeddings`: Skip embedding generation
- `--skip-eval`: Skip evaluation

## Run save_embeddings.py

Precompute and save embeddings:

```bash
python save_embeddings.py --data-dir caltech-101 --weights-dir weights --output-dir embeddings --batch-size 64
```

Options:
- `--data-dir`: Path to dataset (default: caltech-101)
- `--weights-dir`: Directory with model weights (default: weights)
- `--output-dir`: Output directory for embeddings (default: embeddings)
- `--batch-size`: Batch size (default: 32)

## Run evaluate.py

Evaluate saved embeddings:

```bash
python evaluate.py --embeddings-dir embeddings --data-dir caltech-101
```

Options:
- `--embeddings-dir`: Directory with saved embeddings (default: embeddings)
- `--data-dir`: Path to dataset (default: caltech-101)

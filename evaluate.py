import os
import argparse
import numpy as np
from retrieval import recall_at_k, plot_tsne, show_retrieval

def evaluate_experiment(exp_name: str, embeddings_dir: str, graphs_dir: str) -> dict:
    print(f"Evaluating: {exp_name}")

    # Load embeddings and labels
    test_emb = np.load(os.path.join(embeddings_dir, 'embeddings_test.npy'))
    test_labels = np.load(os.path.join(embeddings_dir, 'labels_test.npy'))
    test_paths = np.load(os.path.join(embeddings_dir, 'paths_test.npy'), allow_pickle=True)
    
    exp_output_dir = os.path.join(graphs_dir, exp_name)
    os.makedirs(exp_output_dir, exist_ok=True)
    
    print("Computing Recall@K...")
    r1 = recall_at_k(test_emb, test_labels, k=1)
    r5 = recall_at_k(test_emb, test_labels, k=5)
    r10 = recall_at_k(test_emb, test_labels, k=10)
    
    print(f"Recall@1: {r1:.4f}")
    print(f"Recall@5: {r5:.4f}")
    print(f"Recall@10: {r10:.4f}")
    
    print("Generating t-SNE visualization...")
    tsne_output = os.path.join(exp_output_dir, 'tsne.png')
    plot_tsne(test_emb, test_labels, title=f'{exp_name} - t-SNE Visualization', output_path=tsne_output)
    
    print("Generating retrieval visualizations...")
    retrieval_dir = os.path.join(exp_output_dir, 'retrieval')
    os.makedirs(retrieval_dir, exist_ok=True)
    
    n_queries = min(10, len(test_paths))
    query_indices = np.linspace(0, len(test_paths)-1, n_queries, dtype=int)
    
    for i, query_idx in enumerate(query_indices):
        output_path = os.path.join(retrieval_dir, f'query_{i:02d}.png')
        show_retrieval(
            int(query_idx), test_emb, test_paths, test_labels, 
            k=5, output_path=output_path
        )
    
    print(f"Results saved to {exp_output_dir}")
    
    return {
        'recall@1': r1,
        'recall@5': r5,
        'recall@10': r10
    }

def main() -> None:
    parser = argparse.ArgumentParser(description='Evaluate saved embeddings')
    parser.add_argument('--embeddings-dir', default='embeddings', help='Directory with precomputed embeddings')
    parser.add_argument('--output-dir', default='graphs', help='Directory to save results')
    
    args = parser.parse_args()
    
    experiments = ['contrastive', 'triplet_random', 'triplet_hard']
    results = {}
    
    for exp_name in experiments:
        exp_embeddings_dir = os.path.join(args.embeddings_dir, exp_name)
        
        if not os.path.exists(exp_embeddings_dir):
            print(f"Embeddings not found for {exp_name}: {exp_embeddings_dir}")
            print("Run: python save_embeddings.py")
            continue
        
        results[exp_name] = evaluate_experiment(exp_name, exp_embeddings_dir, args.output_dir)
    
    print("\nEvaluation Summary:")
    print(f"{'Model':<20} {'Recall@1':<12} {'Recall@5':<12} {'Recall@10':<12}")
    
    for exp_name, metrics in results.items():
        print(f"{exp_name:<20} {metrics['recall@1']:<12.4f} {metrics['recall@5']:<12.4f} {metrics['recall@10']:<12.4f}")
    
    print(f"\nResults saved to: {args.output_dir}")

if __name__ == '__main__':
    main()

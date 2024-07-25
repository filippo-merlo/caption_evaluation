import argparse
import os
from rating_datasets.flickr8k_dataset import Flickr8kDataset
from rating_datasets.composite_dataset import CompositeDataset
from rating_datasets.thumb_dataset import ThumbDataset
from rating_datasets.polaris_dataset import PolarisDataset
from rating_datasets.pascal50_dataset import Pascal50Dataset
from rating_datasets.reformulations_dataset import ReformulationsDataset

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', choices=['flickr8k_expert', 'flickr8k_cf', 'composite', 'thumb', 'polaris', 'pascal50', 'reformulations'], required=True)
    parser.add_argument('--eval_method', choices=['correlation', 'pairwise'], default='correlation')
    parser.add_argument('--correlation_type', choices=['pearson', 'spearman', 'kendall_b', 'kendall_c'])
    parser.add_argument('--clip_image_score', action='store_true')
    args = parser.parse_args()

    if args.dataset == 'flickr8k_expert':
        dataset = Flickr8kDataset('expert')
        correlation_type = 'kendall_c' if args.correlation_type is None else args.correlation_type
    elif args.dataset == 'flickr8k_cf':
        dataset = Flickr8kDataset('expert')
        correlation_type = 'kendall_b' if args.correlation_type is None else args.correlation_type
    elif args.dataset == 'composite':
        dataset = CompositeDataset()
        correlation_type = 'kendall_c' if args.correlation_type is None else args.correlation_type
    elif args.dataset == 'thumb':
        dataset = ThumbDataset()
        correlation_type = 'pearson' if args.correlation_type is None else args.correlation_type
    elif args.dataset == 'polaris':
        dataset = PolarisDataset()
        correlation_type = 'kendall_c' if args.correlation_type is None else args.correlation_type
    elif args.dataset == 'pascal50':
        dataset = Pascal50Dataset()
        correlation_type = 'pearson' if args.correlation_type is None else args.correlation_type
    elif args.dataset == 'reformulations':
        dataset = ReformulationsDataset()
        correlation_type = 'pearson' if args.correlation_type is None else args.correlation_type

    dump_file = f'{dataset.get_name()}_data.pkl'
    if os.path.isfile(dump_file):
        print(f'Loading dataset from file: {dump_file}')
        dataset.load()
    else:
        print(f'Collecting data...')
        dataset.collect_data()
        print(f'Dumping dataset to file: {dump_file}')
        dataset.dump()

    print('Computing metrics...')
    dataset.compute_metrics(compute_clip_image_score=args.clip_image_score)

    if args.eval_method == 'correlation':
        res = dataset.compute_correlation()
    else:
        res = dataset.pairwise_comparison()

    print(res)